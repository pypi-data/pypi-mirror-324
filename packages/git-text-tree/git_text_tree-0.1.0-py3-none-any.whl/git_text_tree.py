#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import mimetypes
import json
import argparse
from pathspec import PathSpec

def load_gitignore_patterns(repo_dir):
    """
    从 repo_dir 下的 .gitignore 中加载规则；若文件不存在，则返回空规则。
    """
    gitignore_path = os.path.join(repo_dir, '.gitignore')
    if not os.path.isfile(gitignore_path):
        # 返回空规则，后续可统一 spec.match_file
        return PathSpec.from_lines('gitwildmatch', [])

    with open(gitignore_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    return PathSpec.from_lines('gitwildmatch', lines)

def is_text_file(file_path):
    """
    简单判断是否为 'text/*' MIME Type。
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    return bool(mime_type and mime_type.startswith('text'))

def file_size_in_mb(file_path):
    """
    获取文件大小（MB）。
    """
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024.0)
    except OSError:
        return 0

def find_text_occurrences(text, search_string):
    """
    在给定文本 text 中搜索 search_string，
    返回一个列表，包含出现该字符串的所有行号(从1开始)。
    若未找到或 search_string 为空，则返回空列表。
    """
    if not search_string:
        return []

    lines = text.splitlines()
    hits = []
    for idx, line in enumerate(lines, start=1):
        if search_string in line:
            hits.append(idx)
    return hits

def read_file_content(file_path, show_content, max_length=0, search_text=None):
    """
    - show_content=False 时，不读取内容，直接返回 (None, [])
    - 若文件非文本类型，返回 (None, [])。
    - 若 skip_size 生效，需要在调用前就跳过，不在这里处理。
    - 如果 max_length>0，则只读取前 max_length 字符。
    - 如果 search_text 不为空，则额外搜索出现位置（行号列表）。
    - 返回 (content, search_hits)，content 为字符串或 None，
      search_hits 为行号列表（若 search_text=None 或无匹配则为空）。
    """
    if not show_content:
        return None, []

    # 判断是否文本文件
    if not is_text_file(file_path):
        return None, []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(max_length) if max_length > 0 else f.read()
    except Exception:
        # 读取异常，比如权限问题
        return None, []

    # 搜索文本
    search_hits = find_text_occurrences(content, search_text) if search_text else []

    return content, search_hits

def should_process_file(file_name, include_exts=None, exclude_exts=None):
    """
    判断当前文件名是否需要处理，基于后缀过滤。
    - 若 include_exts 非空，则只有在 include_exts 内的文件后缀才处理。
    - 若 include_exts 为空，则再判断 exclude_exts，若在 exclude_exts 内则跳过。
    """
    if not include_exts:
        # 没有 include_exts，才看 exclude_exts
        if exclude_exts:
            ext = os.path.splitext(file_name)[1].lower()
            if ext in exclude_exts:
                return False
        return True
    else:
        # 如果有 include_exts，仅处理包含的后缀
        ext = os.path.splitext(file_name)[1].lower()
        return (ext in include_exts)

def build_file_tree(
    repo_dir,
    spec,
    show_content=True,
    max_length=0,
    skip_size=0,
    search_text=None,
    include_exts=None,
    exclude_exts=None,
    stats=None
):
    """
    构建并返回文件树（dict 结构），并更新扫描统计信息 stats。
    stats 是一个可变字典，用于记录:
      - stats["dirs"] 目录数
      - stats["files"] 文件数
      - stats["ignored"] 被 .gitignore 忽略的文件数
      - stats["skipped_large"] 跳过的大文件数
      - stats["matched_search"] 存在搜索匹配的文件数

    树形结构示例:
    {
      "name": {
          "type": "dir" / "file",
          "children": {...},       # 仅 type="dir" 时
          "content": "...",        # 仅 type="file" 且为文本文件
          "search_hits": [行号...],# 若有搜索关键词，且有命中时
      },
      ...
    }
    """
    if stats is None:
        stats = {
            "dirs": 0,
            "files": 0,
            "ignored": 0,
            "skipped_large": 0,
            "matched_search": 0
        }

    repo_dir = os.path.abspath(repo_dir)
    tree = {}

    for root, dirs, files in os.walk(repo_dir):
        # rel_root for placing in tree
        rel_root = os.path.relpath(root, repo_dir)
        if rel_root == '.':
            rel_root = ''

        # 首先，强制跳过以 '.' 开头的隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        # 然后再过滤被 .gitignore 忽略的目录（避免深入遍历）
        keep_dirs = []
        for d in dirs:
            d_rel_path = os.path.join(rel_root, d) if rel_root else d
            if spec.match_file(d_rel_path):
                # 忽略目录
                stats["ignored"] += 1
                continue
            keep_dirs.append(d)
        dirs[:] = keep_dirs

        # 导航到对应节点
        path_parts = rel_root.split(os.sep) if rel_root else []
        current_node = tree
        for part in path_parts:
            current_node = current_node[part]["children"]

        # 先把目录加入树
        for d in dirs:
            current_node.setdefault(d, {
                "type": "dir",
                "children": {}
            })
            stats["dirs"] += 1

        # 处理当前目录下的文件
        for f in files:
            f_rel_path = os.path.join(rel_root, f) if rel_root else f

            # 若文件本身是隐藏文件（以.开头），也可以额外跳过，这里视需求决定：
            # if f.startswith('.'):
            #     continue

            if spec.match_file(f_rel_path):
                # 被 .gitignore 忽略
                stats["ignored"] += 1
                continue

            # 根据后缀判断是否处理
            if not should_process_file(f, include_exts, exclude_exts):
                continue

            full_path = os.path.join(root, f)

            # 检查文件大小，若超出 skip_size 则跳过
            if skip_size > 0 and file_size_in_mb(full_path) > skip_size:
                stats["skipped_large"] += 1
                continue

            stats["files"] += 1
            content, hits = read_file_content(
                file_path=full_path,
                show_content=show_content,
                max_length=max_length,
                search_text=search_text
            )

            # 如果有搜索结果，计数
            if hits:
                stats["matched_search"] += 1

            current_node[f] = {
                "type": "file",
                "content": content,
                "search_hits": hits
            }

    return tree, stats

def print_tree_text(tree, prefix="", show_content=False):
    """
    类似 Unix 'tree' 命令的文本输出。若 show_content=True，则输出文件内容。
    """
    entries = list(tree.items())
    total = len(entries)
    for i, (name, info) in enumerate(entries):
        connector = "└──" if i == total - 1 else "├──"
        if info["type"] == "dir":
            print(f"{prefix}{connector} {name}/")
            extension = "    " if i == total - 1 else "│   "
            print_tree_text(info["children"], prefix + extension, show_content)
        else:
            print(f"{prefix}{connector} {name}")
            # 如果需要打印文件内容，并且 content 不为空
            if show_content and info.get("content"):
                # 对文件内容进行逐行打印，并在前面加点缩进
                file_content_lines = info["content"].splitlines()
                for line in file_content_lines:
                    print(f"{prefix}    {line}")

def print_summary_text(stats):
    """
    以文本形式打印扫描总结信息。
    """
    print()
    print("=== Summary ===")
    print(f"Directories:         {stats['dirs']}")
    print(f"Files:               {stats['files']}")
    print(f"Ignored (.gitignore):{stats['ignored']}")
    print(f"Skipped large files: {stats['skipped_large']}")
    print(f"Matched search text: {stats['matched_search']}")

def main():
    parser = argparse.ArgumentParser(
        description="扫描并展示 Git 仓库文件树，支持忽略 .gitignore、隐藏目录、文件后缀过滤、大文件跳过、文本搜索等多功能。",
        epilog="示例：python git_text_tree.py --repo ./myrepo --show-content --search-text TODO --format json --skip-size 5"
    )
    parser.add_argument("--repo", required=True,
                        help="指定要扫描的 Git 仓库路径")
    parser.add_argument("--show-content", action="store_true", default=False,
                        help="是否读取并保存文本文件内容（仅对 text/* 生效）")
    parser.add_argument("--max-length", type=int, default=0,
                        help="读取文本文件内容的最大字符数，默认0表示不限制")
    parser.add_argument("--skip-size", type=float, default=0,
                        help="跳过大于指定MB的文件，默认0表示不跳过任何大小")
    parser.add_argument("--search-text", default=None,
                        help="在文本文件中搜索指定字符串，并记录出现行号")
    parser.add_argument("--include-ext", default="",
                        help="仅处理指定后缀文件，多个用逗号分隔（如: .py,.txt）。为空表示不启用此功能")
    parser.add_argument("--exclude-ext", default="",
                        help="排除指定后缀文件，多个用逗号分隔（如: .png,.jpg）。仅在未设置 include 时生效")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="输出格式：text 或 json，默认 text")
    parser.add_argument("--output-file", default="",
                        help="若指定，则将结果写入指定文件；否则输出到控制台")

    args = parser.parse_args()

    repo_dir = os.path.abspath(args.repo)
    spec = load_gitignore_patterns(repo_dir)

    # 处理后缀过滤参数
    include_exts = [ext.strip().lower() for ext in args.include_ext.split(',') if ext.strip()] if args.include_ext else []
    exclude_exts = [ext.strip().lower() for ext in args.exclude_ext.split(',') if ext.strip()] if args.exclude_ext else []

    # 构建文件树
    file_tree, stats = build_file_tree(
        repo_dir=repo_dir,
        spec=spec,
        show_content=args.show_content,
        max_length=args.max_length,
        skip_size=args.skip_size,
        search_text=args.search_text,
        include_exts=include_exts,
        exclude_exts=exclude_exts
    )

    # 输出
    if args.format == "text":
        # 以树的形式打印 + 文件内容（如果 show_content=True）
        print_tree_text(file_tree, show_content=args.show_content)
        # 打印统计信息
        print_summary_text(stats)

        # 若指定了输出文件（文本形式）
        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as out_f:
                import io
                buf = io.StringIO()

                # 暂存当前 stdout
                old_stdout = os.sys.stdout
                os.sys.stdout = buf

                # 打印到 StringIO
                print_tree_text(file_tree, show_content=args.show_content)
                print_summary_text(stats)

                # 恢复 stdout
                os.sys.stdout = old_stdout

                # 写入文件
                out_f.write(buf.getvalue())

    else:
        # JSON 格式输出
        # 将文件树和扫描统计信息打包到一个 dict
        output_data = {
            "tree": file_tree,
            "summary": stats
        }
        json_str = json.dumps(output_data, ensure_ascii=False, indent=2)

        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as out_f:
                out_f.write(json_str)
        else:
            print(json_str)

if __name__ == "__main__":
    main()
