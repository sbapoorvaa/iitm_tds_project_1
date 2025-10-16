from flask import Blueprint, request, jsonify
from backend.llm_generator import generate_code_and_push  # absolute import
from backend.config import STUDENT_SECRET  # absolute import

task_bp = Blueprint("task", __name__)

@task_bp.route("/task", methods=["POST"])
def create_task():
    """
    Endpoint to create a new task, generate code using LLM, and push to GitHub.
    Expects JSON payload:
    {
        "email": "<student_email>",
        "secret": "<student_secret>",
        "brief": "<app_brief>"
    }
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get("email")
    secret = data.get("secret")
    brief = data.get("brief")

    if not email or not secret or not brief:
        return jsonify({"error": "Missing email, secret, or brief"}), 400

    if secret != STUDENT_SECRET:
        return jsonify({"error": "Invalid secret"}), 403

    try:
        # Generate code and push to GitHub
        files = generate_code_and_push(brief)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "email": email,
        "task": brief,
        "files": files
    }), 200
