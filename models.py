from typing import TypedDict

"""Type definitions for GitHub visualizer."""

class Commit(TypedDict):
  repo: str
  message: str
  timestamp: str