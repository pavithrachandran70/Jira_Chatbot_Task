
import json
import random
from datetime import datetime, timedelta

async def dfa_node(state, last_n_sprints=5):
    """
    DFA = Data Formatting Agent
    - Converts raw Jira data into structured, cleaned, and DATE-BASED format for charts.
    - For velocity charts, automatically handles the last N sprints.
    """
    print("--- 3. Executing DFA (Data Formatting Agent) ---")

    structured_query = state.get("structured_query", {})
    chart_type = structured_query.get("chart_type", "none")
    jira_raw = state.get("jira_data", "")

    try:
        jira_data = json.loads(jira_raw) if isinstance(jira_raw, str) else jira_raw
    except:
        jira_data = jira_raw

    if chart_type == "none":
        return state 

    issues = jira_data.get("issues", []) if isinstance(jira_data, dict) else jira_data
    total_scope = sum(
        issue.get("fields", {}).get("customfield_10016", 0)
        for issue in issues if isinstance(issue, dict)
    )


    start_date = datetime.strptime("2023-04-06", "%Y-%m-%d")
    end_date = datetime.strptime("2023-04-13", "%Y-%m-%d")
    sprint_days = (end_date - start_date).days + 1
    date_list = [start_date + timedelta(days=i) for i in range(sprint_days)]


    mock_daily_sp = [0] + random.choices([0, 2, 3, 5, 8], k=sprint_days - 1)
    cumulative_completed = []
    current_sp = 0
    for daily_sp in mock_daily_sp:
        current_sp += daily_sp
        cumulative_completed.append(min(current_sp, 22)) 

    cleaned_data = {
        "total_scope": total_scope if total_scope > 0 else 25,
        "sprint_dates": [d.strftime("%Y-%m-%d") for d in date_list],
        "cumulative_completed": cumulative_completed,
        "chart_type": chart_type
    }

    if chart_type == "velocity":
        velocity_data = {
            "sprints": [f"Sprint {i}" for i in range(last_n_sprints)],
            "completed_points": [random.randint(10, 25) for _ in range(last_n_sprints)]
        }

        if cumulative_completed:
            velocity_data["completed_points"][-1] = cumulative_completed[-1]

        cleaned_data["velocity_data"] = velocity_data

    state["retrieved_visualization_data"] = cleaned_data
    return state