import logging
import time
from round1 import run_round1
from round2 import run_round2

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def evaluate(task):
    """
    Central evaluation function.
    Handles round 1 and any subsequent rounds.
    Returns structured results with logs and execution time.
    """
    task_id = task.get("task")
    round_no = task.get("round")
    email = task.get("email")
    nonce = task.get("nonce")

    logger.info(f"Starting evaluation | Task: {task_id} | Round: {round_no} | Email: {email} | Nonce: {nonce}")

    start_time = time.time()
    result = {"task": task_id, "round": round_no, "status": "pending", "logs": "", "time_taken": 0}

    try:
        if round_no == 1:
            eval_result = run_round1(task)
        else:  # Round 2 and beyond
            eval_result = run_round2(task)

        result.update({"status": "success", "logs": str(eval_result)})
        logger.info(f"Evaluation success | Task: {task_id} | Round: {round_no}")

    except Exception as e:
        logger.exception("Error during evaluation")
        result.update({"status": "failed", "logs": str(e)})

    end_time = time.time()
    result["time_taken"] = round(end_time - start_time, 2)
    logger.info(f"Task evaluation finished | Task: {task_id} | Time: {result['time_taken']}s")

    return result
