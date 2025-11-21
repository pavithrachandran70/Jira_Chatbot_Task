


import matplotlib.pyplot as plt
import os
import numpy as np

async def dva_node(state):
    """
    DVA = Visualization Agent
    Generates burnup, burndown, and velocity charts.
    """
    print("--- 4. Executing DVA (Visualization Agent) ---")

    if state.get("stop_pipeline"):
        print("[DVA] Pipeline stop flag detected — skipping visualization.")
        return state

    structured_query = state.get("structured_query", {})
    chart_type = structured_query.get("chart_type")
    sprint = structured_query.get("sprint_range")
    project = structured_query.get("project_name")

    data = state.get("retrieved_visualization_data", {})

    if not isinstance(data, dict):
        state["visualization_path"] = None
        return state

    plt.figure(figsize=(10, 6))

    if chart_type == "burnup":
        dates = data.get("sprint_dates", [])
        cumulative_completed = data.get("cumulative_completed", [])
        total_scope = data.get("total_scope", 0)

        plt.plot(dates, cumulative_completed, 
                 label='Work Completed', marker='o', color='blue')
        scope_line = np.full(len(dates), total_scope)
        plt.plot(dates, scope_line, label='Total Scope (Goal)', linestyle='--', color='red')

        plt.title(f"Burnup Chart - {project} Sprint {sprint}")
        plt.xlabel("Date")
        plt.ylabel("Story Points")
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.tight_layout()

    elif chart_type == "velocity":
        velocity_data = data.get("velocity_data", {})
        sprint_labels = velocity_data.get("sprints", [])
        completed_points = velocity_data.get("completed_points", [])

        plt.bar(sprint_labels, completed_points, color='teal')
        for idx, val in enumerate(completed_points):
            plt.text(idx, val + 0.5, str(val), ha='center', va='bottom', fontweight='bold')

        plt.title(f"Velocity Chart - {project} - Last {len(sprint_labels)} Sprints")
        plt.xlabel("Sprint")
        plt.ylabel("Completed Story Points")
        plt.grid(axis='y', linestyle=':', alpha=0.6)
        plt.tight_layout()

    else:
        state["visualization_path"] = None
        plt.close()
        return state

    # Save chart
    os.makedirs("charts", exist_ok=True)
    file_path = f"charts/{project.lower()}_sprint_{sprint.lower().replace(' ', '')}_{chart_type}.png"
    plt.savefig(file_path)
    plt.close()
    state["visualization_path"] = file_path
    print(f"[DVA] Chart saved to {file_path}")

    return state




