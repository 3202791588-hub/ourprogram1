from django.db import migrations
from django.utils import timezone


def publish_v3(apps, schema_editor):
    # Immutable copy snapshot. Never edit V3 in place after it is deployed.
    from apps.tests.content_v3 import QUESTION_V3

    Test = apps.get_model("tests", "Test")
    TestVersion = apps.get_model("tests", "TestVersion")
    Question = apps.get_model("tests", "Question")
    QuestionOption = apps.get_model("tests", "QuestionOption")

    test, _ = Test.objects.update_or_create(
        slug="hidden-personality",
        defaults={
            "name": "月森关系地图",
            "description": "24 个真实的相处瞬间，看看你怎样靠近一个人，又希望怎样被回应。",
            "status": "published",
        },
    )
    TestVersion.objects.filter(test=test, status="published").exclude(version=3).update(status="offline")
    version, _ = TestVersion.objects.update_or_create(
        test=test,
        version=3,
        defaults={
            "question_count": 24,
            "scoring_version": "mock-v1",
            "status": "published",
            "published_at": timezone.now(),
        },
    )

    for sequence, payload in enumerate(QUESTION_V3, 1):
        metadata = {
            "title": payload["title"],
            "response_mode": payload["response_mode"],
            "scene_key": payload["scene_key"],
            "scene_asset": payload["scene_asset"],
            "chapter": payload["chapter"],
            "motion_preset": payload["motion_preset"],
            "layout": payload["layout"],
        }
        question, _ = Question.objects.update_or_create(
            test_version=version,
            sequence=sequence,
            defaults={"content": payload["content"], "type": "single", "metadata": metadata},
        )
        for option_sequence, option_content in enumerate(payload["options"], 1):
            QuestionOption.objects.update_or_create(
                question=question,
                sequence=option_sequence,
                defaults={
                    "label": "ABCD"[option_sequence - 1],
                    "content": option_content,
                    "score_config": {},
                },
            )


def unpublish_v3(apps, schema_editor):
    Test = apps.get_model("tests", "Test")
    TestVersion = apps.get_model("tests", "TestVersion")
    test = Test.objects.filter(slug="hidden-personality").first()
    if test is None:
        return
    TestVersion.objects.filter(test=test, version=3).update(status="offline")
    TestVersion.objects.filter(test=test, version=2).update(status="published")


class Migration(migrations.Migration):
    dependencies = [("tests", "0003_publish_moon_forest_v2")]
    operations = [migrations.RunPython(publish_v3, unpublish_v3)]

