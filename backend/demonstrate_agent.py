import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from agents.skills.VectorIndexHealthCheck import check_qdrant_health

load_dotenv()

# Wrap the tool with @function_tool if not already decorated (it wasn't in the file I wrote)
# But wait, I can just import function_tool and decorate a wrapper or pass it directly if it has type hints.
# The check_qdrant_health in VectorIndexHealthCheck.py is a plain function. 
# Let's create a wrapper or just register it.

@function_tool
def check_health_tool() -> dict:
    """
    Checks the health of the Qdrant vector database and returns collection statistics.
    """
    return check_qdrant_health()

async def main():
    print("--- Qdrant Maintenance Agent Demonstration (OpenAI Agents) ---")
    
    agent = Agent(
        name="Qdrant Admin",
        instructions="You are a helpful agent responsible for maintaining the vector database. When asked about the database status, use the check_health_tool to get the latest information and report it to the user.",
        tools=[check_health_tool],
        model="gpt-4o",
    )

    query = "Check the health of the vector database and tell me how many chunks are stored."
    print(f"User: {query}")
    
    result = await Runner.run(agent, input=query)
    print(f"Agent: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())