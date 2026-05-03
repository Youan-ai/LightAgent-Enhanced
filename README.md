# ⚡ LightAgent — Zero-Dependency Agent Framework

> **Light enough to run anywhere. Smart enough to handle real work.**

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-brightgreen)](https://python.org)

LightAgent is a **zero-dependency agent toolkit** built on Python decorators. Register any function as a tool, auto-discover skills from directories, and coordinate multiple agents — all without installing a single external package.

---

## ✨ Features

- **@tool Decorator** — Turn any function into an agent tool with auto-parameter extraction
- **Directory-as-Skill** — Just drop a SKILL.md in skills/ and it's discovered
- **AsyncSafeExecutor** — Solves the nested asyncio problem once and for all
- **LightSwarm** — Multi-agent collaboration dispatcher (5 lines to set up)
- **Protocol-based Memory** — SimpleMemoryStore with pluggable persistence

## 📦 Installation

```bash
git clone https://github.com/Youan-ai/LightAgent-Enhanced.git
cd LightAgent-Enhanced
# No pip package — just import the module and go
```

## 🚀 Quick Start

```python
from light_agent import tool, LightAgent

@tool(name="greet", desc="Say hello to someone")
def greet(name: str):
    return f"Hello, {name}!"

agent = LightAgent()
result = agent.execute("greet", {"name": "World"})
print(result)  # "Hello, World!"
```

## 🏗️ Architecture

```
┌───────────────────────────────────┐
│           LightAgent               │
├───────────────┬───────────────────┤
│ ToolRegistry  │ SkillManager      │
├───────────────┼───────────────────┤
│ @tool decor   │ dir-scans skills/ │
│ auto-extract  │ auto-load         │
│ params        │ SKILL.md files    │
└───────────────┴───────────────────┘
```

## 📚 Key Components

| Component | Purpose |
|-----------|---------|
| `@tool` | Decorator — one line turns function into tool |
| `ToolRegistry` | Central tool registry with context filtering |
| `SkillManager` | Auto-discovers skills/ directory |
| `LightSwarm` | Multi-agent coordinator |
| `AsyncSafeExecutor` | Safe async execution in any environment |

## 🤝 Contributing

Light, fast, simple. Keep it that way.

## 📄 License

MIT — see [LICENSE](LICENSE).
