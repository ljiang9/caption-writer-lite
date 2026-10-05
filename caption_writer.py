"""caption-writer-lite：按主题/平台风格模板生成多版配文，含 hashtag 规则。

平台风格：
- x        ：简短、有力、带一个钩子；
- weibo    ：口语、表情、多个话题标签；
- xiaohongshu：emoji 开头、软种草、密集 hashtag；
- linkedin ：专业、克制、价值导向。
可选 LLM 生成更多版本；无 key 时本地模板已能产出多版配文。
"""

from __future__ import annotations

import json
import os
import re
import urllib.request

PLATFORMS = {
    "x": {
        "templates": [
            "{topic}：{angle}",
            "你知道{topic}还能这样玩吗？{angle}",
            "关于{topic}，这三点值得一看。{angle}",
        ],
        "max_hashtags": 3,
    },
    "weibo": {
        "templates": [
            "分享一个关于{topic}的小经验 ✨ {angle} #分享#",
            "{topic} 这件事，我踩过坑也趟过路 🙈 {angle}",
            "今天聊聊{topic}～{angle} 欢迎评论区补充👇",
        ],
        "max_hashtags": 5,
    },
    "xiaohongshu": {
        "templates": [
            "🌷 {topic}新手必看！{angle}\n建议收藏⭐️",
            "救命🆘 原来{topic}可以这么简单！{angle}",
            "{topic}避坑指南来啦📝 {angle} 姐妹们码住！",
        ],
        "max_hashtags": 8,
    },
    "linkedin": {
        "templates": [
            "在{topic}上，我们总结了三条经验：{angle}",
            "{topic}不只是技术问题，更是协作问题。{angle}",
        ],
        "max_hashtags": 2,
    },
}

ANGLES = [
    "核心是先把目标想清楚，再动手。",
    "关键在于持续迭代，而不是一步到位。",
    "工具不重要，思路才重要。",
]


def make_hashtags(keywords: list[str], limit: int) -> list[str]:
    """把关键词转成 #标签，去重并限制数量。"""
    tags = []
    seen = set()
    for kw in keywords:
        kw = kw.strip().lstrip("#")
        if kw and kw not in seen:
            seen.add(kw)
            tags.append(f"#{kw}")
        if len(tags) >= limit:
            break
    return tags


def generate_captions(topic: str, platform: str = "x",
                      keywords: list[str] | None = None) -> list[str]:
    """按平台风格生成多版配文。"""
    topic = topic.strip()
    if not topic:
        raise ValueError("主题不能为空")
    if platform not in PLATFORMS:
        raise ValueError(f"未知平台：{platform}，可选：{list(PLATFORMS)}")

    cfg = PLATFORMS[platform]
    tags = make_hashtags(keywords or [topic], cfg["max_hashtags"])

    captions = []
    for i, tpl in enumerate(cfg["templates"]):
        angle = ANGLES[i % len(ANGLES)]
        body = tpl.format(topic=topic, angle=angle)
        if tags:
            body = body + "\n" + " ".join(tags)
        captions.append(body)
    return captions


def generate_captions_llm(topic: str, platform: str,
                          keywords: list[str] | None = None,
                          api_key: str | None = None,
                          base_url: str | None = None,
                          model: str | None = None) -> list[str]:
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    base_url = (base_url or os.environ.get("OPENAI_BASE_URL")
                or "https://api.openai.com/v1").rstrip("/")
    model = model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    if not api_key:
        raise RuntimeError("未设置 OPENAI_API_KEY")
    kw = "、".join(keywords or [])
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你是社媒文案，按平台风格输出 3 条配文的 JSON 字符串数组，不要解释。"},
            {"role": "user", "content": f"主题：{topic}；平台：{platform}；关键词：{kw}。给出 3 条配文。"},
        ],
        "temperature": 0.8,
    }
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    content = data["choices"][0]["message"]["content"].strip().strip("`")
    if content.startswith("json"):
        content = content[4:].strip()
    return [str(x) for x in json.loads(content)]


def captions(topic: str, platform: str = "x",
             keywords: list[str] | None = None,
             use_llm: bool = False) -> list[str]:
    base = generate_captions(topic, platform, keywords)
    if use_llm and os.environ.get("OPENAI_API_KEY"):
        try:
            return base + generate_captions_llm(topic, platform, keywords)
        except Exception as exc:
            print(f"[warn] LLM 配文失败，使用模板结果：{exc}")
    return base
