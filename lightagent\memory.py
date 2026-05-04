"""
MemoryStore — 协议化内存接口（轻量版）
========================================
简单的键值存储，兼容 MemoryProtocol 接口。
支持搜索、快照持久化、版本追踪。
"""

from typing import Any, Dict, List, Optional, Tuple


class MemoryStore:
    """Lightweight memory store implementing MemoryProtocol interface."""

    def __init__(self, store: Optional[dict] = None):
        self._store: Dict[str, Any] = store or {}
        self._version = 1

    def put(self, key: str, value: Any) -> None:
        self._store[key] = value
        self._version += 1

    def get(self, key: str, default: Any = None) -> Any:
        return self._store.get(key, default)

    def delete(self, key: str) -> bool:
        if key in self._store:
            del self._store[key]
            self._version += 1
            return True
        return False

    def keys(self, prefix: str = "") -> List[str]:
        if prefix:
            return [k for k in self._store if k.startswith(prefix)]
        return list(self._store.keys())

    def search(self, query: str) -> List[Tuple[str, Any]]:
        """Simple prefix search."""
        q = query.lower()
        return [(k, v) for k, v in self._store.items() if q in k.lower()]

    def clear(self) -> None:
        self._store.clear()
        self._version += 1

    @property
    def version(self) -> int:
        return self._version

    def snapshot(self) -> dict:
        """Return snapshot for persistence."""
        return {"version": self._version, "data": self._store.copy()}

    def restore(self, snapshot: dict) -> None:
        self._version = snapshot.get("version", 1)
        self._store = snapshot.get("data", {})


class SimpleMemoryStore(MemoryStore):
    """Alias for MemoryStore, for compatibility."""
    pass
