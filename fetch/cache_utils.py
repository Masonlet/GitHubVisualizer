import json
from datetime import datetime, timedelta
from pathlib import Path
from config import CACHE_DIR, CACHE_DURATION

def get_cache_path(username: str) -> Path:
  CACHE_DIR.mkdir(exist_ok=True)
  return CACHE_DIR / f"{username}.json"


def get_commit_cache_path(username: str, repo: str) -> Path:
  user_dir = CACHE_DIR / username
  user_dir.mkdir(exist_ok=True)
  return user_dir / f"{repo}_commits.json"


def is_cache_valid(cache_path: Path) -> bool:
  if not cache_path.exists():
    return False
  try:
    cache_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
    return datetime.now() - cache_time < CACHE_DURATION
  except (OSError, PermissionError):
    return False


def format_time(time_diff: timedelta) -> str:
  seconds = time_diff.total_seconds()
  if seconds < 60:
    return "just now"
  elif seconds < 3600:
    mins = int(seconds / 60)
    return f"{mins} minute{'s' if mins != 1 else ''} ago"
  else:
    hours = int(seconds / 3600)
    return f"{hours} hour{'s' if hours != 1 else ''} ago"
