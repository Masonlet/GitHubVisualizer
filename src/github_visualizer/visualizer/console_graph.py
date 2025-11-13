"""
GitHub-style contribution graph visualization.

Manages the creation and display of a contribution heatmap similar to GitHub's profile page.
"""

from ..fetch.commit_api import get_repo_commits
from .graph_data import (
  get_commit_dates,
  create_week_grid,
  populate_grid
)
from .graph_renderer import (
  print_month_labels,
  print_graph_grid,
  print_legend,
  print_stats
)

def display_contribution_graph(
  username: str, 
  repos: list[str], 
  refresh: bool = False, 
  weeks: int = 52,
  token: str | None = None
) -> None:
  """
  Display GitHub-style contribution graph for user's commits.

  Shows a heatmap of commit activity over the specified time period,
  with intensity levels indicating commit frequency.

  Args:
    username: GitHub username
    repos: List of repository names to visualize
    refresh: Whether to refresh cached commit data
    weeks: Number of weeks to display (default: 52)
    token: Optional GitHub personal access token
  """
  print(f"GitHub Contribution Graph for {username}\n")
  
  all_commits = []
  for repo in repos:
    commits = get_repo_commits(username, repo, refresh, token=token)
    all_commits.extend(commits)
   
  if not all_commits:
    print("No commits found.")
    return
    
  commit_dates = get_commit_dates(all_commits)
  grid = create_week_grid(weeks)
  grid = populate_grid(grid, commit_dates)
    
  print_month_labels(grid)
  print_graph_grid(grid)
  print_legend()
  print_stats(commit_dates, weeks)
  print()