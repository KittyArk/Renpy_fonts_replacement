# 1. 运行 extract_fonts.py 以获取原游戏字体列表
define game_fonts = [
    # 在此列出需要替换的原游戏字体文件路径
    # 例如: "fonts/old_font.ttf",
    "xxx.ttf",
    "fonts/xxx.ttf",
]

# 2. 设置替换字体，按顺序对应 game_fonts
define replacement_fonts = [
    # 在此列出替换的新字体文件路径
    # 例如: "tl/Chinese/fonts/new_font.ttf",
    "tl/Chinese/fonts/xxx.ttf",
    "C:/Windows/Fonts/xxx.ttf",
]

# 字体替换逻辑
init python:
    def apply_font_replacement():
        # 检查字体列表长度一致性
        if len(game_fonts) != len(replacement_fonts):
            raise Exception(f"[Font Replacement Error] game_fonts length ({len(game_fonts)}) != replacement_fonts length ({len(replacement_fonts)})")

        # 重置字体替换映射
        config.font_replacement_map = {}

        # 所有粗体和斜体的组合
        style_combinations = [
            (False, False), # Regular
            (True, False),  # Bold
            (False, True),  # Italic
            (True, True),   # Bold Italic
        ]

        # 为每个组合统一映射到 replacement_fonts
        for old_font, new_font in zip(game_fonts, replacement_fonts):
            for bold, italic in style_combinations:
                config.font_replacement_map[old_font, bold, italic] = (new_font, bold, italic)

        # 调试输出替换信息
        print("--- All-Auto Font Replacement Applied ---")
        for old_key, new_val in config.font_replacement_map.items():
            print(f"字体替换: {old_key[0]} (b={old_key[1]}, i={old_key[2]}) -> {new_val[0]}")

# 仅在切换至目标语言（如 Chinese / simplified_chinese）时应用替换
# 请根据项目实际语言名称修改 "Chinese"
translate Chinese python:
    apply_font_replacement()

# 切换回默认语言（None）时清空替换映射
translate None python:
    config.font_replacement_map = {}
