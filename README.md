# Suno AI Prompt Generator

<div align="center">

**基于SUNO提示词清单的AI音乐提示词生成器**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/PyQt6-Latest-green.svg)](https://pypi.org/project/PyQt6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](#english) | [中文](#中文)

</div>

---

## 中文

### 简介

这是一个基于 **SUNO 提示词清单 PDF** 开发的 AI 音乐提示词生成工具，帮助用户快速生成高质量的 Suno AI 音乐提示词。

### 功能特性

- ✨ **现代化界面**
  - 🖥️ 桌面应用（Python + PyQt6）
  - 🌐 Web 应用（HTML + JavaScript）
  
- 🎨 **7 大分类标签页**
  - Genre 风格
  - Tempo 节奏
  - Style 描述
  - Instruments 乐器
  - Bonus 附加
  - Structure 结构
  - Dance 舞曲

- 🔍 **智能搜索与筛选**
  - 实时搜索（支持中英文）
  - 分类筛选
  - 分页显示（每页10项）

- 📝 **一键生成提示词**
  - 智能组合所有选择
  - 自动添加描述性词汇
  - 一键复制到剪贴板

- 🌙 **深色主题**
  - 护眼设计
  - 现代美观

### 快速开始

#### 桌面版（推荐）

```bash
# 克隆仓库
git clone https://github.com/yourusername/suno-prompt-generator.git
cd suno-prompt-generator

# 安装依赖
pip install PyQt6

# 运行应用
python suno_prompt_generator_pyqt.py
```

#### Web 版

```bash
# 使用 HTTP 服务器运行
python -m http.server 8000

# 然后在浏览器中访问
# http://localhost:8000/index.html
```

### 项目结构

```
suno-prompt-generator/
├── suno_prompt_generator_pyqt.py  # PyQt6 桌面应用
├── suno_prompt_generator.py         # Tkinter 桌面应用
├── index.html                       # Web 应用
├── suno_data.json                   # 统一数据文件
├── SUNO 提示词清单.pdf              # 原始 PDF 文档
├── Suno提示词清单_分类版.xlsx       # Excel 版本
└── README.md                        # 项目说明
```

### 数据来源

本工具基于 `SUNO 提示词清单.pdf` 文档，包含：
- **568+** 音乐风格标签
- **198** 附加提示词（Lyrics Prompts）
- **74** 结构提示词（Structure Prompts）
- **108** 舞曲提示词（Dance Prompts）

### 编译为可执行文件

```bash
# 安装 PyInstaller
pip install pyinstaller

# 运行编译脚本
python build_exe.py

# 编译完成后，可执行文件位于：
# dist/SunoPromptGenerator.exe
```

详细编译说明请查看 [BUILD_README.md](BUILD_README.md)

### 截图

*添加应用截图*

### 贡献

欢迎提交 Issue 和 Pull Request！

### 许可证

MIT License

---

## English

### Introduction

An AI music prompt generator based on the **SUNO Prompt List PDF**, helping users quickly generate high-quality Suno AI music prompts.

### Features

- ✨ **Modern Interface**
  - 🖥️ Desktop App (Python + PyQt6)
  - 🌐 Web App (HTML + JavaScript)
  
- 🎨 **7 Major Categories**
  - Genre
  - Tempo
  - Style
  - Instruments
  - Bonus
  - Structure
  - Dance

- 🔍 **Smart Search & Filter**
  - Real-time search (bilingual)
  - Category filtering
  - Pagination (10 items per page)

- 📝 **One-Click Generation**
  - Smart combination of all selections
  - Auto-add descriptive keywords
  - Copy to clipboard with one click

- 🌙 **Dark Theme**
  - Eye-friendly design
  - Modern aesthetics

### Quick Start

#### Desktop Version (Recommended)

```bash
# Clone repository
git clone https://github.com/yourusername/suno-prompt-generator.git
cd suno-prompt-generator

# Install dependencies
pip install PyQt6

# Run application
python suno_prompt_generator_pyqt.py
```

#### Web Version

```bash
# Run with HTTP server
python -m http.server 8000

# Then visit in browser
# http://localhost:8000/index.html
```

### Project Structure

```
suno-prompt-generator/
├── suno_prompt_generator_pyqt.py  # PyQt6 desktop app
├── suno_prompt_generator.py         # Tkinter desktop app
├── index.html                       # Web app
├── suno_data.json                   # Unified data file
├── SUNO 提示词清单.pdf              # Original PDF document
├── Suno提示词清单_分类版.xlsx       # Excel version
└── README.md                        # Project documentation
```

### Data Source

Based on the `SUNO 提示词清单.pdf` document, containing:
- **568+** music genre tags
- **198** bonus prompts (Lyrics Prompts)
- **74** structure prompts (Structure Prompts)
- **108** dance prompts (Dance Prompts)

### Build Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Run build script
python build_exe.py

# After compilation, executable located at:
# dist/SunoPromptGenerator.exe
```

For detailed build instructions, see [BUILD_README.md](BUILD_README.md)

### Screenshots

*Add application screenshots*

### Contributing

Issues and Pull Requests are welcome!

### License

MIT License