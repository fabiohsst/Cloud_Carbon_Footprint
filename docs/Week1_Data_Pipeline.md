# Week 1: The Serverless ETL Pipeline

**Objective:** By the end of this week, you will have a cost-effective, automated data pipeline using serverless GCP services. This pipeline will read your mock data and prepare it for loading.

---

### Step 1: Clean Up the Old Airflow Environment
The local Airflow setup is no longer needed for deployment. This simplifies your project significantly.

* **Action:** From your project's root folder (`Cloud_Carbon_Footprint/`), delete the following files and folders:
    * The entire `airflow/` directory (you can keep a copy of your DAG file, `carbon_footprint_pipeline.py`, as we will reuse its Python code).
    * The root `Dockerfile`.
    * The root `requirements.txt`.

### Step 2: Set Up Your Serverless Foundation
* **Action:** In the GCP Console, create a **Cloud Storage** bucket. This has a generous free tier and will store your data files.
* **Action:** Upload your two mock data files (`mock_aws_footprint.csv` and `mock_gcp_footprint.csv`) into this new bucket.

### Step 3: Develop Your Cloud Function
This will be your new ETL engine, replacing the Airflow DAG.

* **Action:** In your project, create a new folder named `cloud_function/`.
* **Action:** Inside `cloud_function/`, create two files: `main.py` and `requirements.txt`.
* **Action:** In `main.py`, create a Python function. **Copy the data transformation logic** from your old `carbon_footprint_pipeline.py` file into this function. You will use the `pandas` library as before.
* **Action:** Modify the "Extract" part of your code to read the CSVs from your Cloud Storage bucket instead of a local file path.
* **Action:** In the new `requirements.txt` file, add the necessary libraries:
    ```
    pandas
    gcsfs
    ```

### Step 4: Deploy and Schedule Your Pipeline
* **Action:** Deploy your function to **Google Cloud Functions** using the `gcloud` command line. You will give it an HTTP trigger so you can test it easily.
* **Action:** In the GCP Console, navigate to **Cloud Scheduler**. Create a new job that calls your Cloud Function's trigger URL on a daily schedule (e.g., every day at 2 AM). This replaces the Airflow scheduler and is free.