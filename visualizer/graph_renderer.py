from datetime import datetime
from config import DAY_LABELS, INTENSITY_CHARS
from visualizer.graph_data import get_intensity_char

"""
Rendering logic for contribution graphs.

Handles all terminal output formatting for the contribution graph visualization.
"""

def print_month_labels(grid: list[list[tuple[str, int]]]) -> None:
  """
  Print month labels above the contribution graph.

  Args:
    grid: Week grid with date and commit count tuples
  """
  if not grid or not grid[0]:
    return

  first_row = grid[0]
  last_month = None
  month_positions = []

  for col_i, (date_str, _) in enumerate(first_row):
    date = datetime.fromisoformat(date_str).date()
    current_month = date.month
    if current_month != last_month:
      month_positions.append((col_i, date.strftime('%b')))
      last_month = current_month

  label_line = [" "] * len(first_row)
  for pos, name in month_positions:
    for i, ch in enumerate(name):
      if pos + i < len(label_line):
        label_line[pos + i] = ch

  print("      " + "".join(label_line))


def print_graph_grid(grid: list[list[tuple[str, int]]]) -> None:
  """
  Print the contribution graph grid.

  Args:
    grid: Week grid with date and commit count tuples
  """
  for day_i, row in enumerate(grid):
    print(f"{DAY_LABELS[day_i]:>5} ", end="")
    for date_str, count in row:
      char = get_intensity_char(count)
      print(char, end="")
    print()


def print_legend() -> None:
  """Print the intensity legend."""
  print("\n  Less ", end="")
  for char in INTENSITY_CHARS:
    print(char + ' ', end="")
  print("More")

  
def print_stats(commit_dates: dict[str, int], weeks: int) -> None:
  """
  Print contribution statistics.

  Args:
    commit_dates: Dictionary of dates to commit counts
    weeks: Number of weeks displayed
  """
  total_commits = sum(commit_dates.values())
  active_days = len([count for count in commit_dates.values() if count > 0])

  print(f"\n  Total commits in last {weeks} weeks: {total_commits}")
  print(f"  Active days: {active_days}")
  if active_days > 0:
    print(f"  Average commits per active day: {total_commits / active_days:.1f}")