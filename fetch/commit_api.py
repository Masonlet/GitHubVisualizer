import json
import requests
from datetime import datetime

from .cache_utils import get_commit_cache_path, is_cache_valid

def get_repo_commits(username:str, repo:str, refresh:bool=False, per_page:int=100, token:str | None=None) -> list[dict]:
  cache_path = get_commit_cache_path(username, repo)

  if not refresh and is_cache_valid(cache_path):
    try:
      with open(cache_path, 'r') as f:
        return json.load(f)
    except OSError as e:
      print(f"Could not read from cache: {e}")

  print(f"Fetching commits from GitHub API for {repo}")
  all_commits = []
  page = 1

  headers = {}
  if token:
    headers['Authorization'] = f'token {token}'

  while True:
    url = f"https://api.github.com/repos/{username}/{repo}/commits"
    params = {"per_page": per_page, "page":page}
    try:
      response = requests.get(url, params=params, headers=headers, timeout=10)
      response.raise_for_status()
      commits = response.json()
      if not commits:
        break
      for commit in commits:
        all_commits.append({
          "repo":repo,
          "message":commit["commit"]["message"],
          "timestamp":commit["commit"]["author"]["date"],
        })
      page += 1
    except requests.RequestException as e:
      print(f"Error fetching commits for {repo}: {e}")
      return []

  try:
    with open(cache_path, 'w') as f:
      json.dump(all_commits, f, indent=2)
  except OSError as e:
    print(f"Could not cache commits for {repo}: ({e})")

  return all_commits
