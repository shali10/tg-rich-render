"""Command Line Interface for tg-rich-render."""

import sys
import argparse
from pathlib import Path
from tg_rich_render.parser import render_telegram

def main():
    parser = argparse.ArgumentParser(
        description="Transform Markdown tables into Telegram-optimized rich formats."
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Markdown file to read (reads stdin if omitted)"
    )
    parser.add_argument(
        "--style",
        choices=["rounded", "classic", "clean", "card", "html"],
        default="rounded",
        help="Table rendering style (default: rounded)"
    )
    parser.add_argument(
        "--no-wrap",
        action="store_true",
        help="Do not wrap rendered tables in code blocks"
    )

    args = parser.parse_args()

    if args.file and args.file != "-":
        content = Path(args.file).read_text(encoding="utf-8")
    else:
        content = sys.stdin.read()

    rendered = render_telegram(
        content,
        style=args.style,
        wrap_in_code_block=not args.no_wrap
    )
    print(rendered)

if __name__ == "__main__":
    main()
