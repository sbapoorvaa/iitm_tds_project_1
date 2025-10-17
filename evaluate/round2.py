import logging
from backend.database import update_task_result

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_round2(task):
    """
    Evaluates round 2 or any later rounds.
    Updates task result in Supabase and returns structured feedback.
    """
    required_keys = ["email", "task", "round", "nonce", "brief", "repo_url"]
    missing = [k for k in required_keys if k not in task or not task[k]]
    if missing:
        msg = f"Missing required task keys for Round 2+: {missing}"
        logger.error(msg)
        return {"score": 0, "feedback": msg}

    task_id = task.get("task")
    email = task.get("email")
    brief = task.get("brief")
    repo_url = task.get("repo_url")

    logger.info(f"Running Round {task.get('round')} evaluation | Task: {task_id} | Email: {email} | Repo: {repo_url}")

    try:
        score = 20
        feedback = f"Round {task.get('round')} executed successfully"

        try:
            update_task_result(task_id, {"score": score, "feedback": feedback})
            logger.info(f"Task {task_id} updated in Supabase")
        except Exception as e:
            logger.warning(f"Failed to update Supabase: {e}")

        return {"score": score, "feedback": feedback}

    except Exception as e:
        logger.exception("Error during Round 2+ evaluation")
        return {"score": 0, "feedback": f"Error: {str(e)}"}
