# 运行 extract_fonts.py 以获取游戏字体列表
define game_fonts = [
    # 在此列出需要替换的游戏内字体文件
    # 例如: "fonts/old_font.ttf",
    "DejaVuSans.ttf",
    ]

# 手动设置替换的字体，按顺序排列
define replacement_fonts = [
    # 在此列出新的字体文件
    # 例如: "fonts/new_font.ttf",
    # 动态生成替换字体列表
    # replacement_fonts = ["tl/chinese/fonts/LXGWWenKaiMonoGB-Regular.ttf"] * len(game_fonts)
    "tl/chinese/fonts/LXGWWenKaiMonoGB-Regular.ttf",
]

    
# 字体替换函数
init python:
    def apply_font_replacement():

        # 检查字体列表长度
        if len(game_fonts) != len(replacement_fonts):
            raise Exception(f"game_fonts length: {len(game_fonts)}, replacement_fonts length: {len(replacement_fonts)}")

        # 创建字体替换映射
        config.font_replacement_map = {}
        for old_font, new_font in zip(game_fonts, replacement_fonts):
            config.font_replacement_map[old_font, False, False] = (new_font, False, False)

        # 调试：打印替换映射到 Ren'Py 控制台
        print("Font replacement map:", config.font_replacement_map)
        for old, new in config.font_replacement_map.items():
            print(f"字体替换: {old[0]} -> {new[0]}")


translate chinese python:
    apply_font_replacement()
