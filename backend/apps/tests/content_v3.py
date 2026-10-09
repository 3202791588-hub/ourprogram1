"""Immutable human-relationship copy snapshot for Moon Forest V3.

The V2 visual metadata is deliberately reused so the approved 24 illustrations
stay stable.  This module defines presentation copy and response-mode metadata
only; scoring and relationship matching remain owned by replaceable Engines.
"""

from __future__ import annotations

from .content_v2 import QUESTION_V2


COPY_V3 = [
    {
        "title": "意外空出来的下午", "response_mode": "behavior", "chapter": "靠近与空间",
        "content": "一个周末下午突然空了出来。你第一时间更想和 TA 怎么安排？",
        "options": ["一起去一个都没去过的地方", "找个舒服的位置，慢慢待上一下午", "待在同一个空间里，各做各的事情", "先各自安排，晚一点再交换今天的故事"],
    },
    {
        "title": "迟迟没有回音的消息", "response_mode": "behavior", "chapter": "靠近与空间",
        "content": "你给 TA 发了一条很想分享的消息，过了很久还没有回复。你通常会怎么做？",
        "options": ["再发一句，确认 TA 有没有看到", "先等一等，TA 忙完自然会回复", "继续做自己的事，不让注意力一直停在那里", "等下次见面再问，避免一个人反复猜测"],
    },
    {
        "title": "第一时间想分享的开心", "response_mode": "behavior", "chapter": "靠近与空间",
        "content": "你刚刚遇到一件很开心的事，第一时间会怎样和 TA 分享？",
        "options": ["马上发消息或打电话，边说边表达兴奋", "先留在心里，等见面时认真告诉 TA", "直接邀请 TA 一起参与，让开心变成共同经历", "发一张照片或留下线索，等 TA 主动发现"],
    },
    {
        "title": "比想象中热闹的聚会", "response_mode": "need", "chapter": "靠近与空间",
        "content": "你和 TA 一起参加一个比预想中热闹的聚会。哪种相处方式会让你最舒服？",
        "options": ["大部分时间待在一起，彼此有个照应", "各自去认识人，过一会儿再回来分享", "先一起待在安静一点的位置，适应后再行动", "简单露面后离开，把剩下的时间留给两个人"],
    },
    {
        "title": "一段暂时见不到的日子", "response_mode": "need", "chapter": "靠近与空间",
        "content": "如果你们有一段时间见不到面，哪种联系最能让你感到安心？",
        "options": ["直接告诉彼此“我想你了”", "偶尔分享日常的小事，保持生活里的存在感", "各自忙自己的事，不需要固定频率也能信任彼此", "提前确定下一次见面的时间，让等待有个落点"],
    },
    {
        "title": "想独处的一天", "response_mode": "need", "chapter": "靠近与空间",
        "content": "TA 说今天想一个人待着。哪种表达最能让你既尊重 TA，也不会不安？",
        "options": ["“我今天需要独处，明天再来找你。”", "“不是你的问题，我还是很在意你。”", "不必特别解释，各自休息后自然联系就好", "简单告诉你发生了什么，再留出独处时间"],
    },
    {
        "title": "突然被打乱的约会", "response_mode": "behavior", "chapter": "情绪怎样被看见",
        "content": "原本安排好的约会突然进行不下去了。你第一句更可能说什么？",
        "options": ["“那就临时换一个，意外也可能挺有趣。”", "“等一下，我找一个更稳妥的替代方案。”", "“你是不是有点失望？我们先缓一缓。”", "“先笑一下这场意外，再一起慢慢调整。”"],
    },
    {
        "title": "疲惫的一天结束后", "response_mode": "behavior", "chapter": "情绪怎样被看见",
        "content": "TA 忙完疲惫的一天回到你身边。你更自然的靠近方式是：",
        "options": ["准备一点喝的，听 TA 把今天慢慢说完", "先问最麻烦的事情是什么，看看能不能解决", "不急着问，先给 TA 一个安静的拥抱", "把环境照顾好，让 TA 自己缓一会儿"],
    },
    {
        "title": "一句听起来不像“没事”的没事", "response_mode": "behavior", "chapter": "情绪怎样被看见",
        "content": "TA 说“我没事”，但你感觉事实并不完全是这样。你通常会怎么做？",
        "options": ["再问一次：“你可以跟我说真实的感受。”", "留在附近：“你想说的时候我都在。”", "先做一件可能让 TA 轻松一点的小事", "暂时不追问，晚一点再回来看看"],
    },
    {
        "title": "只想安静缩起来的时候", "response_mode": "need", "chapter": "情绪怎样被看见",
        "content": "如果今天的你什么都不想处理，哪一种靠近会让你最舒服？",
        "options": ["TA 坐下来，认真听你把感受说完", "TA 帮你处理眼前最麻烦的一件事", "TA 不追问，只安静陪你待一会儿", "TA 先给你空间，等你准备好再回来"],
    },
    {
        "title": "一件 TA 不太理解的小事", "response_mode": "need", "chapter": "情绪怎样被看见",
        "content": "你因为一件 TA 不太理解的小事难过。你最希望 TA 怎样回应？",
        "options": ["先接受这件事对你来说真的很重要", "问问这件事背后对你意味着什么", "陪你换个角度，寻找能让你舒服一点的可能", "先给情绪一点时间，平静后再认真聊"],
    },
    {
        "title": "低谷里最想听的一句话", "response_mode": "need", "chapter": "情绪怎样被看见",
        "content": "当你处在一段低谷里，哪一句话最能让你感到“我们是一起的”？",
        "options": ["“我明白你为什么会这样难受。”", "“不用急，我会在这里陪你。”", "“我们一起把接下来要做的事理清楚。”", "“你先休息，眼前这一部分我来处理。”"],
    },
    {
        "title": "讨论越来越急", "response_mode": "behavior", "chapter": "分歧与修复",
        "content": "你和 TA 的讨论越来越急，双方都开始听不进对方的话。你更可能先做什么？",
        "options": ["继续把自己的意思讲清楚，不想带着误会停下", "先暂停，但明确约好什么时候继续谈", "先说“我现在有点受伤”，让 TA 看见感受", "先处理眼前最具体的分歧，其他问题稍后再谈"],
    },
    {
        "title": "发现自己误会了 TA", "response_mode": "behavior", "chapter": "分歧与修复",
        "content": "争执过后，你发现自己刚才误会了 TA。你更可能怎么做？",
        "options": ["直接说“是我弄错了，对不起”", "先解释自己为什么会那样理解，再认真道歉", "不说太多，先用行动把造成的问题修正", "先用一点轻松的方式缓和尴尬，再认真道歉"],
    },
    {
        "title": "关系磕碰之后", "response_mode": "need", "chapter": "分歧与修复",
        "content": "TA 的某个做法让你受伤。之后，什么最能让你感到这段关系正在被修复？",
        "options": ["TA 清楚地说出“对不起”", "TA 真正明白你为什么会受伤", "TA 说明以后会具体做出什么改变", "TA 主动靠近，让两个人先恢复连接"],
    },
    {
        "title": "同一个问题又出现", "response_mode": "behavior", "chapter": "分歧与修复",
        "content": "你们以为已经解决的问题再次出现。你更倾向怎样处理？",
        "options": ["重新定一条更清楚的规则，并认真执行", "一起寻找它为什么总在相似的位置发生", "双方各调整一点，形成都能接受的新方案", "承认有些差异很难消失，讨论怎样与它共存"],
    },
    {
        "title": "争吵后的沉默", "response_mode": "need", "chapter": "分歧与修复",
        "content": "争吵后，你们暂时谁也没有说话。你更希望接下来发生什么？",
        "options": ["今晚把话说开，不让问题留到明天", "约好明天再谈，现在先各自冷静", "不必马上解释，但至少重新坐回彼此身边", "先分别想清楚，谁准备好谁先开口"],
    },
    {
        "title": "怎样才算真的和好", "response_mode": "need", "chapter": "分歧与修复",
        "content": "一次分歧暂时结束后，什么最能让你确认“我们真的和好了”？",
        "options": ["把刚才没说清楚的部分完整聊完", "一个拥抱或明确的亲近，确认彼此不再推开", "一起做件轻松的小事，让相处重新自然起来", "在之后的日子里，真的看到相关行为发生变化"],
    },
    {
        "title": "周末的两个方向", "response_mode": "behavior", "chapter": "共同生活的节奏",
        "content": "一个没有固定安排的周末，你通常更想和 TA 怎么度过？",
        "options": ["一起去一个没体验过的新地方", "回到熟悉又舒服的安排里放松一天", "不提前决定，看当天状态再选择", "一部分时间一起，一部分时间各自活动"],
    },
    {
        "title": "一起旅行的节奏", "response_mode": "behavior", "chapter": "共同生活的节奏",
        "content": "和 TA 一起旅行时，哪种安排方式最接近你？",
        "options": ["把路线、时间和重要事项都提前确认好", "只定几个关键地点，其余时间留给意外", "先出发，走到哪里再决定下一站", "谁更擅长规划谁负责，另一个配合补位"],
    },
    {
        "title": "纪念日真正重要的事", "response_mode": "need", "chapter": "共同生活的节奏",
        "content": "对于纪念日或对你们有意义的日子，你真正看重的是什么？",
        "options": ["TA 有没有花心思准备一件特别的事", "不必隆重，但 TA 要记得并表达在意", "不用固定日期，想庆祝的时候自然庆祝", "比起某一天，更在意平时有没有被放在心上"],
    },
    {
        "title": "喜欢的事情不一样", "response_mode": "need", "chapter": "共同生活的节奏",
        "content": "你和 TA 喜欢的事情不太一样。哪种相处方式会让你觉得最舒服？",
        "options": ["各自保留喜欢的世界，不必勉强同步", "偶尔体验对方的兴趣，理解对方为什么喜欢", "一起寻找一个双方都没尝试过的新兴趣", "分别去做喜欢的事，之后再交换彼此的故事"],
    },
    {
        "title": "一个重要的共同决定", "response_mode": "behavior", "chapter": "共同生活的节奏",
        "content": "面对一个会影响两个人的重要决定，你通常会先做什么？",
        "options": ["先把现实条件、成本和风险整理清楚", "先确认双方真正的感受和在意的部分", "看看谁更了解这件事，由更擅长的人先主导", "把不同方案都写出来，慢慢找到双方都安心的选择"],
    },
    {
        "title": "你向往的同行方式", "response_mode": "need", "chapter": "共同生活的节奏",
        "content": "如果把一段关系想得更长远一些，你最向往哪一种同行方式？",
        "options": ["大部分时候共享生活节奏，很多事情一起完成", "有时由你带领，有时也能放心跟随 TA", "彼此保留独立空间，需要时再重新靠近", "一起确定重要方向，慢慢建设属于两个人的生活"],
    },
]


if len(COPY_V3) != len(QUESTION_V2) or len(COPY_V3) != 24:
    raise ValueError("Moon Forest V3 must contain exactly 24 questions")

QUESTION_V3 = []
for visual, copy in zip(QUESTION_V2, COPY_V3):
    question = {**visual, **copy}
    if question["response_mode"] not in {"behavior", "need"}:
        raise ValueError("V3 response_mode must be behavior or need")
    if len(question["options"]) != 4:
        raise ValueError("Every Moon Forest V3 question must contain four options")
    QUESTION_V3.append(question)

