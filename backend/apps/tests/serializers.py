from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Question, QuestionOption, Test, TestSession, TestVersion

class OptionSerializer(serializers.ModelSerializer):
    class Meta: model=QuestionOption; fields=("id","label","content","sequence")
class QuestionSerializer(serializers.ModelSerializer):
    options=OptionSerializer(many=True)
    class Meta: model=Question; fields=("id","sequence","type","content","metadata","options")
class TestVersionSerializer(serializers.ModelSerializer):
    questions=QuestionSerializer(many=True)
    class Meta: model=TestVersion; fields=("id","version","question_count","scoring_version","questions")
class TestListSerializer(serializers.ModelSerializer):
    class Meta: model=Test; fields=("slug","name","description","cover_url")
class TestDetailSerializer(TestListSerializer):
    current_version=serializers.SerializerMethodField()
    class Meta(TestListSerializer.Meta): fields=TestListSerializer.Meta.fields+("current_version",)
    @extend_schema_field(TestVersionSerializer(allow_null=True))
    def get_current_version(self,obj):
        version=obj.versions.filter(status=TestVersion.Status.PUBLISHED).order_by("-version").first()
        return TestVersionSerializer(version).data if version else None
class CreateSessionSerializer(serializers.Serializer):
    test_slug=serializers.SlugField(); relation_invite_id=serializers.IntegerField(required=False)
class SaveAnswerSerializer(serializers.Serializer):
    question_id=serializers.IntegerField(); option_id=serializers.IntegerField()
class SessionSerializer(serializers.ModelSerializer):
    answers=serializers.SerializerMethodField()
    questions=serializers.SerializerMethodField()
    class Meta: model=TestSession; fields=("id","test_version_id","status","current_question","relation_invite_id","questions","answers")
    def get_answers(self,obj): return [{"question_id":a.question_id,"option_id":a.option_id} for a in obj.answers.all()]
    @extend_schema_field(QuestionSerializer(many=True))
    def get_questions(self,obj): return QuestionSerializer(obj.test_version.questions.all(),many=True).data
