import os
import sys
from pathlib import Path

# 支持的字体文件扩展名
FONT_EXTENSIONS = ('.otf', '.ttf', '.ttc', '.otc')

def list_fonts(directory, output_file):
    """
    扫描指定目录中的所有字体文件，并记录其相对路径。
    """
    directory = Path(directory).resolve()
    font_files = []

    # 遍历目录
    for root, dirs, files in os.walk(directory):
        # 排除 Ren'Py 翻译文件夹 "tl"
        dirs[:] = [d for d in dirs if d.lower() != "tl"]

        for file in files:
            if file.lower().endswith(FONT_EXTENSIONS):
                # 获取相对于输入目录的路径
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, directory)
                # 统一转为正斜杠 '/' 路径分隔符
                normalized_path = relative_path.replace('\\', '/')
                font_files.append(normalized_path)

    # 将结果按字母顺序写入输出文件
    output_path = Path(output_file)
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# 扫描到的字体文件列表\n")
            f.write("define game_fonts = [\n")
            for font in sorted(font_files):
                f.write(f'    "{font}",\n')
            f.write("]\n")

        print(f"在目录 '{directory}' 中找到 {len(font_files)} 个字体文件。")
        print(f"结果已保存至 {output_path.name}")
    except Exception as e:
        print(f"保存文件时出错 {output_path}: {e}")

if __name__ == "__main__":
    # 获取目录路径（优先支持命令行参数，无参数时使用 input）
    if len(sys.argv) > 1:
        user_dir = sys.argv[1].strip().strip('"\'')
    else:
        user_dir = input("请输入要扫描字体的文件夹路径: ").strip().strip('"\'')

    # 验证目录是否存在
    if not user_dir or not os.path.isdir(user_dir):
        print(f"错误: '{user_dir}' 不是有效的文件夹路径")
    else:
        # 设置输出文件路径为脚本所在目录下的 font_list.txt
        script_dir = Path(__file__).resolve().parent
        output_path = script_dir / "font_list.txt"
        list_fonts(user_dir, output_path)
