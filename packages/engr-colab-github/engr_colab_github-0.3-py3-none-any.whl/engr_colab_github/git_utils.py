from github import Github
import subprocess
from pathlib import Path
import shutil
import webbrowser
from datetime import datetime

# Global variables
token = ""
user_name = ""
user_email = ""
repo_name = ""
g = None


def author():
    linkedin_url = "https://www.linkedin.com/in/engrshishir/"
    webbrowser.open_new_tab(linkedin_url)


def setup():
    """
    Set up the GitHub configuration, including authentication token, username, and email.
    """
    global token, user_name, user_email, g

    token = input("Please enter your GitHub personal access token: ").strip()
    g = Github(token)

    try:
        user_name = input("Enter your GitHub username: ").strip()
        user_email = input("Enter your GitHub email: ").strip()

        # Set global git configuration
        subprocess.run(["git", "config", "--global", "user.name", user_name])
        subprocess.run(["git", "config", "--global", "user.email", user_email])
        print(f"Git configured with username: {user_name}, email: {user_email}")
    except subprocess.CalledProcessError as e:
        print(f"Error while setting Git configuration: {e}")


def create_repo():
    """
    Creates a new GitHub repository using the provided credentials and inputs.
    """
    global repo_name

    repo_name = input("Enter your repository name: ").strip()
    description = input("Enter repo description (optional): ").strip()
    user = g.get_user()
    repo = user.create_repo(
        name=repo_name,
        description=description,
        private=False,
        auto_init=True,
        gitignore_template="Python",  # Adjust as needed
    )
    print(f"Repository '{repo_name}' created successfully!")
    return repo


def clone_repo():
    """
    Clone the specified GitHub repository to the local machine.
    """
    global repo_name

    repo_name = input("Enter your repository name to clone: ").strip()
    clone_url = f"https://{token}@github.com/{user_name}/{repo_name}.git"

    try:
        subprocess.run(["git", "clone", clone_url], check=True)
        print(f"Repository '{repo_name}' cloned successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while cloning the repository: {e}")


def upload_file_to_repo():
    """
    Stages a file for commit and prompts the user to push it manually to the repository.
    """
    current_file_path = input("Please enter the current file path: ").strip()

    try:
        # Stage the file change using git add
        subprocess.run(["git", "add", current_file_path], check=True)
        print(f"File '{current_file_path}' staged for commit.")
        print(
            f"File is staged locally. Please commit and push the changes manually to the repository '{repo_name}'."
        )
    except subprocess.CalledProcessError as e:
        print(f"Error during staging: {e}")


def delete_path():
    """
    Deletes a specified file or folder and all its contents.
    """
    current_file_path = input("Please enter the path that you want to delete: ").strip()
    path = Path(current_file_path)

    if path.is_dir():
        shutil.rmtree(path)
        print(f"Folder '{path}' and its contents have been deleted.")

    elif path.is_file():
        path.unlink()
        print(f"File '{path}' has been deleted.")

    else:
        print(f"Path '{path}' does not exist.")


def git_add():
    """
    Adds a file or folder to the staging area for commit.
    """
    current_file_path = input("Please enter the path to add: ").strip()
    path = Path(current_file_path)

    if path.exists():
        subprocess.run(["git", "add", str(path)], check=True)
        print(f"'{path}' has been added to the staging area.")
    else:
        print(f"The path '{path}' does not exist.")


def git_commit():
    """
    Commits staged changes with a user-provided commit message and an optional description.
    """
    message = input("Please enter commit message: ").strip()
    description = input("Please enter commit description (optional): ").strip()

    # Combine message and description if provided
    commit_message = message
    if description:
        commit_message = f"{message}\n\n{description}"

    try:
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print(f"Changes have been committed with message: '{message}'")
    except subprocess.CalledProcessError as e:
        print(f"Error during commit: {e}")


def git_push():
    try:
        version = input("Please enter version (e.g: v1): ").strip()
        commit_message = "Pushed to remote successfully on"
        current_date = datetime.now().strftime("%d %b, %Y")
        full_commit_message = f"Version {version}: {commit_message} ({current_date})"
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", full_commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        print(f"Version {version} pushed to remote successfully on {current_date}!")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        


def git_Pull():
    try:
        subprocess.run(["git", "pull"], check=True)
        print("Colab folder updated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while pulling updates: {e}")



def git_status():
    try:
        subprocess.run(["git", "status"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

def git_log():
    try:
        subprocess.run(["git", "log"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

def merge_branch():
    branch_name = input("Enter the branch name to merge: ").strip()
    try:
        subprocess.run(["git", "merge", branch_name], check=True)
        print(f"Branch '{branch_name}' merged successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

def git_reset():
    try:
        subprocess.run(["git", "reset", "--hard"], check=True)
        print("Working directory reset to the latest commit.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
