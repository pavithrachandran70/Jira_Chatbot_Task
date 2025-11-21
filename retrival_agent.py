# retrival_agent.py
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType

# Load environment variables
load_dotenv()

# Initialize the LLM
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

async def dra_node(state):
    """
    Data Retrieval Agent (DRA) Node.
    Uses the structured query to fetch Jira data via MCP agent.
    """
    print("--- 2. Executing DRA (Data Retrieval Agent) ---")
    
    structured_query = state.get("structured_query", {})
    user_query = state.get("user_input", "")

    project = structured_query.get("project_name")
    sprint_range = structured_query.get("sprint_range")
    if not project or not sprint_range:
        state["jira_data"] = {"error": "Project or Sprint missing from structured query."}
        return state

    # Initialize MCP client
    client = MultiServerMCPClient({
        "jira": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "-e", f"JIRA_URL={os.getenv('JIRA_URL')}",
                "-e", f"JIRA_USERNAME={os.getenv('JIRA_EMAIL')}",
                "-e", f"JIRA_API_TOKEN={os.getenv('JIRA_API_TOKEN')}",
                "ghcr.io/sooperset/mcp-atlassian:latest"
            ],
            "transport": "stdio",
        }
    })

    try:
        # Get available tools
        tools = await client.get_tools()
        print(f"[DRA] Found {len(tools)} Jira tools.")

        if not tools:
            state["jira_data"] = {"error": "No Jira tools found in MCP."}
            return state

        # Initialize structured agent
        agent = initialize_agent(
            tools=tools,
            llm=model,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False
        )

        # Use user query to fetch Jira data
        response = await agent.arun(user_query)
        state["jira_data"] = response
        print(f"[DRA] Data retrieved successfully (length: {len(str(response))})")

    except Exception as e:
        print(f"[DRA ERROR] {e}")
        state["jira_data"] = {"error": str(e)}

    finally:
        # Close the MCP client
        try:
            await client.close()
            print("[DRA] MCP client closed.")
        except:
            pass

    return state
