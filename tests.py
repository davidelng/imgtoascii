import unittest
from imgtoascii import AsciiArt
from PIL import Image
from shutil import get_terminal_size


class Tests(unittest.TestCase):
    def test_open_img(self):
        img = AsciiArt('media/rick.jpg')
        self.assertIsInstance(img._img, Image.Image)
        img._img.close()

    def test_open_img_fail(self):
        with self.assertRaises(FileNotFoundError):
            img = AsciiArt('media/none.jpg')

    def test_resize(self):
        img = AsciiArt('media/rick.jpg')
        img = img._resize(80)
        self.assertEqual(img.size[0], 40)
        img.close()

    def test_resize_terminal(self):
        img = AsciiArt('media/rick.jpg')
        img = img._resize(999, True)
        t_width, t_height = get_terminal_size()
        self.assertEqual(img.size[0], t_width//2)
        img.close()

    def test_get_brightness_char(self):
        img = AsciiArt('media/rick.jpg')
        char = img._get_brightness_char(255)
        self.assertEqual(char, "@@")
        img._img.close()

    def test_get_brightness_char_empty(self):
        img = AsciiArt('media/rick.jpg')
        char = img._get_brightness_char(0)
        self.assertEqual(char, "  ")
        img._img.close()

    def test_ansi_string(self):
        img = AsciiArt('media/rick.jpg')
        char = img._get_ansi_color("@@", 255, 255, 255)
        self.assertEqual(char, "\x1b[38;2;255;255;255m@@\x1b[0m")
        img._img.close()

    def test_get_ascii_string(self):
        img = AsciiArt('media/rick.jpg')
        cols = 120
        resized = img._resize(cols)
        ascii_string = img._get_ascii_string(cols)
        rows = ascii_string.splitlines()
        printed_rows = len(rows)
        printed_cols = len(rows[0])
        self.assertEqual(printed_cols, cols)
        self.assertEqual(printed_rows, resized.size[1])
        img._img.close()

    def test_get_chars_string(self):
        img = AsciiArt('media/rick.jpg')
        cols = 120
        chars = "#"
        ascii_string = img._get_chars_string(cols, chars)
        rows = ascii_string.splitlines()
        self.assertEqual(chars in ascii_string, True)
        img._img.close()


if __name__ == "__main__":
    unittest.main()