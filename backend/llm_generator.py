import requests, time, json, uuid
from config import AIPIPE_TOKEN
from github_utils import (
    create_repo,
    create_commit_and_push,
    enable_github_pages,
    check_file_exists_in_repo
)

def generate_code_and_push(
    brief,
    repo_name=None,
    attachments=None,
    repo_url=None,
    checks: list = None,
    name=None,
    email=None,
    task=None
):
    """
    Generates code via AI Pipe, pushes to GitHub, enforces repo-level checks
    (like MIT LICENSE), enables GitHub Pages, and returns repo + pages URLs.
    """
    url = "https://aipipe.org/openrouter/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {AIPIPE_TOKEN}",
        "Content-Type": "application/json"
    }

    # Prepare AI prompt
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

        start = text.find("{")
        end = text.rfind("}") + 1
        try:
            files = json.loads(text[start:end])
        except json.JSONDecodeError:
            files = {"index.html": f"<html><body><h1>{brief}</h1></body></html>"}
    except Exception:
        files = {"index.html": f"<html><body><h1>{brief}</h1></body></html>"}

    # Step 2: Handle GitHub repo creation or use existing
    is_new_repo = False
    if not repo_url:
        repo_name = repo_name or f"task-{uuid.uuid4().hex[:8]}"
        repo_url = create_repo(repo_name)
        is_new_repo = True

    repo_short_name = repo_name if repo_name else repo_url.split("/")[-1]

    # Step 3: Push all generated files
    commit_sha = None
    for filename, content in files.items():
        commit_sha = create_commit_and_push(repo_short_name, filename, content, f"Add {filename}")

    # Step 4: Enforce repo-level checks
    if checks:
        for check in checks:
            if check.lower() == "mit license":
                license_filename = "LICENSE"
                if not check_file_exists_in_repo(repo_url, license_filename):
                    mit_text = f"""MIT License

Copyright (c) {name} <{email}>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

This repository contains a project generated to fulfill the task: "{task}".
Brief description: "{brief}"

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
                    create_commit_and_push(repo_short_name, license_filename, mit_text, "Add MIT LICENSE")

# After pushing files
    repo_name = repo_url.split("/")[-1] if repo_url else repo_name

    # Always attempt to enable GitHub Pages if not already
    try:
        pages_url = enable_github_pages(repo_name)
    except Exception:
        pages_url = None

    return {
        "files": files,
        "repo_url": repo_url,
        "commit_sha": commit_sha,
        "pages_url": pages_url
    }



def post_with_retry(url, payload, headers=None, max_retries=5):
    """POST to evaluation_url with exponential backoff."""
    headers = headers or {"Content-Type": "application/json"}
    delay = 1
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"✅ Successfully notified evaluation_url on attempt {attempt+1}")
                return True
            else:
                print(f"⚠️ Attempt {attempt+1} failed with {response.status_code}, error msg: {response.text}")
        except Exception as e:
            print(f"❌ Attempt {attempt+1} error: {e}")
        time.sleep(delay)
        delay *= 2  # Exponential backoff
    print("❌ All retry attempts failed.")
    return False