from django.db import migrations
from django.utils import timezone


def publish_v2(apps, schema_editor):
    # This content module is an immutable snapshot. Future copy changes must be
    # published as a new TestVersion and a new migration, never edited in place.
    from apps.tests.content_v2 import QUESTION_V2

    Test = apps.get_model("tests", "Test")
    TestVersion = apps.get_model("tests", "TestVersion")
    Question = apps.get_model("tests", "Question")
    QuestionOption = apps.get_model("tests", "QuestionOption")

    test, _ = Test.objects.update_or_create(
        slug="hidden-personality",
        defaults={
            "name": "月森关系地图",
            "description": "24 个相处瞬间，看看你习惯怎样靠近、回应和陪伴一个人。",
            "status": "published",
        },
    )
    TestVersion.objects.filter(test=test, status="published").exclude(version=2).update(status="offline")
    version, _ = TestVersion.objects.update_or_create(
        test=test,
        version=2,
        defaults={
            "question_count": 24,
            "scoring_version": "mock-v1",
            "status": "published",
            "published_at": timezone.now(),
        },
    )

    for sequence, payload in enumerate(QUESTION_V2, 1):
        metadata = {
            "title": payload["title"],
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


def unpublish_v2(apps, schema_editor):
    Test = apps.get_model("tests", "Test")
    TestVersion = apps.get_model("tests", "TestVersion")
    test = Test.objects.filter(slug="hidden-personality").first()
    if test is None:
        return
    TestVersion.objects.filter(test=test, version=2).update(status="offline")
    TestVersion.objects.filter(test=test, version=1).update(status="published")


class Migration(migrations.Migration):
    dependencies = [("tests", "0002_initial")]
    operations = [migrations.RunPython(publish_v2, unpublish_v2)]
