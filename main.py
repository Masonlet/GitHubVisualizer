from fetch.github_api import get_user_repos

def main() -> None:
  username = input("Enter GitHub username: ").strip()
  if not username:
    print("Username cannot be empty.")
    return

  refresh = input("Refresh cache? (y/n, default: n): ").strip().lower() == 'y'
  repos = get_user_repos(username, refresh)

  if not repos:
    print(f"No public repositories found for {username}.")
    return

  print(f"Public repositories for {username}:")
  for repo in repos:
    print(f" - {repo}")

if __name__ == "__main__":
  main()
