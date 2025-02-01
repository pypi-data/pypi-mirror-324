# code_utils/git_utils.py
import subprocess
from github import Github

def setup():
    token = input("Please enter your GitHub personal access token: ").strip()
    g = Github(token)

    try:
        user_name = input("Enter your GitHub username: ").strip()
        user_email = input("Enter your GitHub email: ").strip()

        subprocess.run(["git", "config", "--global", "user.name", user_name])
        subprocess.run(["git", "config", "--global", "user.email", user_email])
        print(f"Git configured with username: {user_name}, email: {user_email}")
    except subprocess.CalledProcessError as e:
        print(f"Error while cloning the repository: {e}")

def clone_repo(user_name, repo_name, token):
    """
    Clones the specified GitHub repository.
    Args:
    user_name (str): GitHub username.
    repo_name (str): The name of the GitHub repository to clone.
    token (str): GitHub personal access token for authentication.
    """
    # Construct the clone URL with the provided token
    clone_url = f"https://{token}@github.com/{user_name}/{repo_name}.git"
    
    try:
        subprocess.run(["git", "clone", clone_url], check=True)
        print(f"Repository '{repo_name}' cloned successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while cloning the repository: {e}")
