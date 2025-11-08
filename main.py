import sys
from utils.user_input import get_user_input
from fetch.repo_api import get_user_repos
from visualizer.console_display import display_all_repos
from visualizer.console_graph import display_contribution_graph
from cli import parse_args

def main() -> None:
  """
  Entry point for GitHub repository visualizer.

  Prompts for username and configuration, 
  then displays repository information and contribution graph.
  """
  args = parse_args()

  if args.username is None:
    try: 
      username, refresh, token = get_user_input()
    except ValueError as e:
      print(e)
      return
    weeks = 52
    no_graph = False
    no_list = False
  else:
    username = args.username
    refresh = args.refresh
    token = args.token
    weeks = args.weeks
    no_graph = args.no_graph
    no_list = args.no_list

  repos = get_user_repos(username, refresh, token)
  if not repos:
    print(f"No public repositories found for {username}.")
    return

  if not no_list:
    display_all_repos(username, repos, refresh, token=token)
  if not no_graph:
    display_contribution_graph(username, repos, refresh, weeks=weeks, token=token)

if __name__ == "__main__":
  main()