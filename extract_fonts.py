import os
import sys
from pathlib import Path

# 从 font_tool 导入通用逻辑
from font_tool import run_mode_extract_rpy

def extract_fonts_from_rpy(source_dir, output_file):
    run_mode_extract_rpy(source_dir, output_file)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        source_directory = sys.argv[1].strip().strip('"\'')
    else:
        source_directory = input("请输入要扫描的文件夹路径: ").strip().strip('"\'')

    script_dir = Path(__file__).resolve().parent
    output_rpy = script_dir / "fonts_output.rpy"

    if not source_directory or not os.path.isdir(source_directory):
        print(f"错误: '{source_directory}' 不是有效文件夹路径")
    else:
        extract_fonts_from_rpy(source_directory, output_rpy)
