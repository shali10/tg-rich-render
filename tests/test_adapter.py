import unittest
from tg_rich_render.adapter import smart_format_payload

MD_SAMPLE = """
| 维度 | 得分 |
|---|---|
| 速度 | 98 |
"""

class TestAdapter(unittest.TestCase):
    def test_smart_format_payload_default():
        payload = smart_format_payload(MD_SAMPLE)
        self.assertIsNone(payload["parse_mode"])
        self.assertIn("╭", payload["text"])
        self.assertIn("```", payload["text"])

    def test_smart_format_payload_html(self):
        payload = smart_format_payload(MD_SAMPLE, prefer_html=True)
        self.assertEqual(payload["parse_mode"], "HTML")
        self.assertIn("<table>", payload["text"])

    def test_smart_format_payload_default(self):
        payload = smart_format_payload(MD_SAMPLE)
        self.assertIsNone(payload["parse_mode"])
        self.assertIn("╭", payload["text"])
        self.assertIn("```", payload["text"])

if __name__ == '__main__':
    unittest.main()
