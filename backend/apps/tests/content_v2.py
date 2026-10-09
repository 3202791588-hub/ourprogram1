"""Immutable content snapshot for the Moon Forest demo test V2.

This is presentation content only. It deliberately contains no formal scoring
weights; replacement scoring remains owned by the Engine layer.
"""

from __future__ import annotations


QUESTION_V2 = [
    {
        "title": "意外空出来的下午",
        "content": "月森突然多出一个不用赶路的下午。你和 TA 会怎么用掉这份意外的空白？",
        "options": ["把小船划向没去过的湖湾", "铺开野餐布，慢慢待到天黑", "回到树屋，各做各的也舒服", "先各自行动，晚点交换故事"],
        "scene_key": "unexpected_afternoon", "scene_asset": "/assets/questions/q01/scene.webp", "chapter": "靠近的方式", "motion_preset": "lake-breeze", "layout": "left-right-staggered",
    },
    {
        "title": "树洞迟迟没有回音",
        "content": "你送进树洞的信放了很久，还没有等到回音。你通常会怎么做？",
        "options": ["再递一片叶子，确认 TA 看见了", "安静等着，TA 忙完自然会回", "去走自己的路，不一直守着树洞", "下次见面再问，免得独自在心里猜"],
        "scene_key": "tree_hollow_reply", "scene_asset": "/assets/questions/q02/scene.webp", "chapter": "靠近的方式", "motion_preset": "letter-and-light", "layout": "right-left-staggered",
    },
    {
        "title": "会发光的贝壳",
        "content": "你在海边捡到一枚会发光的贝壳。第一时间，你最想怎么把这份开心交给 TA？",
        "options": ["马上跑去找 TA，边说边比划", "先收好，见面时认真拿给 TA 看", "拉上 TA，一起去找更多发光贝壳", "把贝壳放在窗边，等 TA 自己发现"],
        "scene_key": "glowing_shell", "scene_asset": "/assets/questions/q03/scene.webp", "chapter": "靠近的方式", "motion_preset": "gentle-ripples", "layout": "left-right-staggered",
    },
    {
        "title": "比想象中热闹的灯会",
        "content": "月森灯会比想象中热闹。走进人群前，你更希望和 TA 怎么行动？",
        "options": ["大部分时间待在一起，别走散", "各自去逛，看到有趣的再回来分享", "先找安静角落，慢慢观察和适应", "逛一小圈就离开，去过两个人的夜晚"],
        "scene_key": "forest_festival", "scene_asset": "/assets/questions/q04/scene.webp", "chapter": "靠近的方式", "motion_preset": "lantern-breath", "layout": "right-left-staggered",
    },
    {
        "title": "山谷对面的灯",
        "content": "夜里，你看见 TA 的灯在山谷另一边亮着。想念冒出来时，你通常会怎么做？",
        "options": ["直接点亮信号灯，让 TA 知道", "送去一片小叶子，留下一点暗示", "先把想念放在心里，等 TA 靠近", "开始计划下一次见面的时间"],
        "scene_key": "valley_lights", "scene_asset": "/assets/questions/q05/scene.webp", "chapter": "靠近的方式", "motion_preset": "mist-and-lights", "layout": "left-right-staggered",
    },
    {
        "title": "树屋关灯的一天",
        "content": "TA 说今天想一个人待在树屋里。你的第一反应更接近哪一种？",
        "options": ["告诉 TA“好”，顺便约好下次见面", "有一点失落，希望 TA 再确认一句在意", "正好去忙自己的事，晚点再联系", "先问问是不是发生了什么"],
        "scene_key": "treehouse_day", "scene_asset": "/assets/questions/q06/scene.webp", "chapter": "靠近的方式", "motion_preset": "window-and-leaves", "layout": "right-left-staggered",
    },
    {
        "title": "被雨冲断的小路",
        "content": "原定的约会小路被雨冲断了。站在岔路口时，你第一句更可能说什么？",
        "options": ["“那就随便选一条，意外也挺有趣。”", "“等一下，我重新找条最稳妥的路线。”", "“你是不是很失望？我们先缓一缓。”", "“先笑一下这场意外，再边走边调整。”"],
        "scene_key": "rain_broken_path", "scene_asset": "/assets/questions/q07/scene.webp", "chapter": "情绪被看见", "motion_preset": "path-pawprints", "layout": "left-right-staggered",
    },
    {
        "title": "带着一身雨回来",
        "content": "TA 带着一身疲惫和雨水回到木屋。你更自然的靠近方式是：",
        "options": ["倒杯热饮，听 TA 把今天慢慢说完", "先问最麻烦的事是什么，马上帮忙处理", "不急着说话，先给 TA 一个安静的拥抱", "留好灯和热水，让 TA 自己缓一会儿"],
        "scene_key": "home_in_rain", "scene_asset": "/assets/questions/q08/scene.webp", "chapter": "情绪被看见", "motion_preset": "rain-and-steam", "layout": "right-left-staggered",
    },
    {
        "title": "芦苇后的“没事”",
        "content": "TA 躲在芦苇后说“我没事”。你听得出来并不完全是这样，会怎么做？",
        "options": ["再靠近一点：“你可以跟我说真的。”", "留在看得见的地方：“想说时我都在。”", "先做一件能让 TA 舒服的小事", "暂时不追问，晚一点再回来看看"],
        "scene_key": "reeds_nothing", "scene_asset": "/assets/questions/q09/scene.webp", "chapter": "情绪被看见", "motion_preset": "mist-and-water", "layout": "left-right-staggered",
    },
    {
        "title": "只想躲在叶子下面",
        "content": "如果今天的你只想缩在一片大叶子下面，哪一种靠近会让你最舒服？",
        "options": ["TA 坐到旁边，认真听你说完", "TA 帮你挡住眼前最麻烦的风", "TA 不追问，只安静陪你待一会儿", "TA 先离开，等你准备好再回来"],
        "scene_key": "under_the_leaf", "scene_asset": "/assets/questions/q10/scene.webp", "chapter": "情绪被看见", "motion_preset": "soft-wind", "layout": "right-left-staggered",
    },
    {
        "title": "沉进水里的羽毛",
        "content": "一片发光羽毛沉进水里，TA 为这件你不太理解的小事难过。你更可能：",
        "options": ["先接受这件事对 TA 来说真的很重要", "问问这片羽毛背后藏着什么故事", "陪 TA 换个角度，也许还能找到别的光", "等情绪平静，再一起谈发生了什么"],
        "scene_key": "sinking_feather", "scene_asset": "/assets/questions/q11/scene.webp", "chapter": "情绪被看见", "motion_preset": "feather-ripple", "layout": "left-right-staggered",
    },
    {
        "title": "夜路只剩一盏灯",
        "content": "夜路上只剩一盏灯。哪一句话最能让你觉得“我们是一起的”？",
        "options": ["“我明白你为什么会这样难受。”", "“不用急，我会在这里陪你。”", "“我们一起把接下来的路找出来。”", "“你先休息，这一段我来背。”"],
        "scene_key": "one_night_light", "scene_asset": "/assets/questions/q12/scene.webp", "chapter": "情绪被看见", "motion_preset": "camp-light", "layout": "right-left-staggered",
    },
    {
        "title": "吊桥开始摇晃",
        "content": "话越说越急，脚下的吊桥也开始摇晃。你更可能先做什么？",
        "options": ["继续讲清楚，不想带着误会停下来", "先离开桥面，约好冷静后再回来", "先说“我现在有点受伤”，让 TA 看见感受", "先处理眼前最具体的分歧，再谈其他部分"],
        "scene_key": "swaying_bridge", "scene_asset": "/assets/questions/q13/scene.webp", "chapter": "分歧与修复", "motion_preset": "bridge-settle", "layout": "left-right-staggered",
    },
    {
        "title": "倒过来的地图",
        "content": "你突然发现，争了半天的地图一直拿反了。意识到自己误会 TA 时，你会：",
        "options": ["马上说“是我弄错了，对不起”", "解释自己刚才为什么会那样理解", "把地图转正，用行动重新带路", "先用一句玩笑松开尴尬，再认真道歉"],
        "scene_key": "upside_down_map", "scene_asset": "/assets/questions/q14/scene.webp", "chapter": "分歧与修复", "motion_preset": "map-turn", "layout": "right-left-staggered",
    },
    {
        "title": "被水冲歪的踏脚石",
        "content": "一块踏脚石被水冲歪了。关系出现磕碰后，你最希望 TA 怎样把它放回去？",
        "options": ["清楚地说出“对不起”", "真正明白你为什么会受伤", "告诉你以后会具体怎么改变", "主动靠近，让两个人先重新连接"],
        "scene_key": "stepping_stones", "scene_asset": "/assets/questions/q15/scene.webp", "chapter": "分歧与修复", "motion_preset": "water-settle", "layout": "left-right-staggered",
    },
    {
        "title": "又漏水的小木坝",
        "content": "昨天补好的木坝又漏水了。同一个问题再次出现，你更想和 TA 怎么处理？",
        "options": ["重新定一条清楚的规则，照着执行", "先找找为什么总在同一个地方漏水", "各改一点，做一个双方都能接受的方案", "承认有些地方很难彻底修好，学会共存"],
        "scene_key": "leaking_dam", "scene_asset": "/assets/questions/q16/scene.webp", "chapter": "分歧与修复", "motion_preset": "stream-settle", "layout": "right-left-staggered",
    },
    {
        "title": "篝火两边的沉默",
        "content": "争吵后的篝火还没熄，但你们暂时谁也没说话。你更希望接下来发生什么？",
        "options": ["今晚把话说开，不让问题留到明天", "约好明早再谈，现在先各自冷静", "不必马上解释，但至少坐回彼此身边", "先分别想清楚，谁准备好谁先开口"],
        "scene_key": "fire_between_us", "scene_asset": "/assets/questions/q17/scene.webp", "chapter": "分歧与修复", "motion_preset": "fire-breath", "layout": "left-right-staggered",
    },
    {
        "title": "重新靠岸的小船",
        "content": "小船终于重新靠岸。和好以后，什么最能让你确认这件事真的过去了？",
        "options": ["把刚才没说清的话完整聊完", "一个拥抱，确认彼此不再推开", "一起做件轻松的小事，让气氛重新流动", "看到那个问题以后真的有了变化"],
        "scene_key": "boat_returns", "scene_asset": "/assets/questions/q18/scene.webp", "chapter": "分歧与修复", "motion_preset": "rope-and-ripples", "layout": "right-left-staggered",
    },
    {
        "title": "湖谷里的两个方向",
        "content": "周末的湖谷同时出现一条新小径和一块熟悉的晒太阳石。你更想把时间放在哪里？",
        "options": ["一起走进没去过的新小径", "回到熟悉的位置，舒服地待上一天", "不提前决定，看当天心情再选", "一半一起探索，一半各自活动"],
        "scene_key": "two_weekend_paths", "scene_asset": "/assets/questions/q19/scene.webp", "chapter": "一起生活", "motion_preset": "cloud-and-water", "layout": "left-right-staggered",
    },
    {
        "title": "雪山车站的地图",
        "content": "雪山车站只剩一张地图，远处却有好几条路。旅行时，你最舒服的方式是：",
        "options": ["把路线、时间和停靠点都提前确认好", "只定几个重要地点，中间留给意外", "先出发，走到哪里再决定下一站", "让更擅长规划的人领路，另一个轻松跟上"],
        "scene_key": "snow_station_map", "scene_asset": "/assets/questions/q20/scene.webp", "chapter": "一起生活", "motion_preset": "map-and-snow", "layout": "right-left-staggered",
    },
    {
        "title": "月湖边的小石头",
        "content": "月湖边摆着几颗代表共同日子的石头。对纪念日，你真正看重的是：",
        "options": ["TA 有没有花心思准备一件特别的事", "不必隆重，但 TA 要记得并表达在意", "不用固定日期，想庆祝时就庆祝", "比起某一天，更在意平时有没有被放在心上"],
        "scene_key": "moon_lake_stones", "scene_asset": "/assets/questions/q21/scene.webp", "chapter": "一起生活", "motion_preset": "stone-glow", "layout": "left-right-staggered",
    },
    {
        "title": "树屋和溪流",
        "content": "TA 喜欢在溪流里玩水，你更喜欢待在树屋看书。兴趣不同时，你觉得怎样最舒服？",
        "options": ["各自保留喜欢的世界，不必勉强同步", "偶尔交换一天，体验对方为什么喜欢", "一起寻找一个谁都没试过的新兴趣", "分别去玩，晚上回到平台交换故事"],
        "scene_key": "treehouse_and_stream", "scene_asset": "/assets/questions/q22/scene.webp", "chapter": "一起生活", "motion_preset": "page-and-water", "layout": "right-left-staggered",
    },
    {
        "title": "长桌上的四样东西",
        "content": "面对一个重要的共同决定，长桌上放着地图、暖石、指南针和一张空白纸。你会先拿起什么？",
        "options": ["地图——先把现实条件看清楚", "暖石——先确认两个人真实的感受", "指南针——谁更了解方向，谁先主导", "空白纸——慢一点，写出双方都安心的方案"],
        "scene_key": "four_things_table", "scene_asset": "/assets/questions/q23/scene.webp", "chapter": "一起生活", "motion_preset": "map-and-stones", "layout": "left-right-staggered",
    },
    {
        "title": "最后一段月光路",
        "content": "旅程快结束了。望着通往营地的几条月光路，你最向往哪一种同行方式？",
        "options": ["两个人大部分时候并肩前进", "有时由你领路，有时放心跟随 TA", "偶尔走不同的小路，之后再汇合", "一起选个地方，把它慢慢建成共同营地"],
        "scene_key": "last_moonlit_path", "scene_asset": "/assets/questions/q24/scene.webp", "chapter": "一起生活", "motion_preset": "final-pawprints", "layout": "right-left-staggered",
    },
]


def validate_question_v2() -> None:
    if len(QUESTION_V2) != 24:
        raise ValueError("Moon Forest V2 must contain exactly 24 questions")
    for sequence, question in enumerate(QUESTION_V2, 1):
        if len(question["options"]) != 4:
            raise ValueError(f"Q{sequence:02d} must contain exactly four options")
        expected_asset = f"/assets/questions/q{sequence:02d}/scene.webp"
        if question["scene_asset"] != expected_asset:
            raise ValueError(f"Q{sequence:02d} scene asset must be {expected_asset}")


validate_question_v2()
