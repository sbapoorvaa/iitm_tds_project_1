import os

from dotenv import load_dotenv

load_dotenv() 


# AI Pipe
AIPIPE_TOKEN = os.environ.get("AIPIPE_TOKEN")  # Your AI Pipe API key

# GitHub
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")

# Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Student secret for your tasks
STUDENT_SECRET = os.environ.get("STUDENT_SECRET")

# Sanity check
for var_name in ["AIPIPE_TOKEN", "GITHUB_TOKEN", "GITHUB_USERNAME", "SUPABASE_URL", "SUPABASE_KEY", "STUDENT_SECRET"]:
    if not globals()[var_name]:
        raise ValueError(f"Environment variable '{var_name}' is not set!")
