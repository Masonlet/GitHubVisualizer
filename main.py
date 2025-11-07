from utils.user_input import get_user_input
from fetch.repo_api import get_user_repos
from visualizer.console_display import display_all_repos
from visualizer.console_graph import display_contribution_graph

def main() -> None:
  """
  Entry point for GitHub repository visualizer.

  Prompts for username and configuration, 
  then displays repository information and contribution graph.
  """
  try: 
    username, refresh, token = get_user_input()
  except ValueError as e:
    print(e)
    return

  repos = get_user_repos(username, refresh, token)
  if not repos:
    print(f"No public repositories found for {username}.")
    return

  display_all_repos(username, repos, refresh, token=token)
  display_contribution_graph(username, repos, refresh, weeks=52, token=token)

if __name__ == "__main__":
  main()
