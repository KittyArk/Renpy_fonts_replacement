import os
import sys
from pathlib import Path

# 从 font_tool 导入通用逻辑
from font_tool import run_mode_scan_directory

def list_fonts(directory, output_file):
    run_mode_scan_directory(directory, output_file)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_dir = sys.argv[1].strip().strip('"\'')
    else:
        user_dir = input("请输入要扫描字体的文件夹路径: ").strip().strip('"\'')

    if not user_dir or not os.path.isdir(user_dir):
        print(f"错误: '{user_dir}' 不是有效文件夹路径")
    else:
        script_dir = Path(__file__).resolve().parent
        output_path = script_dir / "font_list.txt"
        list_fonts(user_dir, output_path)
