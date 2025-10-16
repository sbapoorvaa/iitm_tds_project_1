from flask import Blueprint, request, jsonify
from llm_generator import generate_code_and_push
from config import STUDENT_SECRET

task_bp = Blueprint("task", __name__)

@task_bp.route("/task", methods=["POST"])
def create_task():
    data = request.json
    email = data.get("email")
    secret = data.get("secret")
    brief = data.get("brief")

    if secret != STUDENT_SECRET:
        return jsonify({"error": "Invalid secret"}), 403

    # Generate code and push to GitHub
    files = generate_code_and_push(brief)

    return jsonify({
        "email": email,
        "task": brief,
        "files": files
    })
