"""Tests for cache module."""

from datetime import timedelta, datetime
from pathlib import Path
import pytest
from unittest.mock import patch

from github_visualizer.fetch.cache.formatting import format_time
from github_visualizer.fetch.cache.paths import get_user_cache_path, get_commit_cache_path
from github_visualizer.fetch.cache.validation import is_cache_valid
from github_visualizer.config import CACHE_DIR

class TestFormatTime:
  def test_just_now(self):
    assert format_time(timedelta(seconds=30)) == "just now"


  def test_minutes(self):
    assert format_time(timedelta(minutes=1)) == "1 minute ago"
    assert format_time(timedelta(minutes=5)) == "5 minutes ago"


  def test_hours(self):
    assert format_time(timedelta(hours=1)) == "1 hour ago"
    assert format_time(timedelta(hours=3)) == "3 hours ago"


class TestCachePaths:
  def test_get_user_cache_path_creates_dir(self, tmp_path):
    username = "testuser"
    with patch("github_visualizer.fetch.cache.paths.CACHE_DIR", tmp_path):
      path = get_user_cache_path(username)
      assert path == tmp_path / f"{username}.json"


  def test_get_commit_cache_path_creates_dir(self, tmp_path):
    username = "testuser"
    repo = "testrepo"
    with patch("github_visualizer.fetch.cache.paths.CACHE_DIR", tmp_path):
      path = get_commit_cache_path(username, repo)
      assert path == tmp_path / username / f"{repo}_commits.json"


class TestIsCacheValid:
  def test_returns_false_for_nonexistent_file(self, tmp_path):
    path = tmp_path / "nonexistent.json"
    assert not is_cache_valid(path)


  def test_returns_true_for_valid_cache(self, tmp_path):
    path = tmp_path / "cache.json"
    path.touch()  
    assert is_cache_valid(path)


  def test_returns_false_on_stat_error(self):
    path = Path("dummy.json")
    with patch("github_visualizer.fetch.cache.validation.Path.exists", return_value=True), \
        patch("github_visualizer.fetch.cache.validation.Path.stat", side_effect=OSError):
      assert not is_cache_valid(path)