import pytest
from apps.analytics.models import AnalyticsEvent
from apps.tests.models import TestSession as SessionModel, TestVersion as VersionModel

pytestmark=pytest.mark.django_db

def create_session(api,invite_id=None):
    payload={"test_slug":"hidden-personality"}
    if invite_id: payload["relation_invite_id"]=invite_id
    r=api.post("/api/v1/test-sessions",payload,format="json"); assert r.status_code==201,r.data
    return r.data["data"]["id"]

def submit_complete(api,answer_session,invite_id=None):
    session=create_session(api,invite_id); answer_session(api,session)
    return session,api.post(f"/api/v1/test-sessions/{session}/submit").data["data"]

def make_invite(api,answer_session):
    _,submitted=submit_complete(api,answer_session)
    return api.post("/api/v1/relation-invites",{"result_id":submitted["result_id"]},format="json").data["data"]

def test_create_session(api,login_user):
    login_user(api); session=create_session(api)
    assert api.get(f"/api/v1/test-sessions/{session}").status_code==200
    q=api.get("/api/v1/tests/hidden-personality").data["data"]["current_version"]["questions"][0]
    for option in q["options"][:2]: assert api.put(f"/api/v1/test-sessions/{session}/answers",{"question_id":q["id"],"option_id":option["id"]},format="json").status_code==200
    data=api.get(f"/api/v1/test-sessions/{session}").data["data"]
    assert len(data["answers"])==1 and data["answers"][0]["option_id"]==q["options"][1]["id"]

def test_moon_forest_v3_human_relationship_content(api,login_user):
    login_user(api)
    detail=api.get("/api/v1/tests/hidden-personality").data["data"]
    assert detail["name"]=="月森关系地图"
    assert detail["description"]=="24 个真实的相处瞬间，看看你怎样靠近一个人，又希望怎样被回应。"
    assert detail["current_version"]["version"]==3
    questions=detail["current_version"]["questions"]
    assert len(questions)==24
    assert sum(len(question["options"]) for question in questions)==96
    assert [question["sequence"] for question in questions]==list(range(1,25))
    assert [question["metadata"]["response_mode"] for question in questions].count("behavior")==12
    assert [question["metadata"]["response_mode"] for question in questions].count("need")==12
    for sequence,question in enumerate(questions,1):
        assert question["metadata"]["scene_asset"]==f"/assets/questions/q{sequence:02d}/scene.webp"
        assert [option["label"] for option in question["options"]]==list("ABCD")
    forbidden=("月森","树洞","吊桥","木坝","贝壳","小船","篝火","树屋")
    assert not any(word in question["content"] for question in questions for word in forbidden)

def test_v2_remains_available_for_existing_sessions():
    v2=VersionModel.objects.get(test__slug="hidden-personality",version=2)
    assert v2.status==VersionModel.Status.OFFLINE
    assert v2.questions.count()==24

def test_session_returns_its_version_questions(api,login_user):
    login_user(api)
    session_id=create_session(api)
    session=api.get(f"/api/v1/test-sessions/{session_id}").data["data"]
    assert len(session["questions"])==24
    assert session["questions"][0]["metadata"]["scene_key"]=="unexpected_afternoon"

def test_submit_requires_all_answers(api,login_user):
    login_user(api); session=create_session(api)
    assert api.post(f"/api/v1/test-sessions/{session}/submit").status_code==400

def test_submit_twice(api,login_user,answer_session):
    login_user(api); session=create_session(api); answer_session(api,session)
    first=api.post(f"/api/v1/test-sessions/{session}/submit"); second=api.post(f"/api/v1/test-sessions/{session}/submit")
    assert first.status_code==second.status_code==200
    result_id=first.data["data"]["result_id"]; assert second.data["data"]["result_id"]==result_id
    assert api.get(f"/api/v1/results/{result_id}/preview").status_code==200
    assert api.get(f"/api/v1/results/{result_id}/full").status_code==403
    assert api.post(f"/api/v1/results/{result_id}/unlock",{"unlock_type":"MOCK"},format="json").status_code==200
    assert api.post(f"/api/v1/results/{result_id}/unlock",{"unlock_type":"MOCK"},format="json").status_code==200
    assert api.get(f"/api/v1/results/{result_id}/full").status_code==200

def test_relation_generated(api,login_user,answer_session):
    login_user(api,"user_a"); sa=create_session(api); answer_session(api,sa)
    result_a=api.post(f"/api/v1/test-sessions/{sa}/submit").data["data"]["result_id"]
    invite=api.post("/api/v1/relation-invites",{"result_id":result_a},format="json").data["data"]
    assert api.post(f"/api/v1/relation-invites/{invite['invite_code']}/accept").status_code==400
    login_user(api,"user_b")
    opened=api.get(f"/api/v1/relation-invites/{invite['invite_code']}"); assert opened.status_code==200
    accepted=api.post(f"/api/v1/relation-invites/{invite['invite_code']}/accept"); assert accepted.status_code==200
    accepted2=api.post(f"/api/v1/relation-invites/{invite['invite_code']}/accept"); assert accepted2.status_code==200
    sb=create_session(api,accepted.data["data"]["invite_id"]); answer_session(api,sb)
    submit_b=api.post(f"/api/v1/test-sessions/{sb}/submit"); assert submit_b.status_code==200
    history=api.get("/api/v1/me/relationships").data["data"]; assert len(history)==1
    relation_id=history[0]["id"]
    assert api.get(f"/api/v1/relationships/{relation_id}").status_code==200
    assert api.post(f"/api/v1/test-sessions/{sb}/submit").status_code==200
    assert len(api.get("/api/v1/me/relationships").data["data"])==1
    login_user(api,"user_c"); assert api.get(f"/api/v1/relationships/{relation_id}").status_code==403

