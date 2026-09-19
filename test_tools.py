import os
import shutil
import tempfile
import unittest
from pathlib import Path

from font_tool import (
    run_mode_extract_rpy,
    run_mode_scan_directory,
    run_mode_hybrid,
    is_renpy_builtin,
)

class TestFontTool(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_mode_extract_rpy(self):
        game_dir = Path(self.test_dir) / "game"
        game_dir.mkdir()
        gui_rpy = game_dir / "gui.rpy"
        gui_rpy.write_text(
            'define gui.text_font = "fonts/custom.ttf"\n'
            'define gui.name_font = "DejaVuSans.ttf"\n',
            encoding="utf-8"
        )

        output_file = Path(self.test_dir) / "fonts_output.rpy"
        run_mode_extract_rpy(game_dir, output_file)

        content = output_file.read_text(encoding="utf-8")
        self.assertIn('"fonts/custom.ttf"', content)
        self.assertIn('"DejaVuSans.ttf"', content)

    def test_mode_scan_directory(self):
        fonts_dir = Path(self.test_dir) / "my_fonts"
        fonts_dir.mkdir()
        (fonts_dir / "a.ttf").touch()

        output_file = Path(self.test_dir) / "font_list.txt"
        run_mode_scan_directory(fonts_dir, output_file)

        content = output_file.read_text(encoding="utf-8")
        self.assertIn('"a.ttf"', content)

    def test_mode_hybrid(self):
        game_dir = Path(self.test_dir) / "game"
        game_dir.mkdir()
        fonts_subdir = game_dir / "gui" / "fonts"
        fonts_subdir.mkdir(parents=True)

        # Physical font in subfolder game/gui/fonts/Inter-Regular.ttf
        (fonts_subdir / "Inter-Regular.ttf").touch()
        # Physical font in game/fonts/existing.ttf
        (game_dir / "fonts").mkdir()
        (game_dir / "fonts" / "existing.ttf").touch()

        # RPY file referencing:
        # 1) "Inter-Regular.ttf" (referenced without full path, but exists in gui/fonts/Inter-Regular.ttf)
        # 2) "fonts/existing.ttf" (exact relative path)
        # 3) "fonts/missing.ttf" (truly non-existent font)
        # 4) "DejaVuSans.ttf" (Ren'Py built-in font)
        gui_rpy = game_dir / "gui.rpy"
        gui_rpy.write_text(
            'define gui.font1 = "Inter-Regular.ttf"\n'
            'define gui.font2 = "fonts/existing.ttf"\n'
            'define gui.font3 = "fonts/missing.ttf"\n'
            'define gui.font4 = "DejaVuSans.ttf"\n',
            encoding="utf-8"
        )

        output_file = Path(self.test_dir) / "fonts_output.rpy"
        run_mode_hybrid(game_dir, output_file)

        content = output_file.read_text(encoding="utf-8")
        self.assertIn('"Inter-Regular.ttf"', content)
        self.assertIn('"fonts/existing.ttf"', content)
        self.assertIn('"DejaVuSans.ttf"', content)
        self.assertNotIn('"fonts/missing.ttf"', content)

    def test_is_renpy_builtin(self):
        self.assertTrue(is_renpy_builtin("DejaVuSans.ttf"))
        self.assertTrue(is_renpy_builtin("fonts/DejaVuSans-Bold.ttf"))
        self.assertFalse(is_renpy_builtin("fonts/custom.ttf"))

if __name__ == "__main__":
    unittest.main()
