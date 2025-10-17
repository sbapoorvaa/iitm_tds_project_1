from flask import Blueprint, request, jsonify
from llm_generator import generate_code_and_push, post_with_retry  
from database import insert_prompt, get_prompt_by_repo_url, insert_result
from config import STUDENT_SECRET
import uuid

task_bp = Blueprint("task", __name__)

@task_bp.route("/task", methods=["POST"])
def create_task():
    """
    Endpoint to create a new task.
    Expects JSON payload:
    {
        "email": "<student_email>",
        "name": "<student_name>",
        "secret": "<student_secret>",
        "brief": "<app_brief>",
        "checks": [...],           # optional
        "evaluation_url": "<url>", # optional
        "attachments": {...},      # optional
        "round": 1 or 2,
        "repo_url": "<existing_repo>" # optional for round 1
    }
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get("email")
    name = data.get("name")
    secret = data.get("secret")
    brief = data.get("brief")
    checks = data.get("checks")
    evaluation_url = data.get("evaluation_url")
    attachments = data.get("attachments")
    round_no = data.get("round")
    repo_url = data.get("repo_url")

    if not email or not secret or not brief or not name or not round_no:
        return jsonify({"error": "Missing required fields"}), 400

    if secret != STUDENT_SECRET:
        return jsonify({"error": "Invalid secret"}), 403

    # Generate unique nonce
    nonce = str(uuid.uuid4())

    try:
        prompt_id = None
        pages_url = None
        commit_sha = None
        files = None

        if round_no == 1:
            if not repo_url:
                # Insert into prompts table (new repo)
                prompt = insert_prompt(
                    email=email,
                    name=name,
                    secret=secret,
                    task=brief,
                    round_no=1,
                    nonce=nonce,
                    brief=brief,
                    checks=checks,
                    evaluation_url=evaluation_url,
                    attachments=attachments
                )
                prompt_id = prompt["task_id"]

            # Generate code and push (either existing repo or new)
            gen_result = generate_code_and_push(
                brief=brief,
                repo_name=f"task-{prompt_id}" if prompt_id else None,
                attachments=attachments,
                checks=checks,
                name=name,
                email=email,
                task=brief,
                repo_url=repo_url
            )
            repo_url = gen_result["repo_url"]
            pages_url = gen_result["pages_url"]
            commit_sha = gen_result["commit_sha"]
            files = gen_result["files"]

            # Save to results table
            insert_result(
                task_id=prompt_id,
                email=email,
                task=brief,
                round_no=1,
                nonce=nonce,
                repo_url=repo_url,
                commit_sha=commit_sha,
                files=files,
                pages_url=pages_url
            )
            

# Notify evaluation_url after round 1
        if evaluation_url:
            payload = {
                "task_id": prompt_id,
                "round": round_no,
                "repo_url": repo_url,
                "result": {
                    "commit_sha": commit_sha,
                    "pages_url": pages_url,
                    "score": None,     # optional
                    "feedback": None   # optional
                }
            }
            post_with_retry(evaluation_url, payload)


        elif round_no == 2:
            if not repo_url:
                return jsonify({"error": "repo_url required for round 2"}), 400

            # Ensure Round 1 exists by checking prompts table for same repo_url
            r1_prompt = get_prompt_by_repo_url(repo_url)
            if not r1_prompt:
                return jsonify({"error": "Round 1 for this repo does not exist"}), 400

            # Insert prompt for round 2
            prompt = insert_prompt(
                email=email,
                name=name,
                secret=secret,
                task=brief,
                round_no=2,
                nonce=nonce,
                brief=brief,
                checks=checks,
                evaluation_url=evaluation_url,
                attachments=attachments,
                repo_url=repo_url
            )
            prompt_id = prompt["task_id"]

            # Modify repo according to brief
            gen_result = generate_code_and_push(
                brief=brief,
                attachments=attachments,
                checks=checks,
                name=name,
                email=email,
                task=brief,
                repo_url=repo_url
            )
            repo_url = gen_result["repo_url"]
            pages_url = gen_result["pages_url"]
            commit_sha = gen_result["commit_sha"]
            files = gen_result["files"]

            # Save to results table
            insert_result(
                task_id=prompt_id,
                email=email,
                task=brief,
                round_no=2,
                nonce=nonce,
                repo_url=repo_url,
                commit_sha=commit_sha,
                files=files,
                pages_url=pages_url
            )

        else:
            return jsonify({"error": "Invalid round number"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Return JSON with repo_url, pages_url, commit_sha, files
    return jsonify({
        "task_id": prompt_id,
        "email": email,
        "name": name,
        "nonce": nonce,
        "task": brief,
        "files": files,
        "evaluation_url": evaluation_url,
        "repo_url": repo_url,
        "pages_url": pages_url,
        "commit_sha": commit_sha
    }), 200
