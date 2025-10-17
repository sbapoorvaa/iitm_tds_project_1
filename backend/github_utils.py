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
        # Initial license is optional; we'll enforce MIT in LLM generator
    }
    try:
        r = requests.post(url, json=data, headers=headers)
        r.raise_for_status()
        return r.json()["html_url"]
    except requests.HTTPError as e:
        print(f"Error creating repo {repo_name}: {e.response.text}")
        raise

def create_commit_and_push(repo_name, file_path, content, commit_msg):
    """Commits a file to the given GitHub repo."""
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/contents/{file_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    encoded_content = base64.b64encode(content.encode()).decode()
    data = {"message": commit_msg, "content": encoded_content}
    try:
        r = requests.put(url, json=data, headers=headers)
        r.raise_for_status()
        return r.json()["commit"]["sha"]
    except requests.HTTPError as e:
        print(f"Error committing {file_path} to {repo_name}: {e.response.text}")
        raise

def enable_github_pages(repo_name):
    """Enables GitHub Pages for the repo."""
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/pages"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"source": {"branch": "main", "path": "/"}}
    try:
        r = requests.post(url, json=data, headers=headers)
        if r.status_code not in [201, 204]:
            print(f"Warning: GitHub Pages may not be enabled yet (status {r.status_code})")
        return f"https://{GITHUB_USERNAME}.github.io/{repo_name}/"
    except requests.HTTPError as e:
        print(f"Error enabling GitHub Pages for {repo_name}: {e.response.text}")
        raise

def check_file_exists_in_repo(repo_url, file_path):
    """Checks if a file exists in the given GitHub repo."""
    repo_name = repo_url.rstrip("/").split("/")[-1]
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/contents/{file_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    return r.status_code == 200
