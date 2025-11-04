from datetime import datetime

from fetch.repo_api import get_user_repos
from fetch.commit_api import get_repo_commits

def main() -> None:
  username = input("Enter GitHub username: ").strip()
  if not username:
    print("Username cannot be empty.")
    return

  refresh = input("Refresh cache? (y/n, default: n): ").strip().lower() == 'y'
  repos = get_user_repos(username, refresh)
  if not repos:
    print(f"No public repositories found for {username}.")
    return

  total_commits = 0

  print(f"Public repositories for {username}:")
  for repo in repos:
    commits = get_repo_commits(username, repo, refresh)
    print(f" - {repo}: {len(commits)} commits")
    for c in commits[:3]:
      msg = c["message"].split('\n')[0]
      print(f"  - {msg[:70]}")
    if len(commits) > 3:
      print(f"  - {len(commits) - 3} more commits\n")
    else:
      print()
    total_commits += len(commits)

  print(f"Total commits fetched: {total_commits}")

if __name__ == "__main__":
  main()
