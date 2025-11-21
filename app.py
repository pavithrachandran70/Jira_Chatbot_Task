
import streamlit as st
import asyncio
import os

from Query_agent import qia_node
from retrival_agent import dra_node
from Data_formatting import dfa_node
from visualization_agent import dva_node


async def run_pipeline(user_input: str):
    state = {
        "user_input": user_input,
        "structured_query": {},
        "jira_data": "",
        "retrieved_visualization_data": None,
        "visualization_path": None,
        "stop_pipeline": False,
    }

    # 1) QIA
    st.write("### 🔍 1. Query Interpretation Agent (QIA)")
    result = qia_node(state)
    state.update(result)
    st.json(state["structured_query"])

    # 2) DRA
    st.write("### 🗄️ 2. Data Retrieval Agent (DRA)")
    state = await dra_node(state)

    if isinstance(state.get("jira_data"), dict) and state["jira_data"].get("error"):
        st.error("Jira Retrieval Error: " + state["jira_data"]["error"])
        return state

    st.write("**Raw Jira Data:**")
    st.write(state["jira_data"])

    # For non-chart queries, stop early
    if state["structured_query"].get("chart_type") == "none":
        st.info("ℹ️ No chart required for this query.")
        return state

    # 3) DFA
    st.write("### 🧹 3. Data Formatting Agent (DFA)")
    state = await dfa_node(state)
    st.json(state["retrieved_visualization_data"])

    # 4) DVA
    st.write("### 📊 4. Data Visualization Agent (DVA)")
    state = await dva_node(state)

    # Show chart if available
    if state.get("visualization_path") and os.path.exists(state["visualization_path"]):
        st.success("Chart generated successfully!")
        st.image(state["visualization_path"])
    else:
        st.warning("No visualization created.")

    return state


st.set_page_config(page_title="Jira AI Assistant", page_icon="🚀", layout="wide")
st.title("🚀 Jira AI Assistant (Streamlit Version)")
st.write("Ask me anything about Jira Sprints, Reports, Charts, and Issue Data!")

user_input = st.text_area("Enter your Jira request:", height=100)

if st.button("Run Pipeline"):
    st.info("Running Pipeline...")

    # Streamlit is NOT async -> we must run async code safely
    result = asyncio.run(run_pipeline(user_input))
