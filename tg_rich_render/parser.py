"""Markdown document parser that isolates tables and applies rich Telegram formatting.
"""

import re
from typing import Literal, Optional, List
from tg_rich_render.table import Table

TableStyle = Literal['rounded', 'classic', 'clean', 'card', 'html']

TABLE_LINE_RE = re.compile(r'^\s*\|.*\|\s*$')

def extract_tables_and_text(md_text: str):
    """Split markdown text into ordinary text blocks and table blocks.
    
    Protects existing fenced code blocks from being parsed as tables.
    """
    lines = md_text.splitlines()
    blocks = []
    
    in_code_block = False
    current_text_lines: List[str] = []
    current_table_lines: List[str] = []

    def flush_text():
        nonlocal current_text_lines
        if current_text_lines:
            blocks.append(('text', '\n'.join(current_text_lines)))
            current_text_lines = []

    def flush_table():
        nonlocal current_table_lines
        if current_table_lines:
            raw_table = '\n'.join(current_table_lines)
            t = Table.from_markdown(raw_table)
            if t:
                blocks.append(('table', t))
            else:
                blocks.append(('text', raw_table))
            current_table_lines = []

    for line in lines:
        stripped = line.strip()
        
        # Check code fence
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            if current_table_lines:
                flush_table()
            current_text_lines.append(line)
            continue

        if in_code_block:
            current_text_lines.append(line)
            continue

        # Check if line looks like a markdown table row
        if TABLE_LINE_RE.match(stripped):
            if current_text_lines:
                flush_text()
            current_table_lines.append(line)
        else:
            if current_table_lines:
                flush_table()
            current_text_lines.append(line)

    if current_table_lines:
        flush_table()
    if current_text_lines:
        flush_text()

    return blocks

def render_telegram(
    md_text: str,
    style: TableStyle = 'rounded',
    wrap_in_code_block: bool = True
) -> str:
    """Transform markdown text for optimal Telegram display.
    
    Parameters:
        md_text: Input markdown text containing pipe tables.
        style: Rendering style for tables ('rounded', 'classic', 'clean', 'card', 'html').
        wrap_in_code_block: Wrap monospace tables in ``` for perfect alignment.
    """
    blocks = extract_tables_and_text(md_text)
    output_parts = []

    for kind, payload in blocks:
        if kind == 'text':
            output_parts.append(payload)
        elif kind == 'table':
            table: Table = payload
            if style == 'rounded':
                rendered = table.render_rounded()
                if wrap_in_code_block:
                    rendered = f"```\n{rendered}\n```"
            elif style == 'classic':
                rendered = table.render_classic()
                if wrap_in_code_block:
                    rendered = f"```\n{rendered}\n```"
            elif style == 'clean':
                rendered = table.render_clean()
                if wrap_in_code_block:
                    rendered = f"```\n{rendered}\n```"
            elif style == 'card':
                rendered = table.render_card()
            elif style == 'html':
                rendered = table.render_html()
            else:
                rendered = table.render_rounded()
                if wrap_in_code_block:
                    rendered = f"```\n{rendered}\n```"
            output_parts.append(rendered)

    return "\n".join(output_parts)
