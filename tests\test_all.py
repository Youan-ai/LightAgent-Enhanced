#!/usr/bin/env python3
"""Test suite for LightAgent-Enhanced."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lightagent import (
    LightAgent, ToolRegistry, SkillManager,
    AsyncSafeExecutor, MemoryStore, LightSwarm, AgentSpec,
)


def test_tool_registry():
    """Test ToolRegistry basic operations."""
    reg = ToolRegistry()

    @reg.tool(name="echo", description="Echo input")
    def echo(text: str, times: int = 1) -> str:
        return text * times

    assert len(reg.list_tools()) == 1
    tool_info = reg.get("echo")
    assert tool_info is not None
    assert tool_info["name"] == "echo"

    import asyncio
    result = asyncio.run(reg.execute("echo", {"text": "hi", "times": 3}))
    assert result["success"] is True
    assert result["data"] == "hihihi"

    reg.disable("echo")
    result = asyncio.run(reg.execute("echo", {"text": "test"}))
    assert result["success"] is False
    assert "disabled" in result.get("error", "")

    print("✓ ToolRegistry tests passed")
    return True


def test_skill_manager():
    """Test SkillManager discovery."""
    sm = SkillManager("nonexistent_dir")
    discovered = sm.discover()
    assert discovered == []
    assert sm.list_skills() == []

    # Manual registration
    sm.register("test_skill", "/tmp/skills/test", "A test skill")
    assert sm.get("test_skill") is not None
    assert sm.get("test_skill").description == "A test skill"

    print("✓ SkillManager tests passed")
    return True


def test_async_executor():
    """Test AsyncSafeExecutor."""
    executor = AsyncSafeExecutor()

    async def sample_coro():
        return 42

    # Sync wrapper
    result = executor.run_sync(sample_coro())
    assert result == 42

    print("✓ AsyncSafeExecutor tests passed")
    return True


def test_memory_store():
    """Test MemoryStore operations."""
    mem = MemoryStore()

    mem.put("key1", "value1")
    mem.put("key2", {"nested": "data"})
    assert mem.get("key1") == "value1"
    assert mem.get("key2")["nested"] == "data"
    assert mem.get("nonexistent", "default") == "default"

    assert mem.delete("key1") is True
    assert mem.delete("nonexistent") is False

    mem.put("alpha_1", "a")
    mem.put("alpha_2", "b")
    assert len(mem.keys("alpha_")) == 2

    # Snapshot persistence
    snap = mem.snapshot()
    mem2 = MemoryStore()
    mem2.restore(snap)
    assert mem2.get("alpha_1") == "a"

    print("✓ MemoryStore tests passed")
    return True


def test_light_swarm():
    """Test LightSwarm dispatching."""
    swarm = LightSwarm()

    swarm.register_agent(AgentSpec(
        name="coder", role="Programmer",
        capabilities=["python", "code", "programming"],
    ))
    swarm.register_agent(AgentSpec(
        name="writer", role="Writer",
        capabilities=["writing", "documentation"],
    ))

    # Dispatch a coding task
    result = swarm.dispatch("Write Python code")
    assert len(result) >= 1
    assert result[0].name == "coder"

    print("✓ LightSwarm tests passed")
    return True


def test_light_agent():
    """Test LightAgent integration."""
    agent = LightAgent()

    init = agent.initialize()
    assert init["discovered_skills"] >= 0
    assert init["tools"] >= 6  # 6 built-in tools

    # Built-in tools
    result = agent.execute_sync("get_time")
    assert result["success"] is True
    assert len(result["data"]) > 0  # timestamp string

    # Memory via built-in tools
    result = agent.execute_sync("memory_put", key="test", value="hello")
    assert result["success"] is True

    result = agent.execute_sync("memory_get", key="test")
    assert result["data"] == "hello"

    # Diagnostics
    diag = agent.diagnose()
    assert diag["initialized"] is True
    assert diag["tools"] >= 6

    print("✓ LightAgent integration tests passed")
    return True


def main():
    print("=" * 50)
    print("LightAgent-Enhanced Test Suite")
    print("=" * 50)
    print(f"Python {sys.version}")

    tests = [
        test_tool_registry,
        test_skill_manager,
        test_async_executor,
        test_memory_store,
        test_light_swarm,
        test_light_agent,
    ]

    passed = 0
    failed = 0
    for test_fn in tests:
        try:
            test_fn()
            passed += 1
        except Exception as e:
            print(f"✗ {test_fn.__name__} FAILED: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print(f"\n{'=' * 50}")
    print(f"Results: {passed} passed, {failed} failed, {len(tests)} total")
    print(f"{'=' * 50}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
