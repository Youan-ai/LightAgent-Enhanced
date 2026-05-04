"""
Example 1: Basic tool registration and execution
"""
from lightagent import tool, LightAgent

@tool(name="greet", description="Say hello to someone")
def greet(name: str, excited: bool = False) -> str:
    greeting = f"Hello, {name}!"
    return greeting.upper() if excited else greeting

@tool(name="add", description="Add two numbers")
def add(a: float, b: float) -> float:
    return a + b

@tool(name="reverse", description="Reverse a string")
def reverse(text: str) -> str:
    return text[::-1]

agent = LightAgent()
agent.tools.register(greet)
agent.tools.register(add)
agent.tools.register(reverse)
agent.initialize()

# Execute tools
print(agent.execute_sync("greet", name="World", excited=True))
print(agent.execute_sync("add", a=42, b=10))
print(agent.execute_sync("reverse", text="LightAgent"))

# Check stats
print("\nTool stats:", agent.tools.stats())
