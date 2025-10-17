from flask import Blueprint, request, jsonify
from database import update_prompt_result, insert_result, get_prompt_by_repo_url, get_prompt

evaluation_bp = Blueprint("evaluation", __name__)

@evaluation_bp.route("/evaluate", methods=["POST"])
def evaluate_task():
    """
    Endpoint to receive evaluation results for a task.
    Expects JSON payload:
    {
        "task_id": "<task_id>",  # optional if repo_url is given for round 1
        "round": 1 or 2,
        "repo_url": "<repo_url>", # required for round 2 or existing repo in round 1
        "result": {
            "commit_sha": "<commit_sha>",
            "pages_url": "<pages_url>",
            "score": <score>,
            "feedback": "<feedback>"
        }
    }
    """
    data = request.json
    print("Received evaluation data:", data)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    round_no = data.get("round")
    repo_url = data.get("repo_url")
    result = data.get("result")
    task_id = data.get("task_id")

    if not round_no or not result:
        return jsonify({"error": "Missing round or result"}), 400

    try:
        # Determine task_id if repo_url provided for round 1
        if round_no == 1 and repo_url and not task_id:
            prompt = get_prompt_by_repo_url(repo_url)
            if not prompt:
                return jsonify({"error": "No prompt found for this repo"}), 400
            task_id = prompt["task_id"]

        elif round_no == 2:
            if not repo_url:
                return jsonify({"error": "repo_url required for round 2"}), 400

            # Ensure Round 1 exists
            r1_prompt = get_prompt_by_repo_url(repo_url, round_no=1)
            if not r1_prompt:
                return jsonify({"error": "Round 1 for this repo does not exist"}), 400

        # Update prompts table if task_id exists
        prompt = get_prompt(task_id) if task_id else None
        print("Fetched prompt for update:", prompt)
        if prompt:
            update_data = {"status": "completed","score": result.get("score"),"feedback": result.get("feedback")}
            update_prompt_result(task_id, update_data)

        # Insert into results table
        insert_result(
            task_id=task_id,
            email=prompt["email"] if prompt else None,
            task=prompt["task"] if prompt else None,
            round_no=round_no,
            nonce=prompt["nonce"] if prompt else None,
            repo_url=repo_url,
            commit_sha=result.get("commit_sha"),
            pages_url=result.get("pages_url")
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Task evaluation stored successfully"}), 200
