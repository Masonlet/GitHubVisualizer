from typing import TypedDict

class Commit(TypedDict):
  repo: str
  message: str
  timestamp: str