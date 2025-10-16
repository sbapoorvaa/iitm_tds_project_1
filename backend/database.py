from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_task(email, task, round_no, brief):
    data = {
        "email": email,
        "task": task,
        "round": round_no,
        "brief": brief,
        "status": "pending"
    }
    response = supabase.table("tasks").insert(data).execute()
    return response.data[0]["id"]  # return task_id

def update_task_result(task_id, result):
    supabase.table("tasks").update({"result": result, "status": "completed"}).eq("id", task_id).execute()

def get_task(task_id):
    response = supabase.table("tasks").select("*").eq("id", task_id).execute()
    if response.data:
        return response.data[0]
    return None
