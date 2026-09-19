# RenPy Fonts Replacement Tool (Ren'Py 字体快速替换工具)

[English](#english) | [中文说明](#chinese)

---

<a name="english"></a>
## English

A lightweight toolkit for quickly replacing fonts in Ren'Py games using Ren'Py's native `config.font_replacement_map`.

### Features
- **Font Extraction (`extract_fonts.py`)**: Automatically scans all `.rpy` files in your Ren'Py game folder to find all referenced font files (`.ttf`, `.otf`, `.ttc`, `.otc`). Generates `fonts_output.rpy`.
- **Font Listing (`list_fonts.py`)**: Lists all font files inside a designated folder (e.g., your game or asset directory) and generates `font_list.txt`.
- **Flexible Replacement Configs**:
  - `fonts_replacement.rpy`: Configurable font replacement mapping, allowing independent mappings for regular, bold, italic, and bold-italic font files.
  - `fonts_replacement all-auto.rpy`: Automatically maps all style variations (bold, italic, bold-italic) of a font to the specified replacement font file.

### Usage Steps

1. **Extract game fonts**:
   Run `python extract_fonts.py` and input your game's directory path (or pass as a command-line argument).
2. **List available replacement fonts**:
   Run `python list_fonts.py` and input the folder containing your replacement fonts.
3. **Configure replacement in `.rpy`**:
   Copy either `fonts_replacement.rpy` or `fonts_replacement all-auto.rpy` into your game's `game/` folder. Update `game_fonts` and `replacement_fonts` with the corresponding font paths.
4. **Language Target**:
   Adjust `translate Chinese python:` in the `.rpy` file to match your game's translation language identifier (e.g. `simplified_chinese`).

---

<a name="chinese"></a>
## 中文说明

利用 Ren'Py 原生 `config.font_replacement_map` 实现游戏字体快速替换的轻量化工具集。

### 主要功能
- **提取游戏字体 (`extract_fonts.py`)**：自动扫描 Ren'Py 游戏目录下的所有 `.rpy` 脚本，精准提取引用的字体文件（支持 `.ttf`、`.otf`、`.ttc`、`.otc` 格式），并导出为 `fonts_output.rpy`。
- **列出文件夹字体 (`list_fonts.py`)**：扫描指定文件夹下的所有字体文件，并按相对路径导出为 `font_list.txt`。
- **灵活动态替换**：
  - `fonts_replacement.rpy`：精细化映射配置，可为常规体、粗体、斜体及粗斜体分别指定独立字体文件。
  - `fonts_replacement all-auto.rpy`：全自动映射配置，将某种字体的所有样式组合（粗体、斜体等）统一映射至指定的替换字体。

### 使用方法

1. **提取原游戏字体**：
   运行 `python extract_fonts.py`，根据提示输入游戏根目录或 `game` 文件夹路径（亦可作为命令行参数传入）。
2. **扫描新的替换字体**：
   运行 `python list_fonts.py`，输入存放新字体的文件夹路径。
3. **配置替换规则**：
   将 `fonts_replacement.rpy` 或 `fonts_replacement all-auto.rpy` 放入游戏 `game/` 目录下，根据前面提取的结果填写 `game_fonts` 与 `replacement_fonts` 数组。
4. **语言绑定**：
   修改 `.rpy` 文件底部的 `translate Chinese python:` 为你项目中实际对应的语言标识（如 `simplified_chinese`）。
