# Week 3: Querying the Unified Carbon Footprint

**Objective:** By the end of this week, you will have built an LLM-powered agent that can query your multi-cloud graph database to answer complex questions about your total carbon footprint.

---

### Step 1: Set Up the Local Project
* **Action:** In your project's root, create a new folder named `dashboard/`.
* **Action:** Inside `dashboard/`, create a `requirements.txt` file for your front-end application. Add `streamlit`, `langchain`, `langchain-google-vertexai`, and `neo4j`.
* **Action:** Create your main application script, e.g., `dashboard/app.py`.

### Step 2: Build the LangChain Agent
* **Action:** In `app.py`, write the Python code to set up your LangChain agent.
* **Action:** Use the `GraphCypherQAChain` from LangChain.
* **Action:** Configure the chain to connect to your **Neo4j AuraDB** instance and a Google LLM (e.g., Gemini) via **Vertex AI**.

### Step 3: Test Multi-Cloud Queries
* **Action:** From your local machine, run your Python script (`streamlit run dashboard/app.py`) to test the agent and the simple UI. Ask it questions that require combining data from both mock sources, for example:
    * *"What is our total cloud carbon footprint for PaySydney Pty Ltd?"*
    * *"Compare the emissions from our GCP production project to our AWS analytics project."*