def test_legacy_invite_keeps_legacy_test_version(api,login_user):
    user_a=login_user(api,"user_a")
    legacy_version=VersionModel.objects.get(test__slug="hidden-personality",version=1)
    legacy_session=SessionModel.objects.create(user_id=user_a["id"],test_version=legacy_version)
    for question in legacy_version.questions.prefetch_related("options"):
        option=question.options.first()
        response=api.put(f"/api/v1/test-sessions/{legacy_session.id}/answers",{"question_id":question.id,"option_id":option.id},format="json")
        assert response.status_code==200,response.data
    result_id=api.post(f"/api/v1/test-sessions/{legacy_session.id}/submit").data["data"]["result_id"]
    invite=api.post("/api/v1/relation-invites",{"result_id":result_id},format="json").data["data"]

    login_user(api,"user_b")
    accepted=api.post(f"/api/v1/relation-invites/{invite['invite_code']}/accept").data["data"]
    friend_session_id=create_session(api,accepted["invite_id"])
    friend_session=api.get(f"/api/v1/test-sessions/{friend_session_id}").data["data"]
    assert friend_session["test_version_id"]==legacy_version.id
    assert friend_session["questions"][0]["metadata"]=={}

def test_history_analytics_and_permissions(api,login_user,answer_session):
    login_user(api,"user_a"); session=create_session(api); answer_session(api,session)
    result_id=api.post(f"/api/v1/test-sessions/{session}/submit").data["data"]["result_id"]
    assert len(api.get("/api/v1/me/results").data["data"])==1
    assert api.post("/api/v1/events",{"event_name":"test_submit","session_id":session,"properties":{}},format="json").status_code==201
    assert AnalyticsEvent.objects.count()==1
    login_user(api,"user_b")
    assert api.get(f"/api/v1/results/{result_id}/full").status_code==404
    assert api.post(f"/api/v1/results/{result_id}/unlock",{"unlock_type":"MOCK"},format="json").status_code==403

def test_answer_question(api,login_user):
    login_user(api); session=create_session(api); q=api.get("/api/v1/tests/hidden-personality").data["data"]["current_version"]["questions"][0]
    assert api.put(f"/api/v1/test-sessions/{session}/answers",{"question_id":q["id"],"option_id":q["options"][0]["id"]},format="json").status_code==200

def test_resume_session(api,login_user):
    login_user(api); session=create_session(api)
    assert api.get(f"/api/v1/test-sessions/{session}").data["data"]["id"]==session

def test_submit_session(api,login_user,answer_session):
    login_user(api); _,submitted=submit_complete(api,answer_session)
    assert submitted["result_id"]

def test_result_preview(api,login_user,answer_session):
    login_user(api); _,submitted=submit_complete(api,answer_session)
    assert api.get(f"/api/v1/results/{submitted['result_id']}/preview").status_code==200

def test_full_result_requires_unlock(api,login_user,answer_session):
    login_user(api); _,submitted=submit_complete(api,answer_session)
    assert api.get(f"/api/v1/results/{submitted['result_id']}/full").status_code==403

def test_mock_unlock(api,login_user,answer_session):
    login_user(api); _,submitted=submit_complete(api,answer_session); rid=submitted["result_id"]
    assert api.post(f"/api/v1/results/{rid}/unlock",{"unlock_type":"MOCK"},format="json").status_code==200

def test_create_invite(api,login_user,answer_session):
    login_user(api); invite=make_invite(api,answer_session)
    assert invite["invite_code"] and "user" not in invite["invite_code"]

def test_accept_invite(api,login_user,answer_session):
    login_user(api,"user_a"); invite=make_invite(api,answer_session); login_user(api,"user_b")
    assert api.post(f"/api/v1/relation-invites/{invite['invite_code']}/accept").status_code==200

def test_complete_friend_test(api,login_user,answer_session):
    login_user(api,"user_a"); invite=make_invite(api,answer_session); login_user(api,"user_b")
    accepted=api.post(f"/api/v1/relation-invites/{invite['invite_code']}/accept").data["data"]
    _,submitted=submit_complete(api,answer_session,accepted["invite_id"])
    assert submitted["relationship_id"]

def test_relation_access_control(api,login_user,answer_session):
    login_user(api,"user_a"); invite=make_invite(api,answer_session); login_user(api,"user_b")
    accepted=api.post(f"/api/v1/relation-invites/{invite['invite_code']}/accept").data["data"]
    _,submitted=submit_complete(api,answer_session,accepted["invite_id"]); rel=submitted["relationship_id"]
    login_user(api,"user_c"); assert api.get(f"/api/v1/relationships/{rel}").status_code==403
