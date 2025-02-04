import os
import re
import time
from typing import Tuple, Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm

from .utils import is_text_file, file_size_in_mb, find_text_occurrences
from .logger import setup_logger

# 初始化日志（后续可在 CLI 中传入配置）
logger = setup_logger()

# 简单的文件缓存：保存文件路径及上次读取时的修改时间和内容
FILE_CACHE: Dict[str, Tuple[float, str]] = {}

def should_process_file(file_name: str, include_exts: List[str] = None, exclude_exts: List[str] = None) -> bool:
    ext = os.path.splitext(file_name)[1].lower()
    if include_exts:
        return ext in include_exts
    if exclude_exts and ext in exclude_exts:
        return False
    return True

def read_file_content(
    file_path: str,
    show_content: bool,
    max_length: int = 0,
    search_text: str = None,
    search_is_regex: bool = False
) -> Tuple[str, List[int]]:
    """
    读取文件内容并搜索匹配，同时利用简单缓存避免重复读取未变化的文件。
    """
    if not show_content:
        return None, []
    if not is_text_file(file_path):
        return None, []

    mtime = os.path.getmtime(file_path)
    # 如果缓存中有且文件未更新，则直接使用缓存内容
    if file_path in FILE_CACHE:
        cached_mtime, cached_content = FILE_CACHE[file_path]
        if mtime == cached_mtime:
            content = cached_content
        else:
            content = None
    else:
        content = None

    if content is None:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(max_length) if max_length > 0 else f.read()
            FILE_CACHE[file_path] = (mtime, content)
        except Exception as e:
            logger.error("Error reading file %s: %s", file_path, e)
            return None, []
    
    hits: List[int] = []
    if search_text:
        if search_is_regex:
            try:
                pattern = re.compile(search_text)
            except re.error as e:
                logger.error("Invalid regex '%s': %s", search_text, e)
                return content, []
            for idx, line in enumerate(content.splitlines(), start=1):
                if pattern.search(line):
                    hits.append(idx)
        else:
            hits = find_text_occurrences(content, search_text)
    
    return content, hits

def build_file_tree(
    repo_dir: str,
    spec,
    show_content: bool = True,
    max_length: int = 0,
    skip_size: float = 0,
    search_text: str = None,
    search_is_regex: bool = False,
    include_exts: List[str] = None,
    exclude_exts: List[str] = None,
    stats: Dict[str, int] = None,
    max_workers: int = 8,
    hook_manager: Any = None  # 可传入 HookManager 实例
) -> Tuple[Dict[str, Any], Dict[str, int]]:
    """
    构建文件树，同时调用钩子函数记录扫描前、每个文件处理后、扫描后事件。
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
    tree: Dict[str, Any] = {}

    context = {"repo_dir": repo_dir, "stats": stats, "tree": tree}
    if hook_manager:
        hook_manager.run_pre_scan_hooks(context)
    
    file_tasks: List[Tuple[Dict[str, Any], str, str]] = []
    
    logger.info("Starting directory scan: %s", repo_dir)
    for root, dirs, files in os.walk(repo_dir):
        rel_root = os.path.relpath(root, repo_dir)
        if rel_root == '.':
            rel_root = ''
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        keep_dirs = []
        for d in dirs:
            d_rel_path = os.path.join(rel_root, d) if rel_root else d
            if spec.match_file(d_rel_path):
                stats["ignored"] += 1
                logger.debug("Ignored directory (gitignore): %s", d_rel_path)
                continue
            keep_dirs.append(d)
        dirs[:] = keep_dirs

        path_parts = rel_root.split(os.sep) if rel_root else []
        current_node = tree
        for part in path_parts:
            current_node = current_node.setdefault(part, {"type": "dir", "children": {}})["children"]
        for d in dirs:
            current_node.setdefault(d, {"type": "dir", "children": {}})
            stats["dirs"] += 1

        for f in files:
            f_rel_path = os.path.join(rel_root, f) if rel_root else f
            if spec.match_file(f_rel_path):
                stats["ignored"] += 1
                logger.debug("Ignored file (gitignore): %s", f_rel_path)
                continue
            if not should_process_file(f, include_exts, exclude_exts):
                continue
            full_path = os.path.join(root, f)
            if skip_size > 0 and file_size_in_mb(full_path) > skip_size:
                stats["skipped_large"] += 1
                logger.debug("Skipped large file: %s", full_path)
                continue
            file_tasks.append((current_node, f, full_path))
    
    logger.info("Submitting %d file tasks with %d workers...", len(file_tasks), max_workers)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {
            executor.submit(
                read_file_content,
                full_path,
                show_content,
                max_length,
                search_text,
                search_is_regex
            ): (node, f)
            for node, f, full_path in file_tasks
        }
        for future in tqdm(as_completed(future_to_file),
                           total=len(future_to_file),
                           desc="Reading files", unit="file"):
            node, file_name = future_to_file[future]
            try:
                content, hits = future.result()
            except Exception as e:
                logger.error("Exception during file read: %s", e)
                content, hits = None, []
            stats["files"] += 1
            if hits:
                stats["matched_search"] += 1
            node[file_name] = {"type": "file", "content": content, "search_hits": hits}
            
            # 运行每个文件的钩子
            if hook_manager:
                hook_manager.run_per_file_hooks({
                    "file_name": file_name,
                    "content": content,
                    "search_hits": hits,
                    "stats": stats
                })
    
    context["tree"] = tree
    context["stats"] = stats
    if hook_manager:
        hook_manager.run_post_scan_hooks(context)
    
    logger.info("Directory scan completed.")
    return tree, stats

# 为了使用 file_size_in_mb，在此处导入
from .utils import file_size_in_mb
