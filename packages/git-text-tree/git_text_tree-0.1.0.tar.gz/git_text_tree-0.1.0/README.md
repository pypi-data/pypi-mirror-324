# Git Text Tree

[![Python](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)

**Git Text Tree** 是一款用于扫描 Git 仓库目录并按树状结构展示的命令行工具。它不仅支持 `.gitignore` 过滤规则，还提供对文件后缀过滤、跳过大文件、搜索指定字符串等扩展功能，可在文本或 JSON 格式下输出结果。

## 功能特性

1. **.gitignore 过滤**  
   自动读取仓库根目录下的 `.gitignore` 文件，跳过匹配的文件或目录。

2. **文本文件读取**  
   - 仅对 `text/*` 类型文件进行内容读取（可选）。  
   - 支持限定读取最大字符数，避免处理超大文本文件。

3. **后缀过滤**  
   - `--include-ext`：仅处理特定后缀的文件（如 `.py,.txt`）。  
   - `--exclude-ext`：排除指定后缀的文件。  
   > 若同时指定，脚本中默认以“先看 `include-ext`，若为空再看 `exclude-ext`”的逻辑为准，可按需修改。

4. **跳过大文件**  
   - `--skip-size <MB>`：当文件大于指定体积时直接跳过。

5. **文本搜索**  
   - `--search-text "SOMESTRING"`：检索指定字符串，并记录其在文件中的所有行号。

6. **输出格式可选**  
   - `--format text`：以类似 Unix `tree` 命令的形式打印结果（默认）。  
   - `--format json`：以 JSON 格式输出，便于做二次处理或数据分析。

7. **输出到文件**  
   - `--output-file <FILENAME>`：将结果保存为文本或 JSON 文件。

8. **扫描统计（Summary）**  
   - 打印或返回扫描过程中的统计信息，包括目录数、文件数、忽略数、大文件跳过数、搜索命中数等。

## 安装

### 1. 直接下载脚本

将 `git_text_tree.py` 下载到本地，然后安装依赖：

```bash
pip install pathspec
```

在脚本目录下即可直接使用：
```bash
python git_text_tree.py --help
```

### 2. 安装为 CLI 工具（可选）

若希望使用 `git-text-tree` 命令，可在同一目录下创建 `setup.py`：

```python
from setuptools import setup

setup(
    name='git-text-tree',
    version='0.2.0',
    py_modules=['git_text_tree'],
    install_requires=[
        'pathspec'
    ],
    entry_points={
        'console_scripts': [
            'git-text-tree=git_text_tree:main',
        ],
    },
)
```

然后执行：
```bash
pip install .
```
安装完成后即可在终端使用：
```bash
git-text-tree --help
```

## 使用示例

### 基本用法

```bash
python git_text_tree.py --repo /path/to/your/git/repo
```
或（若已安装为 CLI）：
```bash
git-text-tree --repo /path/to/your/git/repo
```
将以**树状**文本方式输出该仓库未被忽略的所有文件和目录结构。

### 显示文本内容并进行搜索

```bash
git-text-tree \
    --repo /path/to/your/git/repo \
    --show-content \
    --search-text "TODO"
```

- 对所有 `text/*` 类型文件进行内容读取；
- 同时在内容中搜索 `TODO` 字符串，并记录匹配的行号；
- 输出为文本形式，命中的文件行号可在 JSON 结果或自定义打印中查看。

### 跳过大文件、只处理指定后缀、输出 JSON

```bash
git-text-tree \
    --repo /path/to/your/git/repo \
    --include-ext .py,.md \
    --skip-size 5 \
    --format json
```

- **仅处理** `.py` 与 `.md` 文件；  
- 若文件大于 `5MB` 则跳过；  
- 以 JSON 格式在终端打印扫描结果（包含树形结构和统计信息）。

### 保存结果到文件

```bash
git-text-tree \
    --repo /path/to/your/git/repo \
    --format json \
    --output-file result.json
```

- 将扫描结果以 JSON 格式存到 `result.json` 文件，终端不再直接输出。

## 参数说明

| 参数               | 说明                                           | 默认值     |
|--------------------|-----------------------------------------------|------------|
| `--repo`           | **必填**，指定要扫描的 Git 仓库目录            | 无         |
| `--show-content`   | 是否读取并保存文本文件内容（仅 `text/*`）      | `False`    |
| `--max-length`     | 限制读取文本的最大字符数                       | `0`（不限制）|
| `--skip-size`      | 跳过超过指定MB大小的文件                       | `0`（不跳过） |
| `--search-text`    | 在文本文件中检索此字符串，记录行号             | 无         |
| `--include-ext`    | 仅处理指定后缀文件（如 `.py,.txt`）            | 空         |
| `--exclude-ext`    | 排除指定后缀文件（如 `.png,.jpg`）             | 空         |
| `--format`         | 输出格式，`text` 或 `json`                     | `text`     |
| `--output-file`    | 若指定，则将结果写入该文件（文本或 JSON 格式） | 空（不输出） |

> 当 `--include-ext` 不为空时，`--exclude-ext` 会被忽略。

## 输出说明

### 文本模式 (`--format text`)

- 以树形结构打印仓库文件夹与文件：
  ```
  ├── src/
  │   ├── main.py
  │   └── utils.py
  ├── README.md
  └── requirements.txt
  ```
- 之后打印扫描统计信息，如：
  ```
  === Summary ===
  Directories:          5
  Files:                12
  Ignored (.gitignore): 3
  Skipped large files:  1
  Matched search text:  2
  ```

### JSON 模式 (`--format json`)

- 输出一个包含 `tree` 和 `summary` 两部分的 JSON 对象：
  ```json
  {
    "tree": {
      "src": {
        "type": "dir",
        "children": {
          "main.py": {
            "type": "file",
            "content": "...",
            "search_hits": []
          },
          "utils.py": {
            "type": "file",
            "content": null,
            "search_hits": []
          }
        }
      },
      "README.md": {
        "type": "file",
        "content": "# Project\n...",
        "search_hits": [2, 10]
      },
      ...
    },
    "summary": {
      "dirs": 5,
      "files": 12,
      "ignored": 3,
      "skipped_large": 1,
      "matched_search": 2
    }
  }
  ```
- 若指定 `--show-content`，则 `content` 字段可包含部分或全部文件内容。若进行了 `--search-text`，则 `search_hits` 表示命中行号。

## 开源许可

本项目以 [MIT License](https://opensource.org/licenses/MIT) 开放源代码，欢迎自由使用与二次开发。

## 贡献

如有建议或问题，欢迎提 [Issue](https://github.com/last-emo-boy/git-text-tree/issues) 或发起 Pull Request。感谢对本项目的关注与贡献！

---

使用 **Git Text Tree**，你可以更轻松地扫描分析 Git 仓库结构，结合忽略规则、高级过滤和文本搜索，让您的项目管理与调试更加便捷！如有更多需求，可根据自身场景自由扩展脚本。祝使用愉快！