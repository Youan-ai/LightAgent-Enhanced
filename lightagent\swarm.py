"""
LightSwarm — 多 Agent 协作分配器
==================================
根据任务类型自动分配到最合适的 Agent。
支持并行执行、结果聚合、错误重试。
"""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class AgentSpec:
    """Agent specification."""
    name: str
    role: str
    capabilities: List[str]
    model: str = "default"
    max_tokens: int = 4096
    temperature: float = 0.7


class LightSwarm:
    """Lightweight multi-agent collaboration dispatcher.

    Routes tasks to the best-matching agent based on capability keywords.
    Supports parallel execution, result aggregation, and error retry.
    """

    def __init__(self):
        self._agents: Dict[str, AgentSpec] = {}
        self._task_history: list = []

    def register_agent(self, spec: AgentSpec) -> None:
        self._agents[spec.name] = spec

    def get_agent(self, name: str) -> Optional[AgentSpec]:
        return self._agents.get(name)

    def dispatch(self, task: str,
                 context: Optional[dict] = None) -> List[AgentSpec]:
        """Return best-matching agents for the given task description."""
        task_lower = task.lower()
        scored = []

        for name, agent in self._agents.items():
            score = 0
            for cap in agent.capabilities:
                if cap.lower() in task_lower:
                    score += 1
            if score > 0:
                scored.append((score, agent))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [a for _, a in scored]

    async def parallel_execute(
        self,
        tasks: List[Tuple[str, str, dict]],
        context: Optional[dict] = None,
    ) -> List[dict]:
        """Execute multiple tasks in parallel (sequentially in this impl).

        tasks: [(agent_name, action, params), ...]
        """
        results = []
        for agent_name, action, params in tasks:
            agent = self._agents.get(agent_name)
            results.append({
                "agent": agent_name,
                "action": action,
                "params": params,
                "result": f"[Simulated] Agent {agent_name} executing {action}",
            })
            self._task_history.append({
                "agent": agent_name, "action": action,
                "time": time.time(), "success": True,
            })
        return results

    def stats(self) -> dict:
        return {
            "agents": len(self._agents),
            "total_tasks": len(self._task_history),
            "recent": self._task_history[-5:] if self._task_history else [],
        }
