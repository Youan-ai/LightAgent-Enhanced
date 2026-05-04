"""
AsyncSafeExecutor — 异步安全执行器
====================================
解决 asyncio 嵌套问题（在已运行事件循环中创建新循环）。

在 LLM 环境下经常遇到:
    RuntimeError("asyncio.run() cannot be called from a running event loop")

本执行器自动检测事件循环状态并选择正确的执行方式。
"""

import asyncio
from typing import Any, Optional


class AsyncSafeExecutor:
    """Safe async executor that handles nested event loop scenarios.

    Automatically detects event loop state and picks the correct execution mode.
    """

    def __init__(self):
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    async def run(self, coro):
        """Execute coroutine asynchronously (detects loop state)."""
        try:
            loop = asyncio.get_running_loop()
            return await coro
        except RuntimeError:
            return asyncio.run(coro)

    def run_sync(self, coro):
        """Synchronous wrapper for running coroutines."""
        try:
            loop = asyncio.get_running_loop()
            if loop.is_running():
                new_loop = asyncio.new_event_loop()
                try:
                    return new_loop.run_until_complete(coro)
                finally:
                    new_loop.close()
            else:
                return loop.run_until_complete(coro)
        except RuntimeError:
            return asyncio.run(coro)
