"""CJK and wide-character display width utilities.

Ensures perfect column alignment for Chinese, Japanese, Korean,
full-width punctuation, and emoji in Telegram monospace contexts.
"""

import unicodedata
from typing import Literal

def get_char_width(ch: str) -> int:
    """Return the display column width of a single unicode character."""
    # Control characters
    if unicodedata.category(ch).startswith('C'):
        return 0
    # East Asian Width property
    # W: Wide, F: Fullwidth -> 2 columns
    # A: Ambiguous -> usually 1 column in modern monospace fonts
    # Na: Narrow, N: Neutral, H: Halfwidth -> 1 column
    status = unicodedata.east_asian_width(ch)
    if status in ('W', 'F'):
        return 2
    return 1

def get_display_width(text: str) -> int:
    """Calculate the total display width of a string in monospace columns."""
    return sum(get_char_width(ch) for ch in text)

def pad_cjk(text: str, width: int, align: Literal['left', 'right', 'center'] = 'left') -> str:
    """Pad a string containing CJK characters to the specified display width."""
    current_width = get_display_width(text)
    if current_width >= width:
        return text
    
    pad_needed = width - current_width
    if align == 'right':
        return ' ' * pad_needed + text
    elif align == 'center':
        left_pad = pad_needed // 2
        right_pad = pad_needed - left_pad
        return ' ' * left_pad + text + ' ' * right_pad
    else:  # left
        return text + ' ' * pad_needed
