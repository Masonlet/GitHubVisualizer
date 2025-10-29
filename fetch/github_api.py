import requests

def get_user_repos(username: str):
  url = f"https://api.github.com/users/{username}/repos"
  response = requests.get(url)

  if response.status_code != 200:
    print(f"Error: {response.status_code} - {response.text}")
    return []

  repos = response.json()
  return [repo["name"] for repo in repos]
