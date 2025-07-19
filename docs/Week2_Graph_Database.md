# Week 2: Loading the Graph Database

**Objective:** By the end of this week, your serverless pipeline will load the transformed data directly into a free-tier graph database.

---

### Step 1: Set Up Your Graph Database
* **Action:** Sign up for a free **Neo4j AuraDB** instance. When setting it up, choose Google Cloud as the provider and a nearby region.
* **Action:** Securely save your database username, password, and connection URI.

### Step 2: Store Credentials Securely
* **Action:** In **Google Secret Manager**, create a new secret to store your Neo4j password.
* **Action:** Grant your Cloud Function's Service Account the **"Secret Manager Secret Accessor"** role so it can read the password.

### Step 3: Update and Redeploy Your Cloud Function
* **Action:** In your `cloud_function/requirements.txt` file, add the `neo4j` library.
* **Action:** Modify your `cloud_function/main.py` script. The final step of the function will now:
    1.  Securely access the Neo4j credentials from Secret Manager.
    2.  Connect to your Neo4j AuraDB instance.
    3.  Load the transformed pandas DataFrame into the graph using Cypher queries (e.g., `MERGE` commands) to create your `Company`, `Project`, and `CarbonReport` nodes.
* **Action:** Re-deploy your Cloud Function with the updated code and dependencies. Trigger it and verify that the data appears in your Neo4j Browser.