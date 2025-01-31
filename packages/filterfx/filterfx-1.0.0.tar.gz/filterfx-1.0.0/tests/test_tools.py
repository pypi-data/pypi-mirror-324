import unittest
from filterfx.tools import *

class TestToolFilters(unittest.TestCase):
    def test_ensure_rgb_already_rgb(self):
        img = Img.new("RGB", (100, 100), color="red")
        result = ensure_rgb(img)
        self.assertEqual(result.mode, "RGB")

    def test_ensure_rgb_convert_to_rgb(self):
        img = Img.new("L", (100, 100), color="white")
        result = ensure_rgb(img)
        self.assertEqual(result.mode, "RGB")
        