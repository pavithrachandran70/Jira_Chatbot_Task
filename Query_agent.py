



import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv 
import os

load_dotenv() 
api_key = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
)
# ... imports ...

template = """
You are a Query Interpretation Agent.
Convert the user's query into STRICT valid JSON.

User Query: {query}

JSON Schema:
{{
  "chart_type": "burndown",  // Options: "burndown", "burnup", "velocity", "none" (use "none" for lists, status checks, or general questions)
  "project_name": "PROJECT_KEY_HERE",
  "sprint_range": "SPRINT_NAME_OR_ID", 
  "time_frame": "",
  "issue_type": "",
  "additional_filters": {{}}
}}

RULES:
1. Extract 'project_name' (e.g., "BC74").
2. Extract 'sprint_range'. If user says "Sprint 0", output "0" or "Sprint 0".
3. If the user asks to "list", "show tickets", "what is", or "summarize", set "chart_type" to "none".
4. Output JSON ONLY. No markdown.
"""



def qia_node(state):
    print("--- 1. Executing QIA (Query Interpretation Agent) ---")
    user_query = state["user_input"]
    prompt_text = template.format(query=user_query)

    response = llm.invoke([HumanMessage(content=prompt_text)])
    json_text = response.content.strip()

    # Remove markdown
    json_text = json_text.replace("```json", "").replace("```", "").strip()

    # Extract JSON only
    start = json_text.find("{")
    end = json_text.rfind("}") + 1
    if start != -1 and end != -1:
        json_text = json_text[start:end]

    try:
        parsed = json.loads(json_text)
    except Exception as e:
        print(f"[QIA] JSON Parsing failed: {e}")
        parsed = {}

    final_parsed = {
        "chart_type": parsed.get("chart_type", "burndown"),
        "project_name": parsed.get("project_name", ""),
        "sprint_range": parsed.get("sprint_range", ""),
        "time_frame": "",
        "issue_type": "",
        "additional_filters": {}
    }

    print(f"[QIA] Extracted: {json.dumps(final_parsed, indent=2)}")
    return {"structured_query": final_parsed}
