from fetch.github_api import get_user_repos

def main():
  username = "Masonlet"
  repos = get_user_repos(username)

  print(f"Public repositories for {username}:")
  for repo in repos:
    print(f" - {repo}")

if __name__ == "__main__":
  main()
