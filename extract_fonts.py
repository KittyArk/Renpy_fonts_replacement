import os
import re
from pathlib import Path

def extract_fonts_from_rpy(source_dir, output_file):
    # 存储唯一字体路径
    fonts = set()
    
    # 正则表达式匹配双引号、单引号或大括号中的 .otf 或 .ttf 文件路径
    pattern = r'(?:"([^"]*\.(?:otf|ttf))"|\'([^\']*\.(?:otf|ttf))\')|(?:\{([^\}]*\.(?:otf|ttf))\})'
    
    # 遍历目录
    for root, dirs, files in os.walk(source_dir):
        # 排除包含"tl"的子文件夹
        dirs[:] = [d for d in dirs if "tl" not in d.lower()]
        
        for file in files:
            if file.endswith('.rpy'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # 查找所有匹配的字体路径
                        matches = re.findall(pattern, content)
                        # 提取非空匹配并去除 font= 前缀
                        for match in matches:
                            # 匹配结果是 (double_quote_match, single_quote_match, brace_match)
                            # 取第一个非空字符串
                            font = next((m for m in match if m), None)
                            if font:
                                # 去除 font= 前缀
                                clean_font = re.sub(r'^font=', '', font)
                                fonts.add(clean_font)
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")
    
    # 创建新的 .rpy 文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('define game_fonts = [\n')
            for font in sorted(fonts):
                f.write(f'    "{font}",\n')
            f.write(']\n')
        
        print(f"成功提取 {len(fonts)} 个唯一字体到 {output_file}")
    except Exception as e:
        print(f"创建输出文件 {output_file} 时出错: {e}")

if __name__ == "__main__":
    # 用户指定的源文件夹
    source_directory = input("请输入要扫描的文件夹路径: ")
    
    # 输出文件为脚本所在目录的 fonts_output.rpy
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_rpy = os.path.join(script_dir, "fonts_output.rpy")
    
    # 确保源文件夹路径有效
    if not os.path.isdir(source_directory):
        print(f"错误: {source_directory} 不是有效文件夹路径")
    else:
        extract_fonts_from_rpy(source_directory, output_rpy)
