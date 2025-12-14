from fastmcp import FastMCP
from get_github_repo import get_public_repos

mcp = FastMCP("git_repo")

@mcp.tool
def get_repo(name: str) -> str:
    return get_public_repos(name)

if __name__ == "__main__":
    mcp.run()

