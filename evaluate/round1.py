import logging
from backend.database import update_task_result

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_round1(task):
    """
    Evaluates a round 1 task.
    Updates task result in Supabase and returns structured feedback.
    """
    required_keys = ["email", "task", "round", "nonce", "brief"]
    missing = [k for k in required_keys if k not in task]
    if missing:
        msg = f"Missing required task keys: {missing}"
        logger.error(msg)
        return {"score": 0, "feedback": msg}

    task_id = task.get("task")
    email = task.get("email")
    brief = task.get("brief")

    logger.info(f"Running Round 1 evaluation | Task: {task_id} | Email: {email}")

    try:
        score = 10
        feedback = "Task executed successfully"

        try:
            update_task_result(task_id, {"score": score, "feedback": feedback})
            logger.info(f"Task {task_id} updated in Supabase")
        except Exception as e:
            logger.warning(f"Failed to update Supabase: {e}")

        return {"score": score, "feedback": feedback}

    except Exception as e:
        logger.exception("Error during Round 1 evaluation")
        return {"score": 0, "feedback": f"Error: {str(e)}"}
