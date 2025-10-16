# backend/llm_generator.py
import requests
import json
import uuid
from config import AIPIPE_TOKEN
from github_utils import create_repo, create_commit_and_push, enable_github_pages

def generate_code_and_push(brief, repo_name=None, attachments=None):
    """
    Generates files via AI Pipe, pushes them to GitHub,
    enables GitHub Pages, and returns repo + pages URLs.
    """
    url = "https://aipipe.org/openrouter/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {AIPIPE_TOKEN}",
        "Content-Type": "application/json"
    }

    prompt = (
        f"You are a professional web developer. Task: {brief}\n"
        "Generate a minimal, working static website (or minimal app) that satisfies the brief.\n"
        "Return all files in a single JSON object mapping filenames to file contents, for example:\n"
        '{"index.html":"<html>...</html>", "style.css":"..."}\n'
        "Do NOT include extra commentary outside the JSON."
    )

    if attachments:
        prompt += f"\nAttachments info: {attachments}"

    payload = {
        "model": "openai/gpt-4.1-nano",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }

    # Step 1: Generate code
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        text = data["choices"][0]["message"]["content"]

        # Attempt to parse JSON
        start = text.find("{")
        end = text.rfind("}") + 1
        try:
            files = json.loads(text[start:end])
        except json.JSONDecodeError:
            print("Warning: AI Pipe returned invalid JSON. Falling back to basic HTML.")
            files = {"index.html": f"<html><body><h1>{brief}</h1></body></html>"}
    except Exception as e:
        print("Error generating code from AI Pipe:", e)
        files = {"index.html": f"<html><body><h1>{brief}</h1></body></html>"}

    # Step 2: Push to GitHub
    repo_url = None
    pages_url = None
    if not repo_name:
        repo_name = f"task-{uuid.uuid4().hex[:8]}"

    try:
        repo_url = create_repo(repo_name)
        for filename, content in files.items():
            create_commit_and_push(repo_name, filename, content, f"Add {filename}")
        pages_url = enable_github_pages(repo_name)
    except Exception as e:
        print("GitHub push failed:", e)

    # Step 3: Return everything
    return {
        "files": files,
        "repo_url": repo_url,
        "pages_url": pages_url
    }
