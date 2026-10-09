from django.conf import settings
from django.db import models

class Test(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft"; PUBLISHED = "published"; OFFLINE = "offline"
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    cover_url = models.URLField(blank=True)
    status = models.CharField(max_length=16, choices=Status, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str: return self.name

class TestVersion(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft"; PUBLISHED = "published"; OFFLINE = "offline"
    test = models.ForeignKey(Test, on_delete=models.PROTECT, related_name="versions")
    version = models.PositiveIntegerField()
    question_count = models.PositiveIntegerField(default=0)
    scoring_version = models.CharField(max_length=40, default="mock-v1")
    status = models.CharField(max_length=16, choices=Status, default=Status.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["test", "version"], name="unique_test_version")]
        ordering = ["test_id", "version"]
    def __str__(self) -> str: return f"{self.test.name} v{self.version}"

class Question(models.Model):
    test_version = models.ForeignKey(TestVersion, on_delete=models.PROTECT, related_name="questions")
    sequence = models.PositiveIntegerField()
    type = models.CharField(max_length=20, default="single")
    content = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["test_version", "sequence"], name="unique_question_sequence")]
        ordering = ["test_version_id", "sequence"]
    def __str__(self) -> str: return f"{self.test_version} Q{self.sequence}"

class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name="options")
    label = models.CharField(max_length=8)
    content = models.CharField(max_length=300)
    score_config = models.JSONField(default=dict, blank=True)
    sequence = models.PositiveIntegerField()
    class Meta:
        constraints = [models.UniqueConstraint(fields=["question", "sequence"], name="unique_option_sequence")]
        ordering = ["question_id", "sequence"]
    def __str__(self) -> str: return f"{self.question} {self.label}"

class TestSession(models.Model):
    class Status(models.TextChoices):
        CREATED = "CREATED"; ANSWERING = "ANSWERING"; SUBMITTED = "SUBMITTED"; RESULT_GENERATED = "RESULT_GENERATED"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="test_sessions")
    test_version = models.ForeignKey(TestVersion, on_delete=models.PROTECT, related_name="sessions")
    relation_invite = models.ForeignKey("relations.RelationInvite", null=True, blank=True, on_delete=models.PROTECT, related_name="sessions")
    status = models.CharField(max_length=24, choices=Status, default=Status.CREATED)
    current_question = models.PositiveIntegerField(default=1)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Answer(models.Model):
    session = models.ForeignKey(TestSession, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    option = models.ForeignKey(QuestionOption, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["session", "question"], name="unique_session_question_answer")]
