import requests
import json
from datetime import datetime

from .cache_utils import get_cache_path, is_cache_valid, format_time

def _load_from_cache(username:str) -> list[str] | None:
  cache_path = get_cache_path(username)
  if not is_cache_valid(cache_path):
    return None
  try:
    with open(cache_path, 'r') as f:
      data = json.load(f)
      cached_time = datetime.fromisoformat(data['cached_at'])
      time_ago = datetime.now() - cached_time
      print(f"Loaded from cache (Cached {format_time(time_ago)})")
      return data['repos']
  except (json.JSONDecodeError, KeyError) as e:
    print(f"Cache file corrupted, refreshing data ({e})")
    return None


def _save_to_cache(username:str, repos:list):
  cache_path = get_cache_path(username)
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

  print(f"Fetching repos from GitHub API for {username}")
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
