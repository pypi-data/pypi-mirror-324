from typing import Callable, Dict, Any, List

# 定义钩子类型（例如：扫描前、扫描后、处理每个文件）
Hook = Callable[[Dict[str, Any]], None]

class HookManager:
    """
    提供简单的插件机制，允许在特定事件（例如扫描前、扫描后、每个文件处理后）时执行自定义钩子函数。
    """
    def __init__(self):
        self.pre_scan_hooks: List[Hook] = []
        self.post_scan_hooks: List[Hook] = []
        self.per_file_hooks: List[Hook] = []
    
    def add_pre_scan_hook(self, hook: Hook):
        self.pre_scan_hooks.append(hook)
    
    def add_post_scan_hook(self, hook: Hook):
        self.post_scan_hooks.append(hook)
    
    def add_per_file_hook(self, hook: Hook):
        self.per_file_hooks.append(hook)
    
    def run_pre_scan_hooks(self, context: Dict[str, Any]):
        for hook in self.pre_scan_hooks:
            hook(context)
    
    def run_post_scan_hooks(self, context: Dict[str, Any]):
        for hook in self.post_scan_hooks:
            hook(context)
    
    def run_per_file_hooks(self, context: Dict[str, Any]):
        for hook in self.per_file_hooks:
            hook(context)
