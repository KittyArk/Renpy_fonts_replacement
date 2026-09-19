import os
import shutil
import tempfile
import unittest
from pathlib import Path

from extract_fonts import extract_fonts_from_rpy
from list_fonts import list_fonts

class TestRenpyFontTools(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.script_dir = Path(__file__).resolve().parent

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_extract_fonts(self):
        # Create dummy structure
        game_dir = Path(self.test_dir) / "game"
        game_dir.mkdir()

        # Subdirectory with 'tl' in folder name (should not be excluded unless it is exact 'tl')
        castle_dir = game_dir / "castle"
        castle_dir.mkdir()

        tl_dir = game_dir / "tl"
        tl_dir.mkdir()

        # RPY file in game_dir
        gui_rpy = game_dir / "gui.rpy"
        gui_rpy.write_text(
            'define gui.text_font = "fonts/custom.ttf"\n'
            'define gui.name_font = "fonts/name.otf"\n'
            'label start:\n'
            '    "Hello {font=fonts/dialog.ttc}world{/font}"\n',
            encoding="utf-8"
        )

        # RPY file in castle_dir
        castle_rpy = castle_dir / "castle.rpy"
        castle_rpy.write_text(
            'define gui.castle_font = "fonts/castle.otc"\n',
            encoding="utf-8"
        )

        # RPY file in tl_dir (should be ignored)
        tl_rpy = tl_dir / "ignored.rpy"
        tl_rpy.write_text(
            'define gui.tl_font = "fonts/ignored.ttf"\n',
            encoding="utf-8"
        )

        output_file = Path(self.test_dir) / "fonts_output.rpy"
        extract_fonts_from_rpy(game_dir, output_file)

        content = output_file.read_text(encoding="utf-8")
        self.assertIn('"fonts/castle.otc"', content)
        self.assertIn('"fonts/custom.ttf"', content)
        self.assertIn('"fonts/dialog.ttc"', content)
        self.assertIn('"fonts/name.otf"', content)
        self.assertNotIn('"fonts/ignored.ttf"', content)

    def test_list_fonts(self):
        fonts_dir = Path(self.test_dir) / "my_fonts"
        fonts_dir.mkdir()
        sub_dir = fonts_dir / "subfolder"
        sub_dir.mkdir()
        tl_dir = fonts_dir / "tl"
        tl_dir.mkdir()

        (fonts_dir / "a.ttf").touch()
        (sub_dir / "b.otf").touch()
        (tl_dir / "c.ttf").touch()

        output_file = Path(self.test_dir) / "font_list.txt"
        list_fonts(fonts_dir, output_file)

        content = output_file.read_text(encoding="utf-8")
        self.assertIn('"a.ttf"', content)
        self.assertIn('"subfolder/b.otf"', content)
        self.assertNotIn('c.ttf', content)

if __name__ == "__main__":
    unittest.main()
