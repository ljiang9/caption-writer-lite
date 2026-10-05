# caption-writer-lite

零依赖的**社媒配文生成器**：给定主题和关键词，按 `x` / `weibo` / `xiaohongshu` / `linkedin` 四种平台风格，一次生成多版配文，并自动按平台规则附加 hashtag。可选接入 LLM 追加更多版本；没有 key 时本地模板已能产出完整配文。

## 功能简介

- 4 种平台风格：X（简短有力）、微博（口语+话题）、小红书（emoji 种草）、LinkedIn（专业克制）。
- 每个平台多套模板，一次出多版供挑选。
- 关键词自动转 `#标签`，按平台限制数量、自动去重。
- 可选 LLM 追加配文。

## 快速开始

```bash
python3 cli.py --topic "早餐机食谱" --platform xiaohongshu --keyword "减脂" --keyword "快手"

python3 cli.py --topic "远程协作" --platform linkedin
```

## 无 API key 如何运行

本项目**默认纯模板运行**，无需任何 key，立即输出多版配文。
仅当你想让 LLM 额外补几条时，才需要：

```bash
export OPENAI_API_KEY=sk-xxx
python3 cli.py --topic "早餐机食谱" --platform weibo --llm
```

## 目录说明

```
caption-writer-lite/
├── caption_writer.py   # 平台模板 + hashtag 规则 + 可选 LLM
├── cli.py            # 命令行入口
├── tests/
│   └── test_caption.py
├── README.md
├── LICENSE
└── .gitignore
```

## 运行测试

```bash
python3 -m unittest discover -s tests
```

## License

MIT License，Copyright (c) 2026 ljiang9。
