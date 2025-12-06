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
    "tl/xxx/fonts/xxx_regular.ttf",
]

# 2. 粗体替换列表（可选）
# 如果某个字体没有专门的粗体文件，请填入 None
# 如果对应位置填 None，Ren'Py 会尝试算法加粗或使用常规字体
define replacement_bold_fonts = [
    "tl/xxx/fonts/xxx_bold.ttf",  # 对应第一个字体的粗体
    # None,                       # 对应第二个字体（如果有），使用 None 跳过
]

# 3. 斜体替换列表（可选）
# 如果某个字体没有专门的斜体文件，请填入 None
# 如果对应位置填 None，Ren'Py 会尝试算法倾斜或使用常规字体
define replacement_italic_fonts = [
    "tl/xxx/fonts/xxx_italic.ttf", # 对应第一个字体的斜体
    # None, 
]

# 4. 粗斜体替换列表（可选）
# 当文本同时应用了 {b} 和 {i} 标签时使用
define replacement_bold_italic_fonts = [
    "tl/xxx/fonts/xxx_bold_italic.ttf",
    # None,
]

# 字体替换函数
init python:
    def apply_font_replacement():
        
        # 检查基础字体列表长度一致性
        if len(game_fonts) != len(replacement_fonts):
            raise Exception(f"Error: game_fonts length ({len(game_fonts)}) != replacement_fonts length ({len(replacement_fonts)})")
        # 检查粗体字体列表长度一致性
        if len(game_fonts) != len(replacement_bold_fonts):
            raise Exception(f"Error: game_fonts length ({len(game_fonts)}) != replacement_bold_fonts length ({len(replacement_bold_fonts)})")
        # 检查斜体字体列表长度一致性
        if len(game_fonts) != len(replacement_italic_fonts):
            raise Exception(f"Error: game_fonts length ({len(game_fonts)}) != replacement_italic_fonts length ({len(replacement_italic_fonts)})")
        # 检查粗斜体字体列表长度一致性
        if len(game_fonts) != len(replacement_bold_italic_fonts):
            raise Exception(f"Error: game_fonts length ({len(game_fonts)}) != replacement_bold_italic_fonts length ({len(replacement_bold_italic_fonts)})")
            
        # 重置字体替换映射
        config.font_replacement_map = {}

        # 遍历游戏字体列表进行映射
        for index, old_font in enumerate(game_fonts):
            # --- 1. 常规字体映射 (Regular) ---
            new_font = replacement_fonts[index]
            # 映射: (旧字体, 粗体False, 斜体False) -> (新字体, 粗体False, 斜体False)
            config.font_replacement_map[old_font, False, False] = (new_font, False, False)

            # --- 2. 粗体映射 (Bold) ---
            # 检查列表是否存在且该索引不为 None
            if index < len(replacement_bold_fonts) and replacement_bold_fonts[index] is not None:
                new_bold = replacement_bold_fonts[index]
                # 映射: (旧字体, 粗体True, 斜体False) -> (新粗体文件, 强制不加粗, 强制不倾斜)
                config.font_replacement_map[old_font, True, False] = (new_bold, False, False)

            # --- 3. 斜体映射 (Italic) ---
            # 检查列表是否存在且该索引不为 None
            if index < len(replacement_italic_fonts) and replacement_italic_fonts[index] is not None:
                new_italic = replacement_italic_fonts[index]
                # 映射: (旧字体, 粗体False, 斜体True) -> (新斜体文件, 强制不加粗, 强制不倾斜)
                config.font_replacement_map[old_font, False, True] = (new_italic, False, False)

            # (可选) 粗斜体映射 (Bold Italic)
            # 如果你有专门的粗斜体文件，可以仿照上面逻辑添加。
            # 这里通常不需要，除非 UI 对粗斜体有极高要求。
            # --- 4. 粗斜体映射 (Bold Italic) ---
            if index < len(replacement_bold_italic_fonts) and replacement_bold_italic_fonts[index] is not None:
                new_bold_italic = replacement_bold_italic_fonts[index]
                # 映射: (旧字体, 粗体True, 斜体True) -> (新粗斜体文件, 强制不加粗, 强制不倾斜)
                config.font_replacement_map[old_font, True, True] = (new_bold_italic, False, False)
                
        # 调试：打印简易替换映射到 Ren'Py 控制台
        print("--- Font Replacement Applied ---")
        for key, value in config.font_replacement_map.items():
            # 获取样式名称用于显示
            styles = []
            if key[1]: styles.append("Bold")
            if key[2]: styles.append("Italic")
            style_name = " + ".join(styles) if styles else "Regular"
            
            print(f"Replace [{style_name}]: {key[0]} -> {value[0]}")

#仅在特定语言进行替换
translate Chinese python:
    apply_font_replacement()

translate None python:
    config.font_replacement_map = {}
