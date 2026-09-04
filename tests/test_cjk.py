import unittest
from tg_rich_render.cjk import get_display_width, pad_cjk

class TestCJK(unittest.TestCase):
    def test_get_display_width(self):
        self.assertEqual(get_display_width("hello"), 5)
        self.assertEqual(get_display_width("你好"), 4)
        self.assertEqual(get_display_width("Hello, 世界！"), 13)

    def test_pad_cjk(self):
        # Left alignment
        padded = pad_cjk("测试", 6, align='left')
        self.assertEqual(padded, "测试  ")
        self.assertEqual(get_display_width(padded), 6)

        # Right alignment
        padded_r = pad_cjk("测试", 6, align='right')
        self.assertEqual(padded_r, "  测试")
        self.assertEqual(get_display_width(padded_r), 6)

        # Center alignment
        padded_c = pad_cjk("A", 5, align='center')
        self.assertEqual(padded_c, "  A  ")

if __name__ == '__main__':
    unittest.main()
