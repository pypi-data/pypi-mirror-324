import argparse
import os
import json
from .scanner import build_file_tree
from .utils import load_gitignore_patterns
from .printer import print_tree_text, print_summary_text, get_json_output
from .hooks import HookManager
from .logger import setup_logger

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="扫描并展示 Git 仓库文件树，支持并发读取、正则表达式搜索、插件扩展等功能。",
        epilog="示例：git-text-tree --repo ./myrepo --show-content --search-text TODO --regex --format json --skip-size 5"
    )
    parser.add_argument("--repo", required=True, help="指定要扫描的 Git 仓库路径")
    parser.add_argument("--config", default="", help="指定 JSON 格式的配置文件（可选）")
    parser.add_argument("--show-content", action="store_true", default=False, help="是否读取并显示文本文件内容")
    parser.add_argument("--max-length", type=int, default=0, help="读取文本文件内容的最大字符数（0 表示不限制）")
    parser.add_argument("--skip-size", type=float, default=0, help="跳过大于指定MB的文件")
    parser.add_argument("--search-text", default=None, help="在文本文件中搜索指定字符串")
    parser.add_argument("--regex", action="store_true", default=False,
                        help="启用正则表达式搜索（与 --search-text 配合使用）")
    parser.add_argument("--include-ext", default="",
                        help="仅处理指定后缀文件，多个用逗号分隔（例如：.py,.txt）")
    parser.add_argument("--exclude-ext", default="",
                        help="排除指定后缀文件，多个用逗号分隔（例如：.png,.jpg），仅在未设置 include 时生效")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式：text 或 json")
    parser.add_argument("--output-file", default="", help="若指定，则将结果写入指定文件；否则输出到控制台")
    parser.add_argument("--max-workers", type=int, default=8, help="并发线程数")
    parser.add_argument("--log-level", default="INFO", help="日志级别，如 DEBUG、INFO、WARNING、ERROR")
    parser.add_argument("--log-file", default="", help="日志输出文件（可选）")
    return parser.parse_args()

def load_config(config_file: str) -> dict:
    """
    如果指定了配置文件，则加载 JSON 配置（可扩展为 YAML）。
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def main() -> None:
    args = parse_args()
    
    # 优先使用 CLI 参数配置日志，若有配置文件可覆盖
    logger = setup_logger(level=args.log_level, log_file=args.log_file)
    logger.info("Starting git-text-tree scan...")
    
    config = {}
    if args.config:
        config = load_config(args.config)
        logger.info("Loaded configuration from %s", args.config)
    
    # 合并配置，CLI 参数优先
    repo_dir = os.path.abspath(args.repo or config.get("repo"))
    spec = load_gitignore_patterns(repo_dir)
    
    include_exts = ([ext.strip().lower() for ext in args.include_ext.split(',') if ext.strip()] or 
                    config.get("include_exts", []))
    exclude_exts = ([ext.strip().lower() for ext in args.exclude_ext.split(',') if ext.strip()] or 
                    config.get("exclude_exts", []))
    
    # 初始化钩子管理器，并注册一些示例钩子
    hook_manager = HookManager()
    # 示例：扫描前打印提示
    hook_manager.add_pre_scan_hook(lambda ctx: logger.info("Pre-scan hook: scanning %s", ctx["repo_dir"]))
    # 示例：每个文件处理后，如果匹配则打印文件名
    hook_manager.add_per_file_hook(lambda ctx: logger.debug("Processed file: %s, hits: %s",
                                                              ctx["file_name"],
                                                              ctx["search_hits"]))
    # 示例：扫描后打印统计结果
    hook_manager.add_post_scan_hook(lambda ctx: logger.info("Post-scan hook: stats: %s", ctx["stats"]))
    
    tree, stats = build_file_tree(
        repo_dir=repo_dir,
        spec=spec,
        show_content=args.show_content,
        max_length=args.max_length,
        skip_size=args.skip_size,
        search_text=args.search_text,
        search_is_regex=args.regex,
        include_exts=include_exts,
        exclude_exts=exclude_exts,
        stats=None,
        max_workers=args.max_workers,
        hook_manager=hook_manager
    )
    
    if args.format == "text":
        print_tree_text(tree, show_content=args.show_content)
        print_summary_text(stats)
        output_str = None
    else:
        output_str = get_json_output(tree, stats)
        print(output_str)
    
    if args.output_file:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            if output_str:
                f.write(output_str)
            else:
                import io, sys
                buf = io.StringIO()
                old_stdout = sys.stdout
                sys.stdout = buf
                print_tree_text(tree, show_content=args.show_content)
                print_summary_text(stats)
                sys.stdout = old_stdout
                f.write(buf.getvalue())
    
    logger.info("git-text-tree scan completed.")

if __name__ == "__main__":
    main()
