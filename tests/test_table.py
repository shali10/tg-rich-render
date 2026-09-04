import unittest
from tg_rich_render.table import Table

RAW_TABLE = """
| 服务 | 状态 | 延迟 |
|:---|:---:|---:|
| API 网关 | 运行中 | 12ms |
| 数据库 | 正常 | 2ms |
"""

class TestTable(unittest.TestCase):
    def test_table_parsing(self):
        table = Table.from_markdown(RAW_TABLE)
        self.assertIsNotNone(table)
        self.assertEqual(table.headers, ["服务", "状态", "延迟"])
        self.assertEqual(len(table.rows), 2)
        self.assertEqual(table.alignments, ["left", "center", "right"])

    def test_table_render_rounded(self):
        table = Table.from_markdown(RAW_TABLE)
        rendered = table.render_rounded()
        self.assertIn("╭", rendered)
        self.assertIn("╰", rendered)
        self.assertIn("API 网关", rendered)

    def test_table_render_classic(self):
        table = Table.from_markdown(RAW_TABLE)
        rendered = table.render_classic()
        self.assertIn("+", rendered)
        self.assertIn("|", rendered)

    def test_table_render_clean(self):
        table = Table.from_markdown(RAW_TABLE)
        rendered = table.render_clean()
        self.assertIn("─", rendered)
        self.assertIn("API 网关", rendered)

    def test_table_render_card(self):
        table = Table.from_markdown(RAW_TABLE)
        rendered = table.render_card()
        self.assertIn("📌 API 网关", rendered)
        self.assertIn("• 状态: 运行中", rendered)

    def test_table_render_html(self):
        table = Table.from_markdown(RAW_TABLE)
        rendered = table.render_html()
        self.assertIn("<table>", rendered)
        self.assertIn("<th>服务</th>", rendered)

if __name__ == '__main__':
    unittest.main()
