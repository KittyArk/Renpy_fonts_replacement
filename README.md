# RenPy Fonts Replacement Tool (Ren'Py 字体快速替换工具)

[English](#english) | [中文说明](#chinese)

---

<a name="english"></a>
## English

A lightweight toolkit for managing and replacing fonts in Ren'Py games using Ren'Py's native `config.font_replacement_map`.

### Features
- **All-in-One Font Tool (`font_tool.py`)**:
  - **Mode 1**: Extract referenced fonts from `.rpy` scripts only.
  - **Mode 2**: Scan font files inside a folder only.
  - **Mode 3 (Hybrid Mode)**: Extract fonts from `.rpy` scripts, then cross-check against actual files in the folder to remove non-existent font references (exempting Ren'Py built-in fonts like `DejaVuSans.ttf`).
- **Backward Compatibility**: `extract_fonts.py` and `list_fonts.py` remain available as quick entry points.
- **Ren'Py Config Files**: `fonts_replacement.rpy` and `fonts_replacement all-auto.rpy`.

### Usage

Run `font_tool.py`:
```bash
python font_tool.py
```
Select mode (1, 2, or 3) and enter the directory path.

Alternatively, pass mode and path via command line:
```bash
python font_tool.py 3 /path/to/game
```

---

<a name="chinese"></a>
## 中文说明

利用 Ren'Py 原生 `config.font_replacement_map` 实现游戏字体快速替换与提取的轻量化工具集。

### 主要功能
- **多功能一体化字体工具 (`font_tool.py`)**：
  - **模式 1（仅提取 .rpy 中的字体）**：自动扫描游戏 `.rpy` 脚本并提取引用的字体路径导出至 `fonts_output.rpy`。
  - **模式 2（仅扫描文件夹中字体）**：扫描指定文件夹下的所有字体文件相对路径导出至 `font_list.txt`。
  - **模式 3（混合模式）**：扫描 `.rpy` 提取字体，并比对文件夹中的物理字体文件，自动剔除 `.rpy` 中引用但实际不存在的字体（自动忽略/保留 Ren'Py 框架自带的内建字体，如 `DejaVuSans.ttf` 等）。
- **兼容性**：保留 `extract_fonts.py` 与 `list_fonts.py` 快捷入口文件。
- **配置文件**：`fonts_replacement.rpy` 与 `fonts_replacement all-auto.rpy`。

### 使用方法

直接运行 `font_tool.py`：
```bash
python font_tool.py
```
根据提示选择运行模式（1/2/3），并输入文件夹路径。

也可以通过命令行直接指定模式与路径：
```bash
python font_tool.py 3 /path/to/game
```
