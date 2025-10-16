# Central evaluation script (you can call different rounds from here)
from round1 import run_round1
from round2 import run_round2

def evaluate(task):
    if task["round"] == 1:
        return run_round1(task)
    elif task["round"] == 2:
        return run_round2(task)
    else:
        return {"error": "Unknown round"}
