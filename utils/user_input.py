def get_user_input() -> tuple[str, bool]:
  username = input("Enter GitHub username: ").strip()
  if not username:
    raise ValueError("Username cannot be empty.")

  refresh = input("Refresh cache? (y/n, default: n): ").strip().lower() == 'y'
  return username, refresh
