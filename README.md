# ⚡ LightAgent Enhanced — Zero-Dependency Agent Framework

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-brightgreen)](https://python.org)
[![GitHub Stars](https://img.shields.io/github/stars/Youan-ai/LightAgent-Enhanced)](https://github.com/Youan-ai/LightAgent-Enhanced)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](https://github.com/Youan-ai/LightAgent-Enhanced/pulls)

> **Light enough to run anywhere. Smart enough to handle real work.**

LightAgent is a **zero-dependency agent toolkit** built on Python decorators. Register any function as a tool, auto-discover skills from directories, and coordinate multiple agents — all without installing a single external package.

**Why zero-dependency?** AI agents should run in constrained environments (Jupyter, edge devices, CI pipelines, corporate proxies) where `pip install` is painful or impossible. LightAgent uses only Python standard library.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **@tool Decorator** | Turn any function into an agent tool with auto-parameter extraction |
| **Directory-as-Skill** | Drop a `SKILL.md` in `skills/` — it's discovered automatically |
| **AsyncSafeExecutor** | Solves the nested `asyncio.run()` problem once and for all |
| **LightSwarm** | Multi-agent collaboration dispatcher (5 lines to set up) |
| **MemoryStore** | Protocol-based memory with snapshot/restore persistence |
| **6 Built-in Tools** | `get_time`, `list_tools`, `list_skills`, `memory_get/put/search` |
| **Self-Diagnostics** | One-call health check — `agent.diagnose()` |

---

## 🚀 Quick Start

```python
from lightagent import tool, LightAgent

@tool(name="greet", description="Say hello to someone")
def greet(name: str, excited: bool = False) -> str:
    greeting = f"Hello, {name}!"
    return greeting.upper() if excited else greeting

agent = LightAgent()
agent.initialize()

# Sync execution
result = agent.execute_sync("greet", name="World", excited=True)
print(result)  # {'data': 'HELLO, WORLD!', 'success': True, 'elapsed': 0.001}

# List available tools
print(agent.tools.list_tools())
```

### Async Usage

```python
import asyncio

async def main():
    agent = LightAgent()
    agent.initialize()
    result = await agent.execute("greet", {"name": "World"})
    print(result)

asyncio.run(main())
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   LightAgent                         │
├──────────┬───────────┬──────────┬─────────┬─────────┤
│ Tool     │ Skill     │ AsyncSafe│ Memory  │ Light   │
│ Registry │ Manager   │ Executor │ Store   │ Swarm   │
├──────────┴───────────┴──────────┴─────────┴─────────┤
│ • @tool decorator     • dir-scans skills/   • auto  │
│ • auto param extract  • auto-load SKILL.md   • sync │
│ • call limits/filter  • manual register      • safe │
└─────────────────────────────────────────────────────┘
```

### Component Details

| Component | File | Purpose |
|-----------|------|---------|
| `ToolRegistry` | `tool_registry.py` | Central tool registry with decorator, execution, call limits |
| `SkillManager` | `skill_manager.py` | Directory-as-skill auto-discovery |
| `AsyncSafeExecutor` | `async_executor.py` | Safe async in any environment |
| `MemoryStore` | `memory.py` | Simple key-value memory with persistence |
| `LightSwarm` | `swarm.py` | Multi-agent task dispatcher |
| `LightAgent` | `agent.py` | Main entry point integrating all components |

---

## 📚 Examples

### Custom Tools

```python
from lightagent import LightAgent
from lightagent.tool_registry import tool

@tool(name="calculate", description="Perform arithmetic")
def calculate(a: float, b: float, op: str = "add") -> float:
    ops = {"add": a + b, "sub": a - b, "mul": a * b, "div": a / b}
    return ops.get(op, a + b)

agent = LightAgent()
agent.tools.register(calculate)  # or use @agent.tools.tool()
agent.initialize()
```

### Skill Directory

Create `skills/my_toolkit/SKILL.md`:

```markdown
# My Toolkit — Custom analysis tools

## Usage
These tools are auto-discovered by LightAgent.
```

Then any `.py` files in the same directory become discoverable tools.

### Memory Persistence

```python
# Save state
snapshot = agent.memory.snapshot()
import json
with open("memory_backup.json", "w") as f:
    json.dump(snapshot, f)

# Restore state
with open("memory_backup.json", "r") as f:
    agent.memory.restore(json.load(f))
```

---

## 🧪 Testing

```bash
# Clone and test
git clone https://github.com/Youan-ai/LightAgent-Enhanced.git
cd LightAgent-Enhanced
python -c "from lightagent import LightAgent; a = LightAgent(); a.initialize(); print(a.diagnose())"

# Run full test suite
python tests/test_all.py
```

---

## 📦 Installation

```bash
# Clone directly — no pip needed
git clone https://github.com/Youan-ai/LightAgent-Enhanced.git
cd LightAgent-Enhanced

# Optional: install as package
pip install -e .
```

---

## 🤝 Contributing

Light, fast, simple. Keep it that way.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

**Guidelines:**
- Zero external dependencies — standard library only
- Keep it minimal — one file per major component
- Add tests for new functionality
- Maintain backward compatibility

---

## 📄 License

MIT — see [LICENSE](LICENSE).

---

## 🏆 Acknowledgements

- Inspired by [wanxingai/LightAgent](https://github.com/wanxingai/LightAgent) (904★)
- Built as an enhanced, modularized version with additional components

---

## 🌟 Why "Enhanced"?

Compared to the original LightAgent, this version adds:

1. **Modular architecture** — each component in its own file
2. **AsyncSafeExecutor** — solves the nested event loop problem
3. **LightSwarm** — multi-agent coordination
4. **MemoryStore with persistence** — snapshot/restore
5. **Built-in tools** — 6 ready-to-use tools
6. **Comprehensive self-diagnostics**
7. **Full test suite**
8. **Bilingual documentation** (English + Chinese code comments)
