from pathlib import Path
from config import CACHE_DIR

"""
Cache file path management.

Provides functions for generating and managing 
cache file paths for users and repositories.
"""

def get_user_cache_path(username: str) -> Path:
  """
  Get cache file path for user repositories.

  Args:
    username: GitHub username

  Returns:
    Path to user's repository cache file
  """
  CACHE_DIR.mkdir(exist_ok=True)
  return CACHE_DIR / f"{username}.json"


def get_commit_cache_path(
  username: str, 
  repo: str
) -> Path:
  """
  Get cache file path for repository commits.

  Args:
    username: GitHub username
    repo: Repository name

  Returns:
    Path to repository's commit cache file
  """
  user_dir = CACHE_DIR / username
  user_dir.mkdir(exist_ok=True)
  return user_dir / f"{repo}_commits.json"
