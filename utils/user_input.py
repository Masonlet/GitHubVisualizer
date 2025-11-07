def get_user_input() -> tuple[str, bool, str | None]:
  """
  Collect user input for GitHub username and configuration.

  Returns:
    tuple: (username, refresh_cache, access_token)

  Raises:
    ValueError: If username is empty
  """
  username = input("Enter GitHub username: ").strip()
  if not username: raise ValueError("Username cannot be empty.")

  refresh = input("Refresh cache? (y/n, default: n): ").strip().lower() == 'y'
  token = input("Enter GitHub personal access token (optional, press Enter to skip): ").strip()
  return username, refresh, token or None
