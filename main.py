from datetime import datetime

from fetch.repo_api import get_user_repos
from visualizer.console_display import display_all_repos
from utils.user_input import get_user_input

def main() -> None:
  try:
    username, refresh = get_user_input()
  except ValueError as e:
    print(e)
    return

  repos = get_user_repos(username, refresh)
  if not repos:
    print(f"No public repositories found for {username}.")
    return

  total_commits = display_all_repos(username, repos, refresh)
  print(f"Total commits fetched: {total_commits}")

if __name__ == "__main__":
  main()
