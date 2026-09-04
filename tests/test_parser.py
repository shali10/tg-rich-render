import unittest
from tg_rich_render.parser import render_telegram, extract_tables_and_text

DOC = """# 系统巡检报告

以下是当前节点健康度：

| 节点 | CPU | 内存 |
|---|---|---|
| US-East | 14% | 42% |
| HK-01 | 28% | 65% |

```bash
# 这里是普通代码块，不应被误判为表格
| not | a | table |
```

请及时关注高负载节点。
"""

class TestParser(unittest.TestCase):
    def test_extract_tables_and_text(self):
        blocks = extract_tables_and_text(DOC)
        types = [b[0] for b in blocks]
        self.assertIn('table', types)
        self.assertEqual(types.count('table'), 1)

    def test_render_telegram_rounded(self):
        out = render_telegram(DOC, style='rounded')
        self.assertIn("```", out)
        self.assertIn("╭", out)
        self.assertIn("系统巡检报告", out)
        self.assertIn("请及时关注高负载节点", out)

    def test_render_telegram_card(self):
        out = render_telegram(DOC, style='card')
        self.assertIn("📌 US-East", out)
        self.assertIn("• CPU: 14%", out)

if __name__ == '__main__':
    unittest.main()
