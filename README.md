# LightAgent-Enhanced

Zero-dependency agent framework with @tool decorators, async-safe executor, and automatic skill discovery from directory structure.

## Features
- @tool decorator with auto param extraction
- Directory-as-skills: auto discover SKILL.md files
- AsyncSafeExecutor for nested asyncio
- LightSwarm: multi-agent collaboration dispatcher
- MemoryProtocol with SimpleMemoryStore

## Quick Start
```python
from lightagent import ToolRegistry, SkillManager

registry = ToolRegistry()

@registry.register
def my_tool(param: str) -> str:
    return f"Hello {param}"

await registry.execute("my_tool", param="world")
```
