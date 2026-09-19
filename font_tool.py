import os
import re
import sys
from pathlib import Path

# 支持的字体文件扩展名
FONT_EXTENSIONS = ('.otf', '.ttf', '.ttc', '.otc')

# Ren'Py 框架常见自带内建字体（文件名小写）
RENPY_BUILTIN_FONTS = {
    'dejavusans.ttf',
    'dejavusans-bold.ttf',
    'dejavusans-oblique.ttf',
    'dejavusans-boldoblique.ttf',
    'roboto-regular.ttf',
    'sourcehansans-light.otf',
}

# 正则表达式匹配 rpy 中的字体路径
FONT_PATTERN = re.compile(
    r'''(?x)
    ["']([^"']+\.(?:otf|ttf|ttc|otc))["']
    |
    \{font=\s*["']?([^"'\}]+\.(?:otf|ttf|ttc|otc))["']?\}
    ''',
    re.IGNORECASE
)

def is_renpy_builtin(font_path):
    """判断字体是否为 Ren'Py 自带内建字体"""
    filename = Path(font_path).name.lower()
    return filename in RENPY_BUILTIN_FONTS

def scan_rpy_fonts(source_dir):
    """从源目录中的 .rpy 文件提取字体路径列表"""
    source_dir = Path(source_dir).resolve()
    fonts = set()
    scanned_files = 0

    for root, dirs, files in os.walk(source_dir):
        # 排除 Ren'Py 翻译文件夹 "tl"
        dirs[:] = [d for d in dirs if d.lower() != "tl"]

        for file in files:
            if file.lower().endswith('.rpy'):
                file_path = os.path.join(root, file)
                scanned_files += 1
                try:
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

                    matches = FONT_PATTERN.findall(content)
                    for m1, m2 in matches:
                        font = m1 or m2
                        if font:
                            clean_font = font.strip().replace('\\', '/')
                            clean_font = re.sub(r'^font=\s*', '', clean_font, flags=re.IGNORECASE)
                            fonts.add(clean_font)
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")

    print(f"扫描了 {scanned_files} 个 .rpy 文件。")
    return fonts

def scan_directory_fonts(source_dir):
    """扫描指定目录下的实体字体文件相对路径"""
    source_dir = Path(source_dir).resolve()
    font_files = set()

    for root, dirs, files in os.walk(source_dir):
        dirs[:] = [d for d in dirs if d.lower() != "tl"]

        for file in files:
            if file.lower().endswith(FONT_EXTENSIONS):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, source_dir)
                normalized_path = relative_path.replace('\\', '/')
                font_files.add(normalized_path)

    return font_files

def save_fonts_to_rpy(fonts, output_file, header_comment=""):
    """保存字体集合到 .rpy 文件"""
    output_path = Path(output_file)
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            if header_comment:
                f.write(f"# {header_comment}\n")
            f.write("define game_fonts = [\n")
            for font in sorted(fonts):
                f.write(f'    "{font}",\n')
            f.write("]\n")
        print(f"成功导出 {len(fonts)} 个字体到 {output_path.name}")
    except Exception as e:
        print(f"保存文件 {output_path} 时出错: {e}")

def run_mode_extract_rpy(source_dir, output_file):
    """模式 1：仅提取 .rpy 中的字体"""
    fonts = scan_rpy_fonts(source_dir)
    save_fonts_to_rpy(fonts, output_file, "由 rpy 提取模式生成的字体列表")

def run_mode_scan_directory(source_dir, output_file):
    """模式 2：仅扫描文件夹中的字体文件"""
    fonts = scan_directory_fonts(source_dir)
    print(f"在目录中找到 {len(fonts)} 个字体文件。")
    save_fonts_to_rpy(fonts, output_file, "由目录扫描模式生成的字体列表")

def run_mode_hybrid(source_dir, output_file):
    """模式 3：混合模式 - 提取 rpy 字体并根据实际文件过滤不存在的字体（无视 renpy 自带字体）"""
    source_dir = Path(source_dir).resolve()
    rpy_fonts = scan_rpy_fonts(source_dir)
    physical_fonts = scan_directory_fonts(source_dir)

    # 建立不区分大小写的路径映射与纯文件名映射，适配 Ren'Py 自动寻找子目录字体的特性
    physical_fonts_lower = {f.lower(): f for f in physical_fonts}
    physical_basenames_lower = {Path(f).name.lower(): f for f in physical_fonts}

    filtered_fonts = set()
    removed_count = 0

    for font in rpy_fonts:
        clean_font = font.lstrip('./').replace('\\', '/')
        font_path_abs = source_dir / clean_font
        font_basename = Path(clean_font).name.lower()

        # 校验逻辑：
        # 1. 绝对路径存在于磁盘
        # 2. 相对路径完全匹配（忽略大小写）
        # 3. 后缀相对路径匹配（如 rpy 为 'Inter.ttf'，实体为 'gui/fonts/Inter.ttf'）
        # 4. 纯文件名在扫描出的实体字体库中匹配（适配 Ren'Py 在子目录中自动寻址字体）
        # 5. 属于 Ren'Py 默认内建字体
        exists_in_dir = (
            font_path_abs.is_file()
            or clean_font.lower() in physical_fonts_lower
            or any(pf.endswith('/' + clean_font.lower()) for pf in physical_fonts_lower)
            or font_basename in physical_basenames_lower
        )

        if exists_in_dir or is_renpy_builtin(clean_font):
            filtered_fonts.add(font)
        else:
            print(f"[混合模式] 移除不存在的字体: {font}")
            removed_count += 1

    print(f"混合模式完成：从 {len(rpy_fonts)} 个引用中过滤掉 {removed_count} 个不存在的字体。")
    save_fonts_to_rpy(filtered_fonts, output_file, "由混合模式生成的字体列表（已过滤非内建且不存在的字体）")

def main():
    script_dir = Path(__file__).resolve().parent

    print("=== Ren'Py 字体处理工具 ===")
    print("1. 仅提取 .rpy 中的字体")
    print("2. 仅扫描文件夹中的字体文件")
    print("3. 混合模式（提取 .rpy 字体并校验实体文件，自动移除不存在的字体，无视 Ren'Py 自带字体）")

    if len(sys.argv) > 1:
        mode_input = sys.argv[1].strip()
    else:
        mode_input = input("请选择运行模式 (1/2/3, 默认为 3): ").strip() or "3"

    if len(sys.argv) > 2:
        source_directory = sys.argv[2].strip().strip('"\'')
    else:
        source_directory = input("请输入要扫描的文件夹路径: ").strip().strip('"\'')

    if not source_directory or not os.path.isdir(source_directory):
        print(f"错误: '{source_directory}' 不是有效文件夹路径")
        return

    if mode_input == "1":
        output_file = script_dir / "fonts_output.rpy"
        run_mode_extract_rpy(source_directory, output_file)
    elif mode_input == "2":
        output_file = script_dir / "font_list.txt"
        run_mode_scan_directory(source_directory, output_file)
    elif mode_input == "3":
        output_file = script_dir / "fonts_output.rpy"
        run_mode_hybrid(source_directory, output_file)
    else:
        print("无效模式选择！")

if __name__ == "__main__":
    main()
