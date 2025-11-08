from datetime import datetime, timedelta
from collections import defaultdict
from models import Commit
from config import INTENSITY_CHARS, INTENSITY_LEVELS

"""
Data processing for contribution graphs.

Handles commit date counting, grid creation, and intensity level calculations.
"""

def get_commit_dates(commits: list[Commit]) -> dict[str, int]:
  """
  Count commits by date.

  Args:
    commits: List of commit dictionaries

  Returns:
    Dictionary mapping date strings to commit counts
  """
  date_counts = defaultdict(int)
  for commit in commits:
    try:
      date = datetime.fromisoformat(commit['timestamp'].replace('Z', '+00:00'))
      date_key = date.date().isoformat()
      date_counts[date_key] += 1
    except (ValueError, KeyError):
      continue
  return date_counts

def get_intensity_char(commit_count: int) -> str:
  """
  Map commit count to intensity character.

  Args:
    commit_count: Number of commits

  Returns:
    Character representing intensity level
  """
  for i in range(len(INTENSITY_LEVELS) - 1, -1, -1):
    if commit_count >= INTENSITY_LEVELS[i]:
      return INTENSITY_CHARS[i]
  return INTENSITY_CHARS[0]

def create_week_grid(weeks: int = 52) -> list[list[tuple[str, int]]]:
  """
  Create empty week grid for the specified number of weeks.

  Args:
    weeks: Number of weeks to include in grid

  Returns:
    7x(weeks*7) grid where each cell is (date_string, commit_count)
  """
  today = datetime.now().date()
  days_since_sunday = (today.weekday() + 1) % 7
  end_date = today - timedelta(days=days_since_sunday)
  start_date = end_date - timedelta(weeks=weeks - 1)

  grid = [[] for _ in range(7)]
  current_date = start_date

  while current_date <= end_date:
    day_of_week = (current_date.weekday() + 1) % 7
    grid[day_of_week].append((current_date.isoformat(), 0))
    current_date += timedelta(days=1)

  return grid

def populate_grid(
  grid: list[list[tuple[str, int]]], 
  commit_dates: dict[str, int]
) -> list[list[tuple[str, int]]]:
  """
  Fill grid with commit counts.

  Args:
    grid: Empty week grid
    commit_dates: Dictionary of dates to commit counts

  Returns:
    Grid with commit counts populated
  """
  for row_i, row in enumerate(grid):
    grid[row_i] = [(date, commit_dates.get(date, 0)) for date, _ in row]
  return grid