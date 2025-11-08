from fetch.commit_api import get_repo_commits
from config import COMMIT_PREVIEW_COUNT
from models import Commit
from visualizer.message_formatter import format_commit_message

"""
Console display for repository information.

Formats and displays repository lists with commit previews.
"""

def _display_repo_commits(repo: str, commits: list[Commit]) -> None:
  """
  Display commit information for a single repository.

  Args:
    repo: Repository name
    commits: List of commits for the repository
  """
  print(f" - {repo}: {len(commits)} commits")

  for commit in commits[:COMMIT_PREVIEW_COUNT]:
    print(f"  - {format_commit_message(commit["message"])}")

  remaining = len(commits) - COMMIT_PREVIEW_COUNT
  if remaining > 0: 
    print(f"  - {remaining} more commits\n")
  else: 
    print()

def display_all_repos(
  username: str, 
  repos: list[str], 
  refresh: bool, 
  token: str | None = None
) -> None:
  """
  Display all repositories with commit previews.

  Args:
    username: GitHub username
    repos: List of repository names
    refresh: Whether to refresh cached commit data
    token: Optional GitHub personal access token
  """
  print(f"Public repositories for {username}:")
  for repo in repos:
    commits = get_repo_commits(username, repo, refresh, token=token)
    _display_repo_commits(repo, commits)