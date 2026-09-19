import os
import re
import sys
from pathlib import Path

# 正则表达式匹配：
# 1. 引号包围的字体文件路径 ("fonts/xxx.ttf" 或 'fonts/xxx.otf')
# 2. Ren'Py {font=...} 标签 ({font=fonts/xxx.ttf} 或 {font="fonts/xxx.ttf"})
FONT_PATTERN = re.compile(
    r'''(?x)
    ["']([^"']+\.(?:otf|ttf|ttc|otc))["']
    |
    \{font=\s*["']?([^"'\}]+\.(?:otf|ttf|ttc|otc))["']?\}
    ''',
    re.IGNORECASE
)

def extract_fonts_from_rpy(source_dir, output_file):
    """
    扫描源目录中的 .rpy 文件并提取引用的字体文件路径。
    """
    source_dir = Path(source_dir).resolve()
    fonts = set()
    scanned_files = 0

    # 遍历目录
    for root, dirs, files in os.walk(source_dir):
        # 排除 Ren'Py 翻译文件夹 "tl"（精准匹配文件夹名为 "tl"）
        dirs[:] = [d for d in dirs if d.lower() != "tl"]

        for file in files:
            if file.lower().endswith('.rpy'):
                file_path = os.path.join(root, file)
                scanned_files += 1
                try:
                    # 优先使用 utf-8 读取，捕获解码失败时退回 utf-8-sig 或 errors='replace'
                    content = None
                    for encoding in ('utf-8', 'utf-8-sig', 'gbk', 'gb2312'):
                        try:
                            with open(file_path, 'r', encoding=encoding) as f:
                                content = f.read()
                            break
                        except (UnicodeDecodeError, Exception):
                            continue

                    if content is None:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()

                    # 查找所有匹配的字体路径
                    matches = FONT_PATTERN.findall(content)
                    for m1, m2 in matches:
                        font = m1 or m2
                        if font:
                            # 统一路径分隔符为正斜杠 '/'，去除首尾空白
                            clean_font = font.strip().replace('\\', '/')
                            # 移除可能残留的 font= 前缀
                            clean_font = re.sub(r'^font=\s*', '', clean_font, flags=re.IGNORECASE)
                            fonts.add(clean_font)
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")

    # 创建输出的 .rpy 文件
    try:
        output_file_path = Path(output_file)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write('# 由 extract_fonts.py 自动生成的游戏内字体列表\n')
            f.write('define game_fonts = [\n')
            for font in sorted(fonts):
                f.write(f'    "{font}",\n')
            f.write(']\n')

        print(f"扫描了 {scanned_files} 个 .rpy 文件。")
        print(f"成功提取 {len(fonts)} 个唯一字体到 {output_file_path.name}")
    except Exception as e:
        print(f"创建输出文件 {output_file} 时出错: {e}")

if __name__ == "__main__":
    # 获取源文件夹路径（优先支持命令行参数，无参数时使用 input）
    if len(sys.argv) > 1:
        source_directory = sys.argv[1].strip().strip('"\'')
    else:
        source_directory = input("请输入要扫描的文件夹路径: ").strip().strip('"\'')

    # 输出文件为脚本所在目录的 fonts_output.rpy
    script_dir = Path(__file__).resolve().parent
    output_rpy = script_dir / "fonts_output.rpy"

    # 确保源文件夹路径有效
    if not source_directory or not os.path.isdir(source_directory):
        print(f"错误: '{source_directory}' 不是有效文件夹路径")
    else:
        extract_fonts_from_rpy(source_directory, output_rpy)
