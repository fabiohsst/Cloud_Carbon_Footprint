# Week 4: The Serverless Dashboard & Strategic Positioning

**Objective:** This week, you will package your project into a polished, public-facing web application hosted on Google Cloud that scales to zero to remain free.

---

### Step 1: Create a Dockerfile for the Dashboard
* **Action:** Inside your `dashboard/` folder, create a new `Dockerfile`.
* **Action:** This `Dockerfile` will be simple: it will start from a base Python image, copy your `dashboard/` code and `requirements.txt` file, and install the dependencies.

### Step 2: Deploy Your Dashboard to Cloud Run (Scale-to-Zero)
* **Action:** Build your dashboard's Docker image and push it to **Google Artifact Registry**.
* **Action:** Deploy the image as a new service on **Cloud Run**.
* **Action (CRITICAL FOR COST):** In the deployment configuration, set the **minimum instances to 0** and the maximum to a low number like `2`. This ensures the service "sleeps" when not in use and you are not billed for idle time.
* **Action:** Configure the Cloud Run service to securely access your Neo4j credentials from **Secret Manager**, just like you did for the Cloud Function.
* **Action:** Set the service to be **publicly accessible**.

### Step 3: Create a Professional GitHub Showcase
* **Action:** Create your `README.md` file, including an architecture diagram that now shows Cloud Scheduler, Cloud Functions, and a scale-to-zero Cloud Run service.

### Step 4: Craft Your Resume and Interview Narrative
* **Action:** Update your resume to highlight your experience with a modern, event-driven, **serverless architecture on GCP**, which is a highly in-demand skill set.