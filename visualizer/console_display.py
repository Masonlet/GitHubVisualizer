from fetch.commit_api import get_repo_commits

COMMIT_PREVIEW_COUNT = 3
MESSAGE_PREVIEW_LENGTH = 70

def _display_repo_commits(repo:str, commits:list[dict]) -> None:
  print(f" - {repo}: {len(commits)} commits")
  for c in commits[:COMMIT_PREVIEW_COUNT]:
    msg = c["message"].split('\n')[0]
    print(f"  - {msg[:MESSAGE_PREVIEW_LENGTH]}")
  if len(commits) > COMMIT_PREVIEW_COUNT:
    print(f"  - {len(commits) - COMMIT_PREVIEW_COUNT} more commits\n")
  else:
    print()

def display_all_repos(username:str, repos:list[str], refresh:bool) -> int:
  print(f"Public repositories for {username}:")
  total_commits = 0
  for repo in repos:
    commits = get_repo_commits(username, repo, refresh)
    _display_repo_commits(repo, commits)
    total_commits += len(commits)
  return total_commits

