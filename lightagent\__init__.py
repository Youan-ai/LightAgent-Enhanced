"""
LightAgent Enhanced — Zero-dependency agent framework
=====================================================

Light enough to run anywhere. Smart enough to handle real work.

Core components:
    - ToolRegistry: @tool decorator + auto param extraction + context filtering
    - SkillManager: Directory-as-Skill — drop a SKILL.md in skills/ and it's discovered
    - AsyncSafeExecutor: Solves nested asyncio (RuntimeError) once and for all
    - MemoryStore: Protocol-based memory with pluggable persistence
    - LightSwarm: Multi-agent collaboration dispatcher

Usage:
    from lightagent import tool, LightAgent

    @tool(name="greet", description="Say hello")
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    agent = LightAgent()
    result = agent.execute_sync("greet", name="World")
    print(result)  # "Hello, World!"
"""

from .tool_registry import ToolRegistry, tool
from .skill_manager import SkillManager, SkillInfo
from .async_executor import AsyncSafeExecutor
from .memory import MemoryStore, SimpleMemoryStore
from .swarm import LightSwarm, AgentSpec
from .agent import LightAgent

__all__ = [
    "ToolRegistry", "tool",
    "SkillManager", "SkillInfo",
    "AsyncSafeExecutor",
    "MemoryStore", "SimpleMemoryStore",
    "LightSwarm", "AgentSpec",
    "LightAgent",
]

__version__ = "2.0.0"
