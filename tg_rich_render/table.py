"""Markdown Pipe Table Parser and Multi-style Telegram Renderers.

Supports:
- CJK wide character awareness
- Column alignment (:---, :---:, ---:)
- Multiple visual styles: rounded, classic, clean, card, html
"""

import re
import html
from typing import List, Dict, Any, Optional, Literal
from tg_rich_render.cjk import get_display_width, pad_cjk

Alignment = Literal['left', 'right', 'center']

class Table:
    """Represents a parsed Markdown table."""

    def __init__(self, headers: List[str], rows: List[List[str]], alignments: Optional[List[Alignment]] = None):
        self.headers = [h.strip() for h in headers]
        self.rows = [[cell.strip() for cell in row] for row in rows]
        
        col_count = len(self.headers)
        if not alignments or len(alignments) < col_count:
            alignments = ['left'] * col_count
        self.alignments = alignments[:col_count]

        # Calculate max display width per column
        self.col_widths = [get_display_width(h) for h in self.headers]
        for row in self.rows:
            # Pad row if incomplete
            while len(row) < col_count:
                row.append('')
            for idx in range(col_count):
                cell_w = get_display_width(row[idx])
                if cell_w > self.col_widths[idx]:
                    self.col_widths[idx] = cell_w

    @classmethod
    def from_markdown(cls, table_str: str) -> Optional['Table']:
        """Parse a markdown pipe table string into a Table instance."""
        lines = [line.strip() for line in table_str.strip().splitlines() if line.strip()]
        if len(lines) < 2:
            return None

        # Clean pipe edges
        def split_row(line: str) -> List[str]:
            if line.startswith('|'):
                line = line[1:]
            if line.endswith('|'):
                line = line[:-1]
            return [cell.strip() for cell in line.split('|')]

        raw_header = split_row(lines[0])
        separator_line = split_row(lines[1])

        # Validate separator line has dashes
        alignments: List[Alignment] = []
        for sep in separator_line:
            s = sep.strip()
            if not re.match(r'^:?-+:?$', s):
                return None  # Invalid markdown table separator
            if s.startswith(':') and s.endswith(':'):
                alignments.append('center')
            elif s.endswith(':'):
                alignments.append('right')
            else:
                alignments.append('left')

        rows: List[List[str]] = []
        for line in lines[2:]:
            if '|' in line:
                rows.append(split_row(line))

        return cls(headers=raw_header, rows=rows, alignments=alignments)

    @classmethod
    def from_records(
        cls,
        records: List[Dict[str, Any]],
        headers: Optional[List[str]] = None,
        alignments: Optional[List[Alignment]] = None
    ) -> Optional['Table']:
        """Create a Table instance directly from a list of dictionaries (records).

        Args:
            records: List of dictionaries representing table rows.
            headers: Optional explicit column headers / ordering. If None, uses keys of first record.
            alignments: Optional column alignments ('left', 'center', 'right').
        """
        if not records:
            return None

        if headers is None:
            headers = list(records[0].keys())

        rows = []
        for rec in records:
            row = [str(rec.get(h, '')) for h in headers]
            rows.append(row)

        return cls(headers=headers, rows=rows, alignments=alignments)

    def render_rounded(self) -> str:
        """Render using modern Unicode rounded box characters."""
        widths = self.col_widths
        
        # ╭──────┬──────╮
        top = "╭" + "┬".join("─" * (w + 2) for w in widths) + "╮"
        # ├──────┼──────┤
        mid = "├" + "┼".join("─" * (w + 2) for w in widths) + "┤"
        # ╰──────┴──────╯
        bot = "╰" + "┴".join("─" * (w + 2) for w in widths) + "╯"

        def fmt_row(cells: List[str]) -> str:
            padded = []
            for i, cell in enumerate(cells):
                w = widths[i]
                align = self.alignments[i] if i < len(self.alignments) else 'left'
                padded.append(" " + pad_cjk(cell, w, align=align) + " ")
            return "│" + "│".join(padded) + "│"

        lines = [top, fmt_row(self.headers), mid]
        for row in self.rows:
            lines.append(fmt_row(row))
        lines.append(bot)
        return "\n".join(lines)

    def render_classic(self) -> str:
        """Render using classic ASCII borders."""
        widths = self.col_widths
        sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

        def fmt_row(cells: List[str]) -> str:
            padded = []
            for i, cell in enumerate(cells):
                w = widths[i]
                align = self.alignments[i] if i < len(self.alignments) else 'left'
                padded.append(" " + pad_cjk(cell, w, align=align) + " ")
            return "|" + "|".join(padded) + "|"

        lines = [sep, fmt_row(self.headers), sep]
        for row in self.rows:
            lines.append(fmt_row(row))
        lines.append(sep)
        return "\n".join(lines)

    def render_clean(self) -> str:
        """Render minimalist table without vertical border lines."""
        widths = self.col_widths
        header_pad = [pad_cjk(h, widths[i], align=self.alignments[i]) for i, h in enumerate(self.headers)]
        sep_line = ["─" * widths[i] for i in range(len(widths))]
        
        lines = [" ".join(header_pad), " ".join(sep_line)]
        for row in self.rows:
            row_pad = []
            for i, cell in enumerate(row):
                w = widths[i] if i < len(widths) else len(cell)
                align = self.alignments[i] if i < len(self.alignments) else 'left'
                row_pad.append(pad_cjk(cell, w, align=align))
            lines.append(" ".join(row_pad))
        return "\n".join(lines)

    def render_card(self) -> str:
        """Render table as mobile-friendly cards, ideal for narrow screens."""
        blocks = []
        for row_idx, row in enumerate(self.rows):
            title = row[0] if row else f"Item {row_idx + 1}"
            details = []
            for col_idx in range(1, len(self.headers)):
                h = self.headers[col_idx]
                val = row[col_idx] if col_idx < len(row) else ""
                if val:
                    details.append(f"  • {h}: {val}")
            if details:
                blocks.append(f"📌 {title}\n" + "\n".join(details))
            else:
                blocks.append(f"📌 {title}")
        return "\n\n".join(blocks)

    def render_html(self) -> str:
        """Render as Telegram-compatible HTML table or styled blocks."""
        out = ["<table>"]
        out.append("  <thead>")
        out.append("    <tr>" + "".join(f"<th>{html.escape(h)}</th>" for h in self.headers) + "</tr>")
        out.append("  </thead>")
        out.append("  <tbody>")
        for row in self.rows:
            out.append("    <tr>" + "".join(f"<td>{html.escape(cell)}</td>" for cell in row) + "</tr>")
        out.append("  </tbody>")
        out.append("</table>")
        return "\n".join(out)
