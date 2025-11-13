"""Type definitions for GitHub visualizer."""

from typing import TypedDict

class Commit(TypedDict):
  repo: str
  message: str
  timestamp: str