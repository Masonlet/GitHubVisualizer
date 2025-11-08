import json
from datetime import datetime

import requests

from config import DEFAULT_PER_PAGE, API_TIMEOUT
from fetch.cache.paths import get_commit_cache_path
from fetch.cache.validation import is_cache_valid
from fetch.error_handler import handle_api_error
from models import Commit

"""
GitHub commit API operations.

Handles fetching and caching of repository commit history.
"""

def get_repo_commits(
  username: str, 
  repo: str, 
  refresh: bool = False, 
  per_page: int = DEFAULT_PER_PAGE, 
  token: str | None = None
) -> list[Commit]:
  """
  Fetch all commits for a repository.

  Uses cached data if available and not expired (unless refresh=True).
  Preserves partial data if error occurs.

  Args:
    username: GitHub username
    repo: Repository name
    refresh: If True, bypass cache and fetch fresh data
    per_page: Number of commits per API request (max 100)
    token: Optional GitHub personal access token

  Returns:
    List of commit dictionaries containing repo, message, and timestamp
  """
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
    params = {"per_page": per_page, "page": page}
    try:
      response = requests.get(url, params=params, headers=headers, timeout=API_TIMEOUT)
      response.raise_for_status()
      commits = response.json()
      if not commits:
        break
      for commit in commits:
        all_commits.append({
          "repo": repo,
          "message": commit["commit"]["message"],
          "timestamp": commit["commit"]["author"]["date"],
        })
      page += 1
    except requests.RequestException as e:
      handle_api_error(e, f"Fetching commits for {repo} (page {page})")
      if all_commits:
        print(f"Returning {len(all_commits)} commits fetched before error")
      break

  try:
    with open(cache_path, 'w') as f:
      json.dump(all_commits, f, indent=2)
  except OSError as e:
    print(f"Could not cache commits for {repo}: ({e})")

  return all_commits
