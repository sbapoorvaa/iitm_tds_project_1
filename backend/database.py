from supabase import Client, create_client
from config import SUPABASE_URL, SUPABASE_KEY

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_task(email, task, round_no, brief):
    data = {
        "email": email,
        "task": task,
        "round": round_no,
        "brief": brief,
        "status": "pending"
    }
    response = supabase.table("tasks").insert(data).execute()
    # supabase-py returns response.data as a list of inserted rows
    if response.data and len(response.data) > 0:
        return response.data[0]["id"]
    return None

def update_task_result(task_id, result):
    try:
        response = supabase.table("tasks").update(
            {"result": result, "status": "completed"}
        ).eq("id", task_id).execute()
    except Exception as e:
        # Network or client-level error
        raise Exception(f"Failed to update task {task_id}: {e}")

    # supabase-py returns a response with .data and possibly .error
    # If there's an error object or no rows were updated, surface it.
    error = getattr(response, "error", None)
    data = getattr(response, "data", None)

    if error:
        raise Exception(f"Supabase error updating task {task_id}: {error}")

    if not data or len(data) == 0:
        raise Exception(f"No task updated for id {task_id}. Response: {response}")

    # Return the updated row for convenience
    return data[0]

def get_task(task_id):
    response = supabase.table("tasks").select("*").eq("id", task_id).execute()
    if response.data and len(response.data) > 0:
        return response.data[0]
    return None
