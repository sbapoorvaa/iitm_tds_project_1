import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

# AI Pipe
AIPIPE_TOKEN = os.environ.get("AIPIPE_TOKEN")

# GitHub
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")

# Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Student secret (hashed for storage/verification)
STUDENT_SECRET = os.environ.get("STUDENT_SECRET")

# Supabase tables
PROMPTS_TABLE = "prompts"
RESULTS_TABLE = "results"

# Utility function to hash secrets
def hash_secret(secret: str) -> str:
    return hashlib.sha256(secret.encode()).hexdigest()

# Sanity check
for var_name in ["AIPIPE_TOKEN", "GITHUB_TOKEN", "GITHUB_USERNAME", "SUPABASE_URL", "SUPABASE_KEY", "STUDENT_SECRET"]:
    if not globals()[var_name]:
        raise ValueError(f"Environment variable '{var_name}' is not set!")
