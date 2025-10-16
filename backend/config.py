import os
from dotenv import load_dotenv

load_dotenv() 

# AI Pipe
AIPIPE_TOKEN = os.getenv("AIPIPE_TOKEN")  # Your AI Pipe API key
# GitHub
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Student secret for your tasks
STUDENT_SECRET = os.getenv("STUDENT_SECRET")


# sanity check
for var in ["AIPIPE_TOKEN", "GITHUB_TOKEN", "GITHUB_USERNAME", "STUDENT_SECRET"]:
    if not globals()[var]:
        raise ValueError(f"{var} is not set!")