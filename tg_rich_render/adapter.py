"""Adapters and helper bindings for aiogram 3 and python-telegram-bot.
"""

from typing import Any, Optional, Dict, Literal
from tg_rich_render.parser import render_telegram, TableStyle

def smart_format_payload(
    text: str,
    prefer_html: bool = False,
    table_style: TableStyle = 'rounded'
) -> Dict[str, Any]:
    """Prepare payload dictionary with formatted text and appropriate parse_mode."""
    if prefer_html:
        formatted = render_telegram(text, style='html')
        return {
            "text": formatted,
            "parse_mode": "HTML"
        }
    else:
        formatted = render_telegram(text, style=table_style, wrap_in_code_block=True)
        return {
            "text": formatted,
            "parse_mode": None  # Plain/Markdown compatible
        }

async def send_smart_message(
    bot: Any,
    chat_id: Any,
    text: str,
    table_style: TableStyle = 'rounded',
    **kwargs
) -> Any:
    """Send a message through aiogram 3 or python-telegram-bot with auto-formatted rich tables.
    
    Compatible with:
    - aiogram 3.x (Bot instance)
    - python-telegram-bot 20+ (Bot or ExtBot instance)
    """
    payload = smart_format_payload(text, table_style=table_style)
    send_kwargs = {**payload, **kwargs}

    # aiogram 3.x
    if hasattr(bot, 'send_message') and callable(getattr(bot, 'send_message')):
        return await bot.send_message(chat_id=chat_id, **send_kwargs)
    
    # python-telegram-bot
    elif hasattr(bot, 'send_message'):
        return await bot.send_message(chat_id=chat_id, **send_kwargs)
    
    raise TypeError(f"Unsupported bot instance type: {type(bot)}")
