"""Tests for commit API module."""

import pytest
from datetime import datetime, timedelta
from github_visualizer.visualizer.graph_data import (
  get_commit_dates,
  get_intensity_char,
  create_week_grid,
  populate_grid
)


def make_commit(timestamp: str):
  return {"repo": "repo", "message": "msg", "timestamp": timestamp}


class TestGetCommitDates:
  def test_counts_commits_by_date(self):
    commits = [
      make_commit("2025-11-01T12:00:00Z"),
      make_commit("2025-11-01T13:00:00Z"),
      make_commit("2025-11-02T09:00:00Z"),
    ]
    date_counts = get_commit_dates(commits)
    assert date_counts["2025-11-01"] == 2
    assert date_counts["2025-11-02"] == 1


  def test_handles_invalid_timestamps(self):
    commits = [
      make_commit("invalid"),
      make_commit("2025-11-01T12:00:00Z")
    ]
    date_counts = get_commit_dates(commits)
    assert "2025-11-01" in date_counts
    assert len(date_counts) == 1


  def test_ignores_missing_keys(self):
    commits = [{"repo": "repo"}] 
    date_counts = get_commit_dates(commits)
    assert date_counts == {}


  def test_groups_same_day_commits(self):
    commits = [
      make_commit("2025-11-01T01:00:00Z"),
      make_commit("2025-11-01T23:59:59Z")
    ]
    date_counts = get_commit_dates(commits)
    assert date_counts["2025-11-01"] == 2


class TestGetIntensityChar:
  def test_maps_counts_to_intensity_levels(self):
    from github_visualizer.config import INTENSITY_CHARS, INTENSITY_LEVELS
    for i, level in enumerate(INTENSITY_LEVELS):
      if i > 0:
        assert get_intensity_char(level - 1) == INTENSITY_CHARS[i - 1]
      assert get_intensity_char(level) == INTENSITY_CHARS[i]


class TestCreateWeekGrid:
  def test_creates_correct_grid_structure(self):
    grid = create_week_grid(weeks=2)
    assert len(grid) == 7
    for row in grid:
      assert len(row) >= 2
      for date, count in row:
        assert isinstance(date, str)
        assert count == 0


  def test_aligns_to_sunday(self):
    grid = create_week_grid(weeks=1)
    first_day_of_first_row = grid[0][0][0]
    weekday = datetime.fromisoformat(first_day_of_first_row).weekday()
    assert (weekday + 1) % 7 == 0

class TestPopulateGrid:
  def test_fills_grid_with_commit_counts(self):
    grid = create_week_grid(weeks=1)
    dates = [row[0][0] for row in grid[:2]]
    commit_counts = {dates[0]: 3, dates[1]: 1}
    populated = populate_grid(grid, commit_counts)
    assert populated[0][0][1] == 3
    assert populated[1][0][1] == 1
    for row in populated[2:]:
      assert row[0][1] == 0