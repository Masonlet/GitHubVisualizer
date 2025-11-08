from datetime import datetime
from pathlib import Path
from config import CACHE_DURATION

"""
Cache validation utilities.

Checks cache file validity based on existence and expiration time.
"""

def is_cache_valid(cache_path: Path) -> bool:
  """
  Check if cache file exists and is not expired.

  Args:
    cache_path: Path to cache file

  Returns:
    True if cache is valid, False otherwise
  """
  if not cache_path.exists():
    return False
  try:
    cache_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
    return datetime.now() - cache_time < CACHE_DURATION
  except (OSError, PermissionError):
    return False