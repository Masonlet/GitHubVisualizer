from fetch.commit_api import get_repo_commits


COMMIT_PREVIEW_COUNT = 3
MESSAGE_PREVIEW_LENGTH = 70


def _display_repo_commits(repo: str, commits: list[dict]) -> None:
  print(f" - {repo}: {len(commits)} commits")
  for commit in commits[:COMMIT_PREVIEW_COUNT]:
    message = commit["message"].split('\n')[0]
    if message:
      print(f"  - {message[:MESSAGE_PREVIEW_LENGTH]}")
    else:
      print(f"  - (no commit message)")
  if len(commits) > COMMIT_PREVIEW_COUNT:
    print(f"  - {len(commits) - COMMIT_PREVIEW_COUNT} more commits\n")
  else:
    print()

def display_all_repos(username: str, repos: list[str], refresh: bool, token: str | None = None) -> None:
  print(f"Public repositories for {username}:")
  for repo in repos:
    commits = get_repo_commits(username, repo, refresh, token=token)
    _display_repo_commits(repo, commits)

