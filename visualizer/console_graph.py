from datetime import datetime, timedelta
from collections import defaultdict
from fetch.commit_api import get_repo_commits

INTENSITY_CHARS = [' ', '░', '▒', '▓', '█']
INTENSITY_LEVELS = [0, 1, 3, 6, 10]
DAY_LABELS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']


def _get_intensity_char(commit_count:int) -> str:
  for i in range(len(INTENSITY_LEVELS) - 1, -1, -1):
    if commit_count >= INTENSITY_LEVELS[i]:
      return INTENSITY_CHARS[i]
  return INTENSITY_CHARS[0]


def _get_commit_dates(commits:list[dict]) -> dict[str, int]:
  date_counts = defaultdict(int)
  for commit in commits:
    try:
      dt = datetime.fromisoformat(commit['timestamp'].replace('Z', '+00:00'))
      date_key = dt.date().isoformat()
      date_counts[date_key] += 1
    except (ValueError, KeyError):
      continue
  return date_counts


def _get_week_grid(weeks:int=52) -> list[list[tuple[str, int]]]:
  today = datetime.now().date()
  days_since_sunday = (today.weekday() + 1) % 7
  end_date = today - timedelta(days = days_since_sunday)
  start_date = end_date - timedelta(weeks = weeks - 1)

  grid = [[] for _ in range(7)]
  current_date = start_date

  while current_date <= end_date:
    day_of_week = (current_date.weekday() + 1) % 7
    grid[day_of_week].append((current_date.isoformat(), 0))
    current_date += timedelta(days=1)

  return grid


def _populate_grid(
  grid:list[list[tuple[str, int]]], 
  commit_dates:dict[str, int]
) -> list[list[tuple[str, int]]]:
  for row_idx, row in enumerate(grid):
    grid[row_idx] = [(date, commit_dates.get(date, 0)) for date, _ in row]
  return grid


def _print_month_labels(grid:list[list[tuple[str, int]]]) -> None:
  if not grid or not grid[0]:
    return

  first_row = grid[0]
  last_month = None
  month_positions = []

  for col_idx, (date_str, _) in enumerate(first_row):
    date = datetime.fromisoformat(date_str).date()
    current_month = date.month
    if current_month != last_month:
      month_positions.append((col_idx, date.strftime('%b')))
      last_month = current_month

  label_line = [" "] * len(first_row)
  for pos, name in month_positions:
    for i, ch in enumerate(name):
      if pos + i < len(label_line):
        label_line[pos + i] = ch

  print("      " + "".join(label_line))


def _print_graph(grid:list[list[tuple[str, int]]]) -> None:
  _print_month_labels(grid)

  for day_idx, row in enumerate(grid):
    print(f"{DAY_LABELS[day_idx]:>5} ", end="")
    for date_str, count in row:
      char = _get_intensity_char(count)
      print(char, end="")
    print()


def _print_legend() -> None:
  print("\n  Less ", end="")
  for char in INTENSITY_CHARS:
    print(char + ' ', end="")
  print("More")


def _print_stats(commit_dates:dict[str, int], weeks:int) -> None:
  total_commits = sum(commit_dates.values())
  active_days = len([c for c in commit_dates.values() if c > 0])

  print(f"\n  Total commits in last {weeks} weeks: {total_commits}")
  print(f"  Active days: {active_days}")
  if active_days > 0:
    print(f"  Average commits per active day: {total_commits / active_days:.1f}")


def display_contribution_graph(
  username:str, 
  repos:list[str], 
  refresh:bool=False, 
  weeks:int=52,
  token:str | None=None
) -> None:
  print(f"GitHub Contribution Graph for {username}\n")
    
  all_commits = []
  for repo in repos:
    commits = get_repo_commits(username, repo, refresh, token=token)
    all_commits.extend(commits)
   
  if not all_commits:
    print("No commits found.")
    return
    
  commit_dates = _get_commit_dates(all_commits)
  grid = _get_week_grid(weeks)
  grid = _populate_grid(grid, commit_dates)
    
  _print_graph(grid)
  _print_legend()
  _print_stats(commit_dates, weeks)
  print()
