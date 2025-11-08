from config import MESSAGE_PREVIEW_LENGTH

"""
Commit message formatting utilities.

Formats commit messages for display in terminal output.
"""

def format_commit_message(
  message: str, 
  max_length: int = MESSAGE_PREVIEW_LENGTH
) -> str:
  """
  Format a commit message for display.

  Args:
    message: Full commit message
    max_length: Maximum length to display

  Returns:
    Formatted message
  """
  first_line = message.split('\n')[0]
  if not first_line:
    return "(no commit message)"
  return first_line[:max_length]
