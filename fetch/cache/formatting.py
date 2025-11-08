from datetime import timedelta 

def format_time(time_diff: timedelta) -> str:
  """
  Format a time difference as human-readable string.

  Args:
    time_diff: Time difference to format

  Returns:
    Human-readable time string
  """
  seconds = time_diff.total_seconds()
  if seconds < 60:
    return "just now"
  elif seconds < 3600:
    mins = int(seconds / 60)
    return f"{mins} minute{'s' if mins != 1 else ''} ago"
  else:
    hours = int(seconds / 3600)
    return f"{hours} hour{'s' if hours != 1 else ''} ago"
