"""Tests for commit API module."""

import json
import requests
import pytest
from unittest.mock import patch, Mock
from github_visualizer.fetch.commit_api import get_repo_commits, get_commit_cache_path

def make_fake_commit(message: str, date: str):
  return {
    "commit": {
      "message": message,
      "author": {"date": date}
    }
  }

class TestGetRepoCommits:
  def test_returns_cached_data_when_valid(self, tmp_path):
    username = "user"
    repo = "repo"
    cache_path = tmp_path / f"{repo}_commits.json"
    cached_data = [{"repo": repo, "message": "cached commit", "timestamp": "2025-01-01T12:00:00Z"}]
    cache_path.write_text(json.dumps(cached_data))

    with patch("github_visualizer.fetch.commit_api.get_commit_cache_path", return_value=cache_path), \
         patch("github_visualizer.fetch.commit_api.is_cache_valid", return_value=True):
      commits = get_repo_commits(username, repo)
        
    assert commits == cached_data

  def test_fetches_from_api_when_cache_invalid(self, tmp_path):
    username = "user"
    repo = "repo"
    fake_api_response = [make_fake_commit("new commit", "2025-11-15T12:00:00Z")]

    cache_path = tmp_path / f"{repo}_commits.json"

    with patch("github_visualizer.fetch.commit_api.get_commit_cache_path", return_value=cache_path), \
         patch("github_visualizer.fetch.commit_api.is_cache_valid", return_value=False), \
         patch("github_visualizer.fetch.commit_api.requests.get") as mock_get:
      mock_get.side_effect = [
        Mock(json=Mock(return_value=fake_api_response), raise_for_status=Mock()),
        Mock(json=Mock(return_value=[]), raise_for_status=Mock())
      ]
       
      commits = get_repo_commits(username, repo)

    assert commits[0]["message"] == "new commit"
    cached_text = cache_path.read_text()
    assert "new commit" in cached_text
  
  def test_handles_pagination(self, tmp_path):
      username = "user"
      repo = "repo"
      page1 = [make_fake_commit("commit1", "2025-11-15T12:00:00Z")]
      page2 = [make_fake_commit("commit2", "2025-11-15T13:00:00Z")]

      cache_path = tmp_path / f"{repo}_commits.json"

      with patch("github_visualizer.fetch.commit_api.get_commit_cache_path", return_value=cache_path), \
           patch("github_visualizer.fetch.commit_api.is_cache_valid", return_value=False), \
           patch("github_visualizer.fetch.commit_api.requests.get") as mock_get:
        mock_get.side_effect = [
            Mock(json=Mock(return_value=page1), raise_for_status=Mock()),
            Mock(json=Mock(return_value=page2), raise_for_status=Mock()),
            Mock(json=Mock(return_value=[]), raise_for_status=Mock())
        ]

        commits = get_repo_commits(username, repo)
        
      assert len(commits) == 2
      assert commits[0]["message"] == "commit1"
      assert commits[1]["message"] == "commit2"
  
  def test_preserves_partial_data_on_error(self, tmp_path): 
    username = "user"
    repo = "repo"
    page1 = [make_fake_commit("commit1", "2025-11-15T12:00:00Z")]

    cache_path = tmp_path / f"{repo}_commits.json"

    with patch("github_visualizer.fetch.commit_api.get_commit_cache_path", return_value=cache_path), \
         patch("github_visualizer.fetch.commit_api.is_cache_valid", return_value=False), \
         patch("github_visualizer.fetch.commit_api.requests.get") as mock_get, \
         patch("github_visualizer.fetch.commit_api.handle_api_error") as mock_error:
      mock_get.side_effect = [
          Mock(json=Mock(return_value=page1), raise_for_status=Mock()),
          requests.RequestException("Network error")
      ]

      commits = get_repo_commits(username, repo)
      
    assert len(commits) == 1
    assert commits[0]["message"] == "commit1"
  
  def test_transforms_commit_format_correctly(self, tmp_path):
    username = "user"
    repo = "repo"
    api_response = [
      make_fake_commit("my message", "2025-11-15T12:34:56Z")
    ]

    cache_path = tmp_path / f"{repo}_commits.json"

    with patch("github_visualizer.fetch.commit_api.get_commit_cache_path", return_value=cache_path), \
         patch("github_visualizer.fetch.commit_api.is_cache_valid", return_value=False), \
         patch("github_visualizer.fetch.commit_api.requests.get") as mock_get:
      mock_get.side_effect = [
        Mock(json=Mock(return_value=api_response), raise_for_status=Mock()),
        Mock(json=Mock(return_value=[]), raise_for_status=Mock())
      ]

      commits = get_repo_commits(username, repo)
    
    c = commits[0]
    assert c["repo"] == repo
    assert c["message"] == "my message"
    assert c["timestamp"] == "2025-11-15T12:34:56Z"