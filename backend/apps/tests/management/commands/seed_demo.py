from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from apps.relations.models import RelationTemplate
from apps.results.models import PersonalityTemplate
from apps.tests.models import Question,QuestionOption,Test,TestVersion

QUESTIONS=[
"进入一个陌生聚会时，你通常会？","休息日你更想怎样度过？","朋友突然找你倾诉时，你会？","面对新计划，你通常？","聊天冷场时，你会？","做决定时，你更依赖？","计划被打乱时，你会？","你更容易注意到？","遇到分歧时，你倾向？","收到消息后，你通常？","旅行前你会？","压力大时，你更需要？","认识新朋友时，你会？","工作完成后，你更在意？","朋友迟到时，你会？","面对未知机会，你会？","群聊中你通常？","别人误解你时，你会？","你理想的关系节奏是？","获得好消息时，你会？","环境变化时，你通常？","表达关心时，你更常？","遇到复杂问题时，你会？","一天结束时，你更喜欢？"]
OPTIONS=["先观察再行动","主动尝试一下","找熟悉的人同行","按当下感受决定"]
PERSONALITIES={
"night_cat":{"name":"夜行猫型观察者","tags":["慢热","敏感","独立"],"summary":"你通常先观察环境，再决定是否进入关系。","sections":[{"title":"深度分析","content":"你重视边界与真实连接，适合给自己充分的适应时间。"},{"title":"关系特点","content":"比起高频互动，你更看重交流的质量。"},{"title":"建议","content":"需要空间时直接表达，比默默退后更容易被理解。"}]},
"golden_retriever":{"name":"金毛型连接者","tags":["热情","真诚","有行动力"],"summary":"你擅长让关系快速暖起来，也愿意主动回应他人。","sections":[{"title":"深度分析","content":"你通过行动传递善意，容易成为群体里的连接点。"},{"title":"关系特点","content":"你期待及时而清晰的回应。"},{"title":"建议","content":"照顾别人时也要保留自己的节奏。"}]},
"fox":{"name":"狐狸型探索者","tags":["好奇","灵活","有主见"],"summary":"你喜欢发现新鲜路径，并用自己的方式理解世界。","sections":[{"title":"深度分析","content":"你对变化敏感，能快速找到新的可能。"},{"title":"关系特点","content":"共同探索会让你更容易建立连接。"},{"title":"建议","content":"重要决定前给稳定需求留出位置。"}]}}
RELATIONS={
"late_night_radio":{"name":"深夜电台型好友","summary":"你们更适合深入交流，而不是高频社交。"},
"adventure_partner":{"name":"冒险搭档型好友","summary":"新鲜体验能快速点亮你们的互动。"},
"steady_companion":{"name":"稳定同行型好友","summary":"你们容易在可靠的节奏中积累信任。"}}

class Command(BaseCommand):
    help="Create idempotent Demo test, questions and Mock templates"
    @transaction.atomic
    def handle(self,*args,**options):
        test,_=Test.objects.update_or_create(slug="hidden-personality",defaults={"name":"月森关系地图","description":"24 个真实的相处瞬间，看看你怎样靠近一个人，又希望怎样被回应。","status":Test.Status.PUBLISHED})
        has_published_content=TestVersion.objects.filter(test=test,version__gte=2).exists()
        version,_=TestVersion.objects.update_or_create(test=test,version=1,defaults={"question_count":24,"scoring_version":"mock-v1","status":TestVersion.Status.OFFLINE if has_published_content else TestVersion.Status.PUBLISHED,"published_at":timezone.now()})
        for seq,content in enumerate(QUESTIONS,1):
            q,_=Question.objects.update_or_create(test_version=version,sequence=seq,defaults={"content":content,"type":"single"})
            for oseq,text in enumerate(OPTIONS,1): QuestionOption.objects.update_or_create(question=q,sequence=oseq,defaults={"label":"ABCD"[oseq-1],"content":text,"score_config":{}})
        for key,payload in PERSONALITIES.items(): PersonalityTemplate.objects.update_or_create(key=key,defaults={"name":payload["name"],"version":"mock-v1","payload":payload,"active":True})
        for key,payload in RELATIONS.items(): RelationTemplate.objects.update_or_create(key=key,defaults={"name":payload["name"],"version":"mock-v1","payload":payload,"active":True})
        self.stdout.write(self.style.SUCCESS("Demo data ready"))
