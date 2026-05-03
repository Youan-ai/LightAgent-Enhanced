# LightAgent Enhanced

> 零依赖轻量级Agent框架 — @tool装饰器 · 目录即技能 · 多Agent协作

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Youan-ai/LightAgent-Enhanced?style=social)](https://github.com/Youan-ai/LightAgent-Enhanced)

## 概述

LightAgent Enhanced 是一个零依赖的轻量级Agent框架，源自 [LightAgent](https://github.com/wanxingai/lightagent) (904★) 核心设计理念，
融合到 [佑安](https://github.com/youan-ai) 本体中进行了增强和优化。

**核心理念**：用最少的外部依赖，实现最高效的Agent工具注册和调用。

## 功能特性

### 🛠️ ToolRegistry — 装饰器驱动的工具注册
```python
from lightagent import ToolRegistry

registry = ToolRegistry()

@registry.register(description="计算两数之和")
def add(a: int, b: int) -> int:
    return a + b
```
- `@tool` 装饰器自动注册
- 参数类型自动提取
- 上下文预过滤

### 📂 SkillManager — 目录即技能
```python
from lightagent import SkillManager

sm = SkillManager("skills/")
sm.discover()  # 自动发现所有 SKILL.md
```
- 扫描 `skills/` 目录自动发现技能
- 每个目录一个独立技能
- 支持热加载

### ⚡ AsyncSafeExecutor — 安全的异步执行
- 解决 asyncio 嵌套问题
- 支持同步/异步混合调用
- 自动异常捕获

### 🔗 LightSwarm — 多Agent协作分配器
- 基于任务类型的Agent路由
- 支持子Agent并行执行
- 结果自动收集与合并

### 💾 MemoryStore — 协议化内存接口
- 统一的记忆读写协议
- 支持扩展存储后端
- 轻量级实现

## 安装

```bash
# 从PyPI安装
pip install lightagent-enhanced

# 或从源码安装
git clone https://github.com/Youan-ai/LightAgent-Enhanced.git
cd LightAgent-Enhanced
pip install -e .
```

## 快速开始

```python
from lightagent import ToolRegistry, SkillManager

# 1. 创建工具注册器
registry = ToolRegistry()

@registry.register(description="问候指定的名字")
def greet(name: str) -> str:
    return f"你好, {name}!"

# 2. 发现技能
sm = SkillManager("./skills")
sm.discover()

# 3. 调用工具
result = registry.call("greet", name="世界")
print(result)  # 你好, 世界!
```

## 框架对比

| 特性 | LightAgent Enhanced | LangChain | AutoGen |
|:-----|:-------------------:|:---------:|:-------:|
| 外部依赖 | 0 (零依赖) | 100+ | 50+ |
| 安装大小 | < 100KB | > 100MB | > 50MB |
| 学习成本 | 5分钟 | 数天 | 数小时 |
| @tool装饰器 | ✅ 原生支持 | ❌ 需要额外库 | ❌ 需要额外配置 |
| 目录即技能 | ✅ 原生支持 | ❌ | ❌ |
| 多Agent协作 | ✅ LightSwarm | ✅ 复杂 | ✅ 完整 |
| MIT License | ✅ | ✅ | ✅ |

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

*隶属于 [佑安](https://github.com/youan-ai) AI助手体系 — 12引擎驱动，从代码中自我进化*
