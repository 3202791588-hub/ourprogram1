import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

@pytest.fixture(autouse=True)
def demo_data(db): call_command("seed_demo",verbosity=0)

@pytest.fixture
def api(): return APIClient()

def login(api,user="user_a"):
    response=api.post("/api/v1/auth/wechat",{"mock_user":user},format="json")
    assert response.status_code==200,response.data
    api.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['data']['access_token']}")
    return response.data["data"]["user"]

@pytest.fixture
def login_user(): return login

def answer_all(api,session_id):
    detail=api.get("/api/v1/tests/hidden-personality").data["data"]
    for question in detail["current_version"]["questions"]:
        r=api.put(f"/api/v1/test-sessions/{session_id}/answers",{"question_id":question["id"],"option_id":question["options"][0]["id"]},format="json")
        assert r.status_code==200,r.data

@pytest.fixture
def answer_session(): return answer_all
