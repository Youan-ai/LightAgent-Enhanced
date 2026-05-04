"""
Example 2: Multi-agent coordination with LightSwarm
"""
from lightagent import LightAgent
from lightagent.swarm import AgentSpec

agent = LightAgent()
agent.initialize()

# Register specialized agents
agent.swarm.register_agent(AgentSpec(
    name="coder", role="Programmer",
    capabilities=["python", "code", "programming", "debug", "javascript"],
))
agent.swarm.register_agent(AgentSpec(
    name="writer", role="Content Writer",
    capabilities=["writing", "article", "documentation", "blog", "essay"],
))
agent.swarm.register_agent(AgentSpec(
    name="analyst", role="Data Analyst",
    capabilities=["analysis", "data", "statistics", "chart", "report"],
))

# Dispatch tasks
task1 = "Write a Python script to analyze data"
task2 = "Create documentation for the API"
task3 = "Fix this JavaScript bug"

for i, task in enumerate([task1, task2, task3], 1):
    agents = agent.swarm.dispatch(task)
    print(f"\nTask {i}: {task[:40]}...")
    for a in agents:
        print(f"  → {a.name} ({a.role}): score={sum(1 for c in a.capabilities if c.lower() in task.lower())}")

print("\nSwarm stats:", agent.swarm.stats())
