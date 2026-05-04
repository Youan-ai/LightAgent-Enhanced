"""
Example 3: Memory persistence
"""
from lightagent import LightAgent
import json

agent = LightAgent()
agent.initialize()

# Store data
agent.memory.put("user_name", "Alice")
agent.memory.put("user_age", 30)
agent.memory.put("session_id", "abc-123-xyz")
agent.memory.put("preferences", {"theme": "dark", "lang": "en"})

# Retrieve
print("User name:", agent.memory.get("user_name"))
print("All keys:", agent.memory.keys())

# Search
print("Search 'user':", agent.memory.search("user"))

# Persist
snapshot = agent.memory.snapshot()
with open("memory_backup.json", "w") as f:
    json.dump(snapshot, f, indent=2)
print("Saved snapshot to memory_backup.json")

# Restore into new agent
agent2 = LightAgent()
agent2.memory.restore(snapshot)
print("Restored user_name:", agent2.memory.get("user_name"))
