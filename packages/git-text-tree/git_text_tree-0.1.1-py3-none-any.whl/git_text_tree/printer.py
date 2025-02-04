import json
from typing import Dict, Any, List

def print_tree_text(tree: Dict[str, Any], prefix: str = "", show_content: bool = False) -> None:
    """
    以类似 Unix tree 命令的格式打印文件树，支持打印文件内容。
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
            if show_content and info.get("content"):
                for line in info["content"].splitlines():
                    print(f"{prefix}    {line}")

def print_summary_text(stats: Dict[str, int]) -> None:
    """
    打印扫描统计信息。
    """
    print("\n=== Summary ===")
    print(f"Directories:          {stats['dirs']}")
    print(f"Files:                {stats['files']}")
    print(f"Ignored (.gitignore): {stats['ignored']}")
    print(f"Skipped large files:  {stats['skipped_large']}")
    print(f"Matched search text:  {stats['matched_search']}")

def get_json_output(tree: Dict[str, Any], stats: Dict[str, int]) -> str:
    """
    返回 JSON 格式的输出。
    """
    output_data = {"tree": tree, "summary": stats}
    return json.dumps(output_data, ensure_ascii=False, indent=2)

def get_md_output(tree: Dict[str, Any], stats: Dict[str, int]) -> str:
    """
    返回 Markdown 格式的输出，包括文件树和统计信息。
    """
    md_lines: List[str] = []

    def traverse_tree(t: Dict[str, Any], indent: str = "") -> None:
        for name, info in t.items():
            if info["type"] == "dir":
                md_lines.append(f"{indent}- **{name}/**")
                traverse_tree(info["children"], indent + "    ")
            else:
                md_lines.append(f"{indent}- {name}")
                if info.get("content"):
                    # 可以选择是否嵌入文件内容，这里以代码块展示
                    md_lines.append(f"{indent}  ```")
                    md_lines.extend(f"{indent}  {line}" for line in info["content"].splitlines())
                    md_lines.append(f"{indent}  ```")

    md_lines.append("# File Tree")
    md_lines.append("")
    traverse_tree(tree)
    md_lines.append("")
    md_lines.append("## Summary")
    md_lines.append("")
    md_lines.append(f"- **Directories:** {stats['dirs']}")
    md_lines.append(f"- **Files:** {stats['files']}")
    md_lines.append(f"- **Ignored (.gitignore):** {stats['ignored']}")
    md_lines.append(f"- **Skipped large files:** {stats['skipped_large']}")
    md_lines.append(f"- **Matched search text:** {stats['matched_search']}")
    return "\n".join(md_lines)

def get_html_output(tree: Dict[str, Any], stats: Dict[str, int]) -> str:
    """
    返回 HTML 格式的输出，包括文件树和统计信息。
    """
    html_lines: List[str] = []
    html_lines.append("<!DOCTYPE html>")
    html_lines.append("<html>")
    html_lines.append("<head>")
    html_lines.append("  <meta charset='utf-8'>")
    html_lines.append("  <title>File Tree Report</title>")
    html_lines.append("  <style>")
    html_lines.append("    ul { list-style-type: none; }")
    html_lines.append("    li.dir { font-weight: bold; }")
    html_lines.append("    pre { background-color: #f4f4f4; padding: 5px; }")
    html_lines.append("  </style>")
    html_lines.append("</head>")
    html_lines.append("<body>")
    html_lines.append("  <h1>File Tree</h1>")

    def traverse_tree_html(t: Dict[str, Any]) -> None:
        html_lines.append("  <ul>")
        for name, info in t.items():
            if info["type"] == "dir":
                html_lines.append(f"    <li class='dir'>{name}/")
                traverse_tree_html(info["children"])
                html_lines.append("    </li>")
            else:
                html_lines.append(f"    <li>{name}")
                if info.get("content"):
                    html_lines.append("      <pre>")
                    # 对文件内容进行 HTML 转义
                    for line in info["content"].splitlines():
                        escaped_line = (
                            line.replace("&", "&amp;")
                                .replace("<", "&lt;")
                                .replace(">", "&gt;")
                        )
                        html_lines.append(f"        {escaped_line}")
                    html_lines.append("      </pre>")
                html_lines.append("    </li>")
        html_lines.append("  </ul>")

    traverse_tree_html(tree)
    html_lines.append("  <h2>Summary</h2>")
    html_lines.append("  <ul>")
    html_lines.append(f"    <li><strong>Directories:</strong> {stats['dirs']}</li>")
    html_lines.append(f"    <li><strong>Files:</strong> {stats['files']}</li>")
    html_lines.append(f"    <li><strong>Ignored (.gitignore):</strong> {stats['ignored']}</li>")
    html_lines.append(f"    <li><strong>Skipped large files:</strong> {stats['skipped_large']}</li>")
    html_lines.append(f"    <li><strong>Matched search text:</strong> {stats['matched_search']}</li>")
    html_lines.append("  </ul>")
    html_lines.append("</body>")
    html_lines.append("</html>")
    return "\n".join(html_lines)
