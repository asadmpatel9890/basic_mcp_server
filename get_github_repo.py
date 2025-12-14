import requests

def get_public_repos(username):
    """
    Fetch public repositories of a GitHub user (no auth required)
    Returns output as a string
    """
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.status_code}")

    repos = response.json()

    output_lines = []
    for repo in repos:
        line = f"Repo: {repo['name']} | ⭐ Stars: {repo['stargazers_count']}"
        output_lines.append(line)

    return "\n".join(output_lines)


# # Example usage
# if __name__ == "__main__":
#     print(get_public_repos("octocat"))
