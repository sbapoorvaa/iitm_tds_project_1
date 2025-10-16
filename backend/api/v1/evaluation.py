from flask import Blueprint, request, jsonify
from database import update_task_result

evaluation_bp = Blueprint("evaluation", __name__)

@evaluation_bp.route("/evaluate", methods=["POST"])
def evaluate_task():
    data = request.json
    task_id = data.get("task_id")
    result = data.get("result")

    update_task_result(task_id, result)

    return jsonify({"message": "Task evaluated successfully"})
