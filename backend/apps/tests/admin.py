from django.contrib import admin
from .models import Answer, Question, QuestionOption, Test, TestSession, TestVersion

class OptionInline(admin.TabularInline): model = QuestionOption; extra = 0
@admin.register(Test)
class TestAdmin(admin.ModelAdmin): list_display=("slug","name","status","updated_at"); list_filter=("status",); search_fields=("slug","name"); readonly_fields=("created_at","updated_at")
@admin.register(TestVersion)
class TestVersionAdmin(admin.ModelAdmin): list_display=("test","version","question_count","scoring_version","status"); list_filter=("status","test"); readonly_fields=("created_at",)
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin): list_display=("test_version","sequence","type","content"); list_filter=("test_version__test","test_version"); search_fields=("content",); inlines=[OptionInline]; readonly_fields=("created_at",)
@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin): list_display=("question","sequence","label","content"); list_filter=("question__test_version",)
@admin.register(TestSession)
class TestSessionAdmin(admin.ModelAdmin): list_display=("id","user","test_version","status","current_question","updated_at"); list_filter=("status","test_version"); readonly_fields=("started_at","submitted_at","created_at","updated_at")
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin): list_display=("session","question","option","updated_at"); readonly_fields=("created_at","updated_at")
