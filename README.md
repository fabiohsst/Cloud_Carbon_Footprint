# ☁️ Multi-Cloud Carbon Footprint Analyzer

An intelligent, serverless data application that ingests, unifies, and analyzes carbon footprint data from multiple cloud providers, allowing non-technical users to ask questions in plain English.

---

## 🚀 The Problem

As companies increasingly adopt multi-cloud strategies (using services from both AWS, Google Cloud, etc.), they gain flexibility but lose visibility. Carbon footprint data is siloed in each provider's separate reporting tools, making it impossible to get a single, unified view of their total cloud-based emissions. This project solves that problem.

## ✨ Key Features

* **Serverless ETL:** A fully automated, event-driven pipeline built on **Google Cloud Functions** and **Cloud Scheduler** that costs nothing for low-volume usage.
* **Multi-Cloud Unification:** Ingests and transforms carbon footprint reports from both AWS and GCP into a single, standardized model.
* **Knowledge Graph Database:** Models the complex relationships between the company, cloud providers, and their carbon reports using a **Neo4j AuraDB** graph database.
* **Natural Language Interface:** Leverages **LangChain** and the **OpenAI GPT-4o-mini** model to allow users to ask complex questions in plain English.
* **Interactive Dashboard:** A simple and intuitive web interface built with **Streamlit** and deployed for free on **Streamlit Community Cloud**.

## 🏗️ Architecture

This project is built on a modern, event-driven, and serverless architecture to ensure it is both powerful and cost-effective.

┌──────────────────────────┐      ┌───────────────────────────┐      ┌────────────────────────┐
│                          │      │                           │      │                        │
│   User (Web Browser)     ├─────►│  Streamlit Community Cloud  │      │   OpenAI API (LLM)     │
│                          │      │  (Public Dashboard)       │◄─────┤                        │
└──────────────────────────┘      │                           │      │                        │
                                  └─────────────┬─────────────┘      └────────────────────────┘
                                                │
                                                │ (Queries in Cypher)
                                                │
                                  ┌─────────────▼─────────────┐
                                  │                           │
                                  │   Neo4j AuraDB (Free Tier)  │
                                  │   (Graph Database)        │
                                  │                           │
                                  └─────────────▲─────────────┘
                                                │
                                                │ (Loads transformed data)
                                                │
┌──────────────────────────┐      ┌─────────────┴─────────────┐      ┌────────────────────────┐
│                          │      │                           │      │                        │
│ Cloud Scheduler (Trigger)├─────►│  Google Cloud Function    │◄─────┤ Google Cloud Storage   │
│ (e.g., "Run daily")      │      │  (ETL: Extract, Transform)  │      │ (Mock CSV Files)       │
│                          │      │                           │      │                        │
└──────────────────────────┘      └───────────────────────────┘      └────────────────────────┘

1.  **Data Storage:** Mock CSV reports for AWS and GCP are stored in a **Google Cloud Storage** bucket.
2.  **Scheduling:** A **Google Cloud Scheduler** job runs daily, triggering the ETL pipeline.
3.  **ETL Processing:** A **Google Cloud Function** written in Python is triggered by the scheduler. It uses the Pandas library to read the files from the bucket, transform the data, and unify the schemas.
4.  **Database:** The unified data is loaded directly into a free-tier **Neo4j AuraDB** instance.
5.  **Application Front-End:** A **Streamlit** application provides the user interface. It is deployed on **Streamlit Community Cloud**.
6.  **AI Agent:** The Streamlit app uses a **LangChain** agent to connect to the Neo4j database. When a user asks a question, the agent uses an **OpenAI LLM** to convert the question into a Cypher query, retrieve the answer from the database, and present it to the user.

## 🛠️ Tech Stack

* **Cloud Platform:** Google Cloud (Cloud Functions, Cloud Scheduler, Cloud Storage, Secret Manager)
* **Database:** Neo4j AuraDB (Graph Database)
* **Data Processing:** Python, Pandas
* **AI / LLM Framework:** LangChain, OpenAI
* **Front-End:** Streamlit
* **Deployment:** Streamlit Community Cloud, Git & GitHub

## ⚙️ Setup and Usage

To run this project locally, follow these steps:

1.  **Prerequisites:**
    * Python 3.9+ installed
    * A Google Cloud project with billing enabled
    * A Neo4j AuraDB Free Tier instance created
    * An OpenAI API Key

2.  **Clone the Repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

3.  **Set Up Credentials:**
    * Authenticate your local environment with Google Cloud:
        ```bash
        gcloud auth application-default login
        ```
    * In the `dashboard/` folder, create a `.env` file and add your credentials:
        ```
        NEO4J_URI="your-neo4j-uri"
        NEO4J_USERNAME="your-neo4j-username"
        NEO4J_PASSWORD="your-neo4j-password"
        OPENAI_API_KEY="sk-..."
        ```

4.  **Install Dependencies:**
    ```bash
    pip install -r dashboard/requirements.txt
    ```

5.  **Run the Application:**
    ```bash
    python -m streamlit run dashboard/app.py
    ```

## 💡 Example Questions

You can ask the analyzer questions like:
* "What is our total cloud carbon footprint?"
* "Compare the emissions from our GCP and AWS projects."
* "Which service had the highest scope 2 emissions in the first quarter?"