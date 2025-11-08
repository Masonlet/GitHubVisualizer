import requests

"""Centralized error handling for API requests."""

def handle_api_error(error: requests.RequestException, context: str) -> None:
  """
  Centralized error handling for API requests.
  
  Args:
    error: The request exception that occurred
    context: Description of the operation that failed
  """
  if isinstance(error, requests.HTTPError):
      if error.response.status_code == 404:
          print(f"{context}: Not found (404)")
      elif error.response.status_code == 403:
          print(f"{context}: Rate limit exceeded. Try using a token.")
      else:
          print(f"{context}: API error ({error.response.status_code})")
  elif isinstance(error, requests.Timeout):
      print(f"{context}: Request timed out")
  elif isinstance(error, requests.ConnectionError):
      print(f"{context}: Network error")
  else:
      print(f"{context}: Unexpected error - {error}")