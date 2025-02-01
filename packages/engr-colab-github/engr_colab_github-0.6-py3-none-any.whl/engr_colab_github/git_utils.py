from github import Github
import subprocess
from pathlib import Path
import shutil
import webbrowser
from datetime import datetime
import sys

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
    """Set up the GitHub configuration, including authentication token, username, and email."""
    global token, user_name, user_email, g

    try:
        from github import Github
    except ImportError:
        print("⚠️ PyGithub is not installed. Installing PyGithub...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyGithub"])

    has_token = (
        input("Do you already have a GitHub personal access token? (yes/no): ")
        .strip()
        .lower()
    )

    if has_token == "no":
        print("🔗 Create a GitHub personal access token here:")
        print("➡️ https://github.com/settings/personal-access-tokens")
        print("⚠️ Ensure you enable 'Repository' and 'Account' permissions!")

    token = input("🔑 Enter your GitHub personal access token: ").strip()

    try:
        g = Github(token)
        g.get_user().login  # Validate token
    except Exception:
        print("❌ Invalid GitHub token! Please check and try again.")
        sys.exit(1)

    # Check if Git username and email are already configured
    try:
        user_name = (
            subprocess.check_output(["git", "config", "--global", "user.name"])
            .strip()
            .decode()
        )
        user_email = (
            subprocess.check_output(["git", "config", "--global", "user.email"])
            .strip()
            .decode()
        )
        print(
            f"✅ Git is already configured with username: {user_name}, email: {user_email}"
        )
    except subprocess.CalledProcessError:
        print("⚠️ Git username and email not set. Please enter them below.")
        user_name = input("👤 Enter your GitHub username: ").strip()
        user_email = input("📧 Enter your GitHub email: ").strip()

        # Set global git configuration
        subprocess.run(["git", "config", "--global", "user.name", user_name])
        subprocess.run(["git", "config", "--global", "user.email", user_email])
        print(f"✅ Git configured with username: {user_name}, email: {user_email}")


def create_repo():
    """Creates a new GitHub repository with error handling."""
    global repo_name

    try:
        repo_name = input("📂 Enter repository name: ").strip()
        description = input("📝 Enter repository description (optional): ").strip()

        user = g.get_user()
        repo = user.create_repo(
            name=repo_name,
            description=description,
            private=False,
            auto_init=True,
            gitignore_template="Python",
        )
        print(f"✅ Repository '{repo_name}' created successfully!")
        return repo

    except Exception as e:
        if "Bad credentials" in str(e):
            print("❌ Invalid GitHub token! Please check and try again.")
        elif "Requires authentication" in str(e):
            print("❌ You must authenticate using a Personal Access Token (PAT).")
        elif "403" in str(e):
            print("⚠️ Permission denied! Check token permissions at:")
            print("➡️ https://github.com/settings/tokens")
            print("Enable 'Repository' and 'Account' permissions.")
        else:
            print(f"❌ Error: {e}")


def clone_repo():
    """Clones a GitHub repository with error handling."""
    global repo_name

    repo_name = input("📥 Enter repository name to clone: ").strip()
    clone_url = f"https://{token}@github.com/{user_name}/{repo_name}.git"

    try:
        subprocess.run(["git", "clone", clone_url], check=True)
        print(f"✅ Repository '{repo_name}' cloned successfully.")
    except subprocess.CalledProcessError:
        print("❌ Failed to clone repository! Check repository name or permissions.")


def delete_path():
    """Deletes a specified file or folder."""
    path = Path(input("🗑️ Enter path to delete: ").strip())

    if not path.exists():
        print(f"⚠️ Path '{path}' does not exist.")
        return

    try:
        if path.is_dir():
            shutil.rmtree(path)
            print(f"✅ Folder '{path}' and its contents deleted.")
        else:
            path.unlink()
            print(f"✅ File '{path}' deleted.")
    except Exception as e:
        print(f"❌ Error deleting '{path}': {e}")


def git_add():
    """Adds a file or folder to the staging area."""
    path = Path(input("➕ Enter file/folder to add: ").strip())

    if not path.exists():
        print(f"⚠️ Path '{path}' does not exist.")
        return

    try:
        subprocess.run(["git", "add", str(path)], check=True)
        print(f"✅ '{path}' added to the staging area.")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to add '{path}'.")


def git_commit():
    """Commits staged changes with a message."""
    message = input("📝 Enter commit message: ").strip()
    description = input("📜 Enter commit description (optional): ").strip()
    commit_message = f"{message}\n\n{description}" if description else message

    try:
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print(f"✅ Changes committed: '{message}'")
    except subprocess.CalledProcessError:
        print("❌ Commit failed! Ensure changes are staged.")


def git_push():
    """Pushes committed changes to GitHub."""
    version = input("🚀 Enter version (e.g., v1): ").strip()
    commit_message = (
        f"Version {version}: Pushed on {datetime.now().strftime('%d %b, %Y')}"
    )

    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        print(f"✅ Version {version} pushed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Push failed! Check remote branch and authentication.")


def git_status():
    """Displays Git status."""
    try:
        subprocess.run(["git", "status"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to get Git status!")


def git_log():
    """Displays Git log."""
    try:
        subprocess.run(["git", "log"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to get Git log!")


def merge_branch():
    """Merges a specified Git branch."""
    branch_name = input("🔀 Enter branch to merge: ").strip()

    try:
        subprocess.run(["git", "merge", branch_name], check=True)
        print(f"✅ Branch '{branch_name}' merged successfully.")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to merge branch '{branch_name}'.")
