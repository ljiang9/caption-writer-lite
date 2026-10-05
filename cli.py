"""caption-writer-lite 命令行入口。

用法示例：
    python3 cli.py --topic "早餐机食谱" --platform xiaohongshu --keyword "减脂" --keyword "快手"
    python3 cli.py --topic "远程协作" --platform linkedin
"""

from __future__ import annotations

import argparse
import sys

from caption_writer import PLATFORMS, captions


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="caption-writer-lite",
        description="按主题/平台风格生成多版社媒配文（含 hashtag，可选 LLM）",
    )
    p.add_argument("--topic", required=True, help="配文主题")
    p.add_argument("--platform", default="x", choices=list(PLATFORMS),
                   help="平台风格，默认 x")
    p.add_argument("--keyword", action="append", default=[], help="关键词，会转为 hashtag，可重复")
    p.add_argument("--llm", action="store_true", help="追加 LLM 配文（需 OPENAI_API_KEY）")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = captions(args.topic, args.platform, args.keyword, use_llm=args.llm)
    for i, c in enumerate(result, 1):
        print(f"--- 版本 {i} [{args.platform}] ---")
        print(c)
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
