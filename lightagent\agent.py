"""
LightAgent — 主入口：整合所有组件
===================================
"""

import time
from typing import Any, Dict, Optional

from .tool_registry import ToolRegistry, tool
from .skill_manager import SkillManager
from .async_executor import AsyncSafeExecutor
from .memory import SimpleMemoryStore
from .swarm import LightSwarm, AgentSpec


class LightAgent:
    """LightAgent main entry point — integrates all components.

    Usage:
        agent = LightAgent(skills_dir="./skills")
        agent.initialize()

        # Execute a tool
        result = agent.execute_sync("get_time")

        # Use memory
        agent.memory.put("key", "value")
        val = agent.memory.get("key")

        # Diagnostics
        status = agent.diagnose()
    """

    def __init__(self, skills_dir: str = "skills"):
        self.tools = ToolRegistry()
        self.skills = SkillManager(skills_dir)
        self.executor = AsyncSafeExecutor()
        self.memory = SimpleMemoryStore()
        self.swarm = LightSwarm()

        self._register_builtins()
        self._initialized = False

    def _register_builtins(self):
        """Register built-in tool functions."""

        @self.tools.tool(name="get_time", description="Get current time",
                         category="系统")
        def get_time() -> str:
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        @self.tools.tool(name="list_skills",
                         description="List all available skills",
                         category="系统")
        def list_skills() -> list:
            return [
                {"name": s.name, "description": s.description, "category": s.category}
                for s in self.skills.list_skills()
            ]

        @self.tools.tool(name="list_tools",
                         description="List all registered tools",
                         category="系统")
        def list_tools(category: Optional[str] = None) -> list:
            return self.tools.list_tools(category=category)

        @self.tools.tool(name="memory_get",
                         description="Get a value from memory storage",
                         category="记忆")
        def memory_get(key: str, default: Any = None) -> Any:
            return self.memory.get(key, default)

        @self.tools.tool(name="memory_put",
                         description="Store a value in memory",
                         category="记忆")
        def memory_put(key: str, value: Any) -> bool:
            self.memory.put(key, value)
            return True

        @self.tools.tool(name="memory_search",
                         description="Search memory by prefix",
                         category="记忆")
        def memory_search(query: str) -> list:
            return self.memory.search(query)

    def initialize(self):
        """Initialize: auto-discover skills, register agents."""
        discovered = self.skills.discover()
        self.swarm.register_agent(AgentSpec(
            name="佑安", role="AI Assistant",
            capabilities=["编程", "分析", "写作", "咨询", "学习"],
        ))
        self._initialized = True
        return {
            "discovered_skills": len(discovered),
            "tools": len(self.tools._tools),
        }

    async def execute(self, tool_name: str, **kwargs) -> Any:
        """Execute a tool function (async interface)."""
        return await self.tools.execute(tool_name, kwargs)

    def execute_sync(self, tool_name: str, **kwargs) -> Any:
        """Execute a tool function (sync interface)."""
        return self.executor.run_sync(self.tools.execute(tool_name, kwargs))

    def diagnose(self) -> Dict[str, Any]:
        """Run self-diagnostics."""
        return {
            "initialized": self._initialized,
            "tools": len(self.tools._tools),
            "skills_discovered": len(self.skills._skills),
            "skills_manual": len(self.skills._manual_skills),
            "memory_keys": len(self.memory.keys()),
            "agents": len(self.swarm._agents),
            "tool_calls": sum(
                t["call_count"] for t in self.tools._tools.values()
            ),
        }
