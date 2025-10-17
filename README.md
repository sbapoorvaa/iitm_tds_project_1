# Automated Code Evaluation System  
**TDS Take Home Project 1**

A robust backend system for automating **code generation, evaluation, and task management** using large language models, GitHub integration, and Supabase as the persistent database.

---

## Overview

This project implements a full **end-to-end automated evaluation workflow** for coding tasks.  

It supports:
- Task creation via API
- LLM-based code generation
- GitHub repository creation, commit management, and GitHub Pages deployment
- Multi-round automated evaluation
- Storage of prompts, results, and evaluation metadata in Supabase

The system is designed for reproducibility, scalability, and ease of evaluation for take-home coding tasks.

---

## Architecture

                ┌───────────────────────┐
                │     Task Requester    │
                │  (API / Frontend)     │
                └──────────┬────────────┘
                           │
                           ▼
                ┌───────────────────────┐
                │     Flask Backend     │
                │ ───────────────────── │
                │ /api/v1/task          │  →  Generate & submit tasks
                │ /api/v1/evaluate      │  →  Receive evaluation results
                └──────────┬────────────┘
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
         ┌─────────────────┐ ┌─────────────────────┐
         │ GitHub Utility  │ │ Supabase Database   │
         │ (repo, pages)   │ │ (prompts/results)   │
         └─────────────────┘ └─────────────────────┘
          │
          ▼
         ┌───────────┐
         │ Evaluator │
         │ Round 1/2 │
         └───────────┘

---

## Project Structure

backend/
├── api/v1/
│ ├── task.py # Task creation & code generation
│ ├── evaluation.py # Evaluation callbacks
│
├── app.py # Flask server entry point
├── config.py # Environment & constants
├── database.py # Supabase CRUD logic
├── github_utils.py # GitHub repo, commit, and Pages logic
├── llm_generator.py # LLM code generation
│
evaluate/
├── evaluate.py # Common evaluation flow
├── round1.py # Round 1 evaluation script
├── round2.py # Round 2 evaluation script
│
.env # Environment config

---

## Workflow

### 1. Task Generation
1. `POST /api/v1/task` receives a task request (task type, user info, round number).  
2. Backend generates code using the LLM.  
3. GitHub repository is created for the task.  
4. Generated code files are committed and optionally deployed via GitHub Pages.  
5. Task metadata is stored in **Supabase** in `prompts` and `results` tables.

### 2. Evaluation
1. Once code is committed/deployed, backend triggers the evaluation workflow.  
2. Evaluator scripts (`round1.py`, `round2.py`) clone the repo and run tests.  
3. Evaluation results (score, feedback, commit SHA, GitHub Pages URL) are stored back in Supabase.  
4. Optional callback URL can be notified with the results for downstream processing.

---

## Database Schema

### `prompts`

| Column | Type | Description |
|--------|------|-------------|
| id | int (PK) | Auto-increment |
| task_id | int | Unique task identifier |
| email | text | User email |
| task | text | Task description or type |
| nonce | text | Unique identifier for evaluation |
| files | jsonb | Generated code files |
| status | text | Task status (“created”, “evaluating”, “completed”) |

### `results`

| Column | Type | Description |
|--------|------|-------------|
| id | int (PK) | Auto-increment |
| task_id | int | References task from `prompts` |
| email | text | User email |
| round | int | Evaluation round number |
| repo_url | text | GitHub repository URL |
| commit_sha | text | Latest commit SHA |
| pages_url | text | GitHub Pages deployment URL |
| files | jsonb | Generated code files |
| evaluation_url | text | Optional callback URL |
| status | text | "completed" or "evaluated" |

---

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/<your-username>/iitm_tds_project_1.git
cd iitm_tds_project_1
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows
```

### 3. Install Dependancies
```bash
pip install -r requirements.txt
```

### 4. Add Environment variables 
```env
SUPABASE_URL=<your_supabase_url>
SUPABASE_KEY=<your_supabase_key>
GITHUB_TOKEN=<your_github_token>
AIPIPE_API_KEY=<your_aipipe_api_key>
RESULTS_TABLE=results
PROMPTS_TABLE=prompts
```

### 5. Run Flask Server
```bash
python backend/app.py
```

## Future Improvements

- Add async job queue (Celery + Redis) for scalable evaluation.
- Build a frontend dashboard for task management and visualization.
- Extend evaluation metrics with detailed automated feedback.
- Enhanced logging, error reporting, and monitoring.

## Sample Tester File
```json
{
  "email": <email_here>,
  "name": <name_here>,
  "secret": <your_secret_here>,
  "task": <one-liner-about-task>,
  "round": <round-number: int>,
  "nonce": <nonce-here>,
  "brief": <a-brief-description-of-what-needs-to-be-done>,
  "checks": <list-of-checks-to-be-performed>,
  "evaluation_url": <url-to-evaluate-the-git-commit: optional>
}
```
