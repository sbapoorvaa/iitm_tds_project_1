# backend/github_utils.py
import requests
import base64
from config import GITHUB_TOKEN, GITHUB_USERNAME

def create_repo(repo_name):
    """Creates a GitHub repository for the user."""
    url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {
        "name": repo_name,
        "private": False,
        "auto_init": True,
        "license_template": "mit"
    }
    r = requests.post(url, json=data, headers=headers)
    r.raise_for_status()
    return r.json()["html_url"]

def create_commit_and_push(repo_name, file_path, content, commit_msg):
    """Commits a file to the given GitHub repo."""
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/contents/{file_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    encoded_content = base64.b64encode(content.encode()).decode()
    data = {"message": commit_msg, "content": encoded_content}
    r = requests.put(url, json=data, headers=headers)
    r.raise_for_status()
    return r.json()["commit"]["sha"]

def enable_github_pages(repo_name):
    """Enables GitHub Pages for the repo."""
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/pages"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"source": {"branch": "main", "path": "/"}}
    r = requests.post(url, json=data, headers=headers)
    # GitHub might return 201 Created or 204 No Content
    if r.status_code not in [201, 204]:
        print("Warning: GitHub Pages may not be enabled yet")
    return f"https://{GITHUB_USERNAME}.github.io/{repo_name}/"
