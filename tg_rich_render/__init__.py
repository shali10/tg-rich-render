"""tg-rich-render: Lightweight Telegram rich table and format converter.

Solves the common pain point of ugly, misaligned tables in Telegram bots.
Provides zero-dependency CJK alignment and multi-style table formatting.
"""

from tg_rich_render.cjk import get_display_width, pad_cjk
from tg_rich_render.table import Table
from tg_rich_render.parser import render_telegram, extract_tables_and_text, TableStyle
from tg_rich_render.adapter import smart_format_payload, send_smart_message

__version__ = "0.1.0"
__all__ = [
    "Table",
    "TableStyle",
    "get_display_width",
    "pad_cjk",
    "render_telegram",
    "extract_tables_and_text",
    "smart_format_payload",
    "send_smart_message",
]
