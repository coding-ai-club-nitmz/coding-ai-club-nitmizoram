# Copyright (c) 2026 Coding & AI Club, NIT Mizoram. All Rights Reserved.
import unittest
from google_sheets import sanitize_for_sheet

class TestSanitization(unittest.TestCase):
    def test_formula_injection_escaping(self):
        self.assertEqual(sanitize_for_sheet("=SUM(1,2)"), "'=SUM(1,2)")
        self.assertEqual(sanitize_for_sheet("+CMD|' /C calc'!A0"), "'+CMD|' /C calc'!A0")
        self.assertEqual(sanitize_for_sheet("-10+20"), "'-10+20")
        self.assertEqual(sanitize_for_sheet("@EVIL_FUNC()"), "'@EVIL_FUNC()")

    def test_xss_html_tag_stripping(self):
        self.assertEqual(sanitize_for_sheet("<script>alert('xss')</script>"), "alert('xss')")
        self.assertEqual(sanitize_for_sheet("Hello <b>World</b>"), "Hello World")
        self.assertEqual(sanitize_for_sheet("<a href='http://malicious.com'>Link</a>"), "Link")

    def test_normal_clean_text(self):
        self.assertEqual(sanitize_for_sheet("BT24CS028"), "BT24CS028")
        self.assertEqual(sanitize_for_sheet("DILIP SAHU"), "DILIP SAHU")
        self.assertEqual(sanitize_for_sheet(""), "")
        self.assertEqual(sanitize_for_sheet(None), "")

if __name__ == '__main__':
    unittest.main()
