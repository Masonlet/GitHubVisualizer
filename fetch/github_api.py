import json
from datetime import datetime, timedelta
from pathlib import Path

import requests

CACHE_DIR = Path(".github_cache")
CACHE_DURATION = timedelta(hours=2)


def _get_cache_path(username:str) -> Path:
  CACHE_DIR.mkdir(exist_ok=True)
  return CACHE_DIR / f"{username}.json"


def _is_cache_valid(cache_path:Path) -> bool:
  if not cache_path.exists():
    return False
  cache_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
  return datetime.now() - cache_time < CACHE_DURATION


def _format_time(time_diff:timedelta) -> str:
  seconds = time_diff.total_seconds()
  if seconds < 60:
    return "just now"
  elif seconds < 3600:
    mins = int(seconds / 60)
    return f"{mins} minute{'s' if mins != 1 else ''} ago"
  else:
    hours = int(seconds / 3600)
    return f"{hours} hour{'s' if hours != 1 else ''} ago"


def _load_from_cache(username:str) -> list[str] | None:
  cache_path = _get_cache_path(username)
  if not _is_cache_valid(cache_path):
    return None
  try:
    with open(cache_path, 'r') as f:
      data = json.load(f)
      cached_time = datetime.fromisoformat(data['cached_at'])
      time_ago = datetime.now() - cached_time
      print(f"Loaded from cache (Cached {_format_time(time_ago)})")
      return data['repos']
  except (json.JSONDecodeError, KeyError):
    return None


def _save_to_cache(username:str, repos:list):
  cache_path = _get_cache_path(username)
  data = {
    'username': username,
    'repos': repos,
    'cached_at': datetime.now().isoformat()
  }
  try:
    with open(cache_path, 'w') as f:
      json.dump(data, f, indent=2)
  except OSError as e:
    print(f"Could not save to cache: {e}")


def get_user_repos(username:str, refresh:bool=False) -> list[str]:
  if not refresh:
    cached_repos = _load_from_cache(username)
    if cached_repos is not None:
      return cached_repos

  print(f"Fetching from GitHub API")
  url = f"https://api.github.com/users/{username}/repos"

  try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    repos = response.json()
    repo_names = [repo["name"] for repo in repos]

    _save_to_cache(username, repo_names)
    return repo_names

  except requests.RequestException as e:
    print(f"Error fetching from GitHub: {e}")
    return []
