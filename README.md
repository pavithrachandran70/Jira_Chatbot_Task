# 🚀 Jira AI Assistant (Streamlit + LangChain + MCP + Gemini)

An intelligent **Jira data analysis assistant** built using:

* **Google Gemini 2.5 Flash** (LLM)
* **LangChain Agents**
* **MCP (Model Context Protocol)** for real Jira retrieval
* **Docker-based Jira MCP server**
* **Streamlit** user interface
* **Python async pipeline** (QIA → DRA → DFA → DVA)
* **Matplotlib** charts for burndown, burnup, and velocity

This project turns natural-language Jira questions into **structured queries**, fetches real Jira data, cleans it, and generates **visual charts**.

---

## 📁 Project Architecture

```
Jira AI Pipeline
│
├── 1. Query_agent.py          → Query Interpretation (QIA)
├── 2. retrival_agent.py        → Real Jira Retrieval via MCP + Docker (DRA)
├── 3. Data_formatting.py       → Clean + Transform Jira Data (DFA)
├── 4. visualization_agent.py   → Generate Burnup/Velocity Charts (DVA)
│
└── app.py (or Streamlit UI)    → Frontend (User queries → Charts)
```

---

## 🔥 Core Pipeline

The system uses a **4-agent pipeline**:

### **1️⃣ QIA — Query Interpretation Agent**

* Converts natural language into STRICT JSON
* Extracts:
  ✔ project key
  ✔ sprint ID
  ✔ chart type (burnup, velocity, none)
* Ensures clean, always-parseable JSON

---

### **2️⃣ DRA — Data Retrieval Agent**

* Uses **LangChain MCP client**
* Runs **Docker container**:

  ```
  ghcr.io/sooperset/mcp-atlassian
  ```
* Passes env variables:

  * `JIRA_URL`
  * `JIRA_EMAIL`
  * `JIRA_API_TOKEN`
* Fetches real Jira issue data from the API

---

### **3️⃣ DFA — Data Formatting Agent**

* Converts Jira raw JSON into chart-friendly, date-based datasets
* Normalizes fields
* Generates synthetic daily burnup values for demo mode
* Generates last N sprint velocity data

---

### **4️⃣ DVA — Visualization Agent**

Creates charts:

📈 **Burnup Chart**
📊 **Velocity Chart**

Saved in:

```
/charts/{project}_sprint_{id}_{chart}.png
```

---

## 🖥️ Streamlit UI

The app provides a rich UI:

* Step-by-step execution logs
* JSON visualization for each stage
* Raw Jira data preview
* Auto-rendered charts

Run it via:

```
streamlit run app.py
```

---

## ⚙️ Installation

### **1. Clone the repository**

```
git clone <your-repo>
cd <project-folder>
```

### **2. Install dependencies**

```
pip install -r requirements.txt
```

### **3. Install & Enable Docker**

Required for running MCP Jira agent.

---

## 🔐 Environment Variables

Create a **.env** file:

```
GEMINI_API_KEY=your_api_key
JIRA_URL=https://yourdomain.atlassian.net
JIRA_EMAIL=your_email
JIRA_API_TOKEN=your_jira_api_token
```

Make sure Docker Desktop is running.

---

## ▶️ Running the Application

### Option A — Run the full pipeline (console)

```
python pipeline.py
```

### Option B — Run Streamlit UI

```
streamlit run app.py
```

---

## 📝 Example Queries

Try:

* `Plot a burnup chart for Sprint 5 of BC74`
* `Show velocity for last 5 sprints of BC74`
* `List all bugs in project BC74`
* `Show completed story points for Sprint 10`
* `What issues are pending in Sprint 3 of BC74?`

---

## 🧪 Sample Output

### ✔ JSON (after QIA)

```json
{
  "chart_type": "velocity",
  "project_name": "BC74",
  "sprint_range": "Sprint 5",
  "time_frame": "",
  "issue_type": "",
  "additional_filters": {}
}
```

### ✔ Velocity Chart Example

Image saved as:

```
charts/bc74_sprint_5_velocity.png
```

---

## 🐳 MCP (Docker) Notes

Jira data retrieval uses:

```
ghcr.io/sooperset/mcp-atlassian:latest
```

Run automatically by DRA:

```
docker run -i --rm 
  -e JIRA_URL 
  -e JIRA_USERNAME 
  -e JIRA_API_TOKEN 
  ghcr.io/sooperset/mcp-atlassian:latest
```

If Docker is blocked or API key is leaked, you may see:

⚠ **403 Your API key was reported as leaked**
Fix by regenerating new tokens.

---

## 🛠️ Troubleshooting

### ❗ DRA error: *“No Jira tools found in MCP”*

→ Docker container didn’t start
→ Check Docker Desktop is running

### ❗ JSON parsing failed in QIA

→ Gemini returned Markdown
→ Auto-stripping is included but ensure template rules remain strict

### ❗ Chart not showing in Streamlit

→ Check folder:

```
/charts
```

### ❗ Streamlit async error

Handled using:

```
asyncio.run()
```

---

## 📌 Future Improvements

* Real burndown chart (remaining SP per day)
* Sprint list auto-fetch from Jira
* Replace mock burnup data with true history
* Multi-project dashboard
* LLM fallback if Jira API unavailable

<img width="409" height="648" alt="image" src="https://github.com/user-attachments/assets/63f889fd-b046-4b7f-ab62-6063d26176f3" />

