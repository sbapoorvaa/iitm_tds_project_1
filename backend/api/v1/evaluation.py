from flask import Blueprint, request, jsonify
from ...database import update_task_result  # Adjusted to absolute import

evaluation_bp = Blueprint("evaluation", __name__)

@evaluation_bp.route("/evaluate", methods=["POST"])
def evaluate_task():
    """
    Endpoint to receive evaluation results for a task.
    Expects JSON payload:
    {
        "task_id": "<task_id>",
        "result": "<result>"
    }
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    task_id = data.get("task_id")
    result = data.get("result")

    if not task_id or result is None:
        return jsonify({"error": "Missing task_id or result"}), 400

    try:
        update_task_result(task_id, result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Task evaluated successfully"}), 200
