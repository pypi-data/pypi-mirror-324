import os
import mimetypes
from pathspec import PathSpec
from typing import List

def load_gitignore_patterns(repo_dir: str) -> PathSpec:
    """
    从 repo_dir 下的 .gitignore 中加载规则；若文件不存在，则返回空规则。
    """
    gitignore_path = os.path.join(repo_dir, '.gitignore')
    if not os.path.isfile(gitignore_path):
        return PathSpec.from_lines('gitwildmatch', [])
    
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    return PathSpec.from_lines('gitwildmatch', lines)

def is_text_file(file_path: str) -> bool:
    """
    判断文件是否为文本类型（'text/*'）。
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    return bool(mime_type and mime_type.startswith('text'))

def file_size_in_mb(file_path: str) -> float:
    """
    获取文件大小（MB）。
    """
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024.0)
    except OSError:
        return 0.0

def find_text_occurrences(text: str, search_string: str) -> List[int]:
    """
    在文本中搜索 search_string，返回出现该字符串的所有行号（从1开始）。
    """
    if not search_string:
        return []
    return [idx for idx, line in enumerate(text.splitlines(), start=1) if search_string in line]
