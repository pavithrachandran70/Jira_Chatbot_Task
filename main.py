import asyncio
from Query_agent import qia_node
from retrival_agent import dra_node
from Data_formatting import dfa_node
from visualization_agent import dva_node

async def run_pipeline(user_input: str):
    """
    Full pipeline: 
    QIA → DRA → (stop for non-charts) → DFA → DVA
    """
    state = {
        "user_input": user_input,
        "structured_query": {},
        "jira_data": "",
        "retrieved_visualization_data": None,
        "visualization_path": None,
        "stop_pipeline": False,
    }

    print("\n==============================")
    print("Starting Jira AI Pipeline")
    print("==============================")

    result = qia_node(state)
    state.update(result)

    state = await dra_node(state)

    if isinstance(state.get("jira_data"), dict) and state["jira_data"].get("error"):
        print("\nJira Retrieval Error:")
        print(state["jira_data"]["error"])
        return state

    chart_type = state["structured_query"].get("chart_type", "none")

    if chart_type == "none":
        print("\n Final (Non-chart) Response:")
        print(state["jira_data"])
        return state

    state = await dfa_node(state)

    state = await dva_node(state)

    if state.get("visualization_path"):
        print("\n📊 Chart generated:", state["visualization_path"])
    else:
        print("\n⚠ No visualization generated.")

    return state


async def main():
    while True:
        user_input = input("\nEnter Jira request (or 'exit'): ")

        if user_input.lower().strip() == "exit":
            print("Goodbye!")
            break

        await run_pipeline(user_input)


if __name__ == "__main__":
    asyncio.run(main())
