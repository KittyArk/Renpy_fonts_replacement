# 运行 extract_fonts.py 以获取游戏字体列表
define game_fonts = [
    # 在此列出需要替换的游戏内字体文件
    # 例如: "fonts/old_font.ttf",
    "xxx.ttf",
    "fonts/xxx.ttf",
]

# 手动设置替换的字体，按顺序排列
define replacement_fonts = [
    # 在此列出新的字体文件
    # 例如: "fonts/new_font.ttf",
    # 动态生成替换字体列表
    # replacement_fonts = ["tl/xxx/fonts/xxx.ttf"] * len(game_fonts)
    # replacement_fonts = (["tl/xxx/fonts/xxx.ttf"] * x ) + ["tl/xxx/fonts/xxx.ttf"] + .....
    "tl/Chinese/fonts/xxx.ttf",
    "C:/Windows/Fonts/xxx.ttf",
    ]

    
# 字体替换函数
init python:
    def apply_font_replacement():

        # 检查字体列表长度
        if len(game_fonts) != len(replacement_fonts):
            raise Exception(f"game_fonts length: {len(game_fonts)}, replacement_fonts length: {len(replacement_fonts)}")

        # 创建字体替换映射
        config.font_replacement_map = {}
        # 所有粗体和斜体的组合
        style_combinations = [
                (False, False),
                (True, False),
                (False, True),
                (True, True),
        ]
        #把上面的排列组合丢进config.font_replacement_map替换
        for old_font, new_font in zip(game_fonts, replacement_fonts):
            for bold, italic in style_combinations:
                config.font_replacement_map[old_font, bold, italic] = (new_font, bold, italic)
                # 调试：打印替换映射到 Ren'Py 控制台
                #print("Font replacement map:", config.font_replacement_map)
        # 调试：打印简易替换映射到 Ren'Py 控制台
        for old, new in config.font_replacement_map.items():
            print(f"字体替换: {old[0]} -> {new[0]}")

#仅在特定语言进行替换
translate Chinese python:
    apply_font_replacement()
translate None python:
    config.font_replacement_map = {}
