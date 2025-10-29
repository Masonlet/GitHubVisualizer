from fetch.github_api import get_user_repos

def main():
  username = input("Enter GitHub username: ").strip()
  repos = get_user_repos(username)

  if not repos:
    print(f"No public repositories found for {username}.")
    return

  print(f"Public repositories for {username}:")
  for repo in repos:
    print(f" - {repo}")

if __name__ == "__main__":
  main()
