# 1. 运行 extract_fonts.py 以获取原游戏字体列表
define game_fonts = [
    # 在此列出需要替换的原游戏字体文件路径
    # 例如: "fonts/old_font.ttf",
    "xxx.ttf",
    "fonts/xxx.ttf",
]

# 2. 手动设置对应的替换字体（常规体/Regular），顺序需与 game_fonts 一一对应
define replacement_fonts = [
    # 在此列出替换的新字体文件路径
    # 例如: "tl/Chinese/fonts/new_font.ttf",
    "tl/Chinese/fonts/xxx_regular.ttf",
]

# 3. 粗体替换列表（可选）
# 如果某个字体没有专门的粗体文件，可填 None 或置空 []
# 对应位置填 None 时，Ren'Py 会尝试算法加粗或退回常规字体
define replacement_bold_fonts = [
    # "tl/Chinese/fonts/xxx_bold.ttf",
    # None,
]

# 4. 斜体替换列表（可选）
define replacement_italic_fonts = [
    # "tl/Chinese/fonts/xxx_italic.ttf",
    # None,
]

# 5. 粗斜体替换列表（可选）
# 当文本同时应用了 {b} 和 {i} 标签时使用
define replacement_bold_italic_fonts = [
    # "tl/Chinese/fonts/xxx_bold_italic.ttf",
    # None,
]

# 字体替换逻辑
init python:
    def apply_font_replacement():
        # 检查基础字体列表长度一致性
        if len(game_fonts) != len(replacement_fonts):
            raise Exception(f"[Font Replacement Error] game_fonts length ({len(game_fonts)}) != replacement_fonts length ({len(replacement_fonts)})")

        # 安全获取可选样式列表
        bold_list = replacement_bold_fonts if 'replacement_bold_fonts' in globals() and replacement_bold_fonts else []
        italic_list = replacement_italic_fonts if 'replacement_italic_fonts' in globals() and replacement_italic_fonts else []
        bold_italic_list = replacement_bold_italic_fonts if 'replacement_bold_italic_fonts' in globals() and replacement_bold_italic_fonts else []

        # 重置字体替换映射
        config.font_replacement_map = {}

        # 遍历游戏字体列表进行映射
        for index, old_font in enumerate(game_fonts):
            new_font = replacement_fonts[index]

            # --- 1. 常规字体映射 (Regular) ---
            config.font_replacement_map[old_font, False, False] = (new_font, False, False)

            # --- 2. 粗体映射 (Bold) ---
            if index < len(bold_list) and bold_list[index] is not None:
                config.font_replacement_map[old_font, True, False] = (bold_list[index], False, False)

            # --- 3. 斜体映射 (Italic) ---
            if index < len(italic_list) and italic_list[index] is not None:
                config.font_replacement_map[old_font, False, True] = (italic_list[index], False, False)

            # --- 4. 粗斜体映射 (Bold Italic) ---
            if index < len(bold_italic_list) and bold_italic_list[index] is not None:
                config.font_replacement_map[old_font, True, True] = (bold_italic_list[index], False, False)

        # 调试输出替换信息
        print("--- Font Replacement Applied ---")
        for key, value in config.font_replacement_map.items():
            styles = []
            if key[1]: styles.append("Bold")
            if key[2]: styles.append("Italic")
            style_name = " + ".join(styles) if styles else "Regular"
            print(f"Replace [{style_name}]: {key[0]} -> {value[0]}")

# 仅在切换至目标语言（如 Chinese / simplified_chinese）时应用替换
# 请根据项目实际语言名称修改 "Chinese"
translate Chinese python:
    apply_font_replacement()

# 切换回默认语言（None）时清空替换映射
translate None python:
    config.font_replacement_map = {}
