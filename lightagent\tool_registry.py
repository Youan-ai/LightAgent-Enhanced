"""
ToolRegistry — 零依赖工具注册中心
=================================
装饰器驱动的工具注册、参数自动提取、上下文预过滤。

Use:
    reg = ToolRegistry()

    @reg.tool(name="search", description="Search the web")
    def search(query: str, count: int = 5) -> str:
        ...

    result = await reg.execute("search", {"query": "AI"})
"""

import asyncio
import inspect
import time
import traceback
from typing import Any, Callable, Dict, List, Optional, Set


def tool(name: Optional[str] = None, description: str = "",
         category: str = "通用", hidden: bool = False,
         max_calls_per_task: Optional[int] = None):
    """Standalone @tool decorator for use outside ToolRegistry.

    Usage:
        @tool(name="greet", description="Say hello")
        def greet(name: str) -> str:
            return f"Hello, {name}!"
    """
    def decorator(func):
        import functools
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper._tool_name = name or func.__name__
        wrapper._tool_description = description or func.__doc__ or ""
        wrapper._tool_category = category
        wrapper._tool_hidden = hidden
        wrapper._tool_max_calls = max_calls_per_task
        wrapper._is_tool = True

        # Extract params
        sig = inspect.signature(func)
        wrapper._tool_params = {}
        for pname, param in sig.parameters.items():
            if pname == "self":
                continue
            default = None if param.default is inspect.Parameter.empty else param.default
            wrapper._tool_params[pname] = {
                "required": param.default is inspect.Parameter.empty,
                "default": default,
            }
        return wrapper
    return decorator


class ToolRegistry:
    """Zero-dependency tool registry. Supports sync and async functions.

    Usage:
        reg = ToolRegistry()

        @reg.tool(name="search", description="Search the web")
        def search(query: str, count: int = 5) -> str:
            ...

        result = await reg.execute("search", {"query": "AI", "count": 3})
    """

    def __init__(self, auto_prune: bool = True):
        self._tools: Dict[str, dict] = {}
        self._disabled: Set[str] = set()
        self._call_history: list = []
        self._auto_prune = auto_prune

    def tool(self, name: Optional[str] = None, description: str = "",
             category: str = "通用", hidden: bool = False,
             max_calls_per_task: Optional[int] = None):
        """Register a tool via decorator. Auto-extracts parameter signature."""
        def decorator(func):
            nonlocal name
            tool_name = name or func.__name__

            # Extract param info from signature
            sig = inspect.signature(func)
            params = {}
            for pname, param in sig.parameters.items():
                default = None if param.default is inspect.Parameter.empty else param.default
                annotation = str if param.annotation is inspect.Parameter.empty else param.annotation
                required = param.default is inspect.Parameter.empty
                params[pname] = {
                    "type": annotation.__name__ if hasattr(annotation, '__name__') else str(annotation),
                    "required": required,
                    "default": default,
                }

            # Skip 'self' for methods
            if tool_name != "self" and "self" in params:
                del params["self"]

            is_async = asyncio.iscoroutinefunction(func)

            self._tools[tool_name] = {
                "name": tool_name,
                "description": description or func.__doc__ or "",
                "func": func,
                "signature": sig,
                "params": params,
                "is_async": is_async,
                "category": category,
                "hidden": hidden,
                "call_count": 0,
                "max_calls": max_calls_per_task or 999999,
                "enabled": True,
            }
            return func
        return decorator

    def register(self, func: Callable, name: Optional[str] = None,
                 description: str = "", **kwargs):
        """Register a function directly (non-decorator mode)."""
        return self.tool(name=name, description=description, **kwargs)(func)

    def get(self, name: str) -> Optional[dict]:
        return self._tools.get(name)

    def list_tools(self, category: Optional[str] = None,
                   include_hidden: bool = False) -> List[dict]:
        result = []
        for tool in self._tools.values():
            if tool["hidden"] and not include_hidden:
                continue
            if category and tool["category"] != category:
                continue
            if not tool["enabled"]:
                continue
            result.append({
                "name": tool["name"],
                "description": tool["description"][:100],
                "params": tool["params"],
                "category": tool["category"],
            })
        return result

    async def execute(self, name: str, kwargs: dict,
                      context: Optional[dict] = None) -> Any:
        """Execute a tool function. Auto-handles sync/async."""
        tool = self._tools.get(name)
        if not tool:
            return {"error": f"Tool '{name}' not found", "success": False}
        if not tool["enabled"] or name in self._disabled:
            return {"error": f"Tool '{name}' is disabled", "success": False}

        # Call limit
        tool["call_count"] += 1
        if tool["call_count"] > tool["max_calls"]:
            return {
                "error": f"Tool '{name}' exceeded max calls ({tool['max_calls']})",
                "success": False,
            }

        # Filter params: only pass what the function accepts
        filtered = {k: v for k, v in kwargs.items() if k in tool["params"]}

        start = time.time()
        try:
            if tool["is_async"]:
                result = await tool["func"](**filtered)
            else:
                result = tool["func"](**filtered)
            elapsed = time.time() - start

            self._call_history.append({
                "tool": name, "args": filtered, "elapsed": elapsed,
                "success": True, "time": time.time(),
            })

            return {"data": result, "success": True, "elapsed": elapsed}
        except Exception as e:
            elapsed = time.time() - start
            self._call_history.append({
                "tool": name, "args": filtered, "elapsed": elapsed,
                "success": False, "error": str(e), "time": time.time(),
            })
            return {
                "error": str(e), "traceback": traceback.format_exc(),
                "success": False, "elapsed": elapsed,
            }

    def disable(self, name: str):
        self._disabled.add(name)
        if name in self._tools:
            self._tools[name]["enabled"] = False

    def enable(self, name: str):
        self._disabled.discard(name)
        if name in self._tools:
            self._tools[name]["enabled"] = True

    def stats(self) -> dict:
        usage = {}
        for t in self._tools.values():
            usage[t["name"]] = t["call_count"]
        return {
            "total_tools": len(self._tools),
            "disabled": len(self._disabled),
            "total_calls": sum(t["call_count"] for t in self._tools.values()),
            "usage": usage,
            "last_calls": self._call_history[-10:] if self._call_history else [],
        }

    def prune_history(self, max_age: float = 3600):
        """Clean old history records."""
        now = time.time()
        self._call_history = [
            h for h in self._call_history if now - h["time"] < max_age
        ]
