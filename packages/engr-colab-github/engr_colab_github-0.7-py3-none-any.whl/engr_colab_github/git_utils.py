import os
from github import Github
import subprocess
from pathlib import Path
import shutil
import webbrowser
from datetime import datetime
import sys
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the variables from the environment
token = os.getenv("GITHUB_TOKEN")
user_name = os.getenv("GITHUB_USER_NAME")
user_email = os.getenv("GITHUB_EMAIL")
active_repo = os.getenv(
    "ACTIVE_REPO", ""
)  # Load active_repo from .env, default to empty string if not set
g = None


def author():
    linkedin_url = "https://www.linkedin.com/in/engrshishir/"
    webbrowser.open_new_tab(linkedin_url)


def setup():
    """Set up the GitHub configuration, including authentication token, username, and email."""
    global g

    try:
        from github import Github
    except ImportError:
        print("⚠️ PyGithub is not installed. Installing PyGithub...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyGithub"])

    # Ensure token is available
    if not token:
        print("❌ GitHub token not found. Please set it in the .env file.")
        sys.exit(1)

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
    global active_repo

    try:
        active_repo = input("📂 Enter repository name: ").strip()
        description = input("📝 Enter repository description (optional): ").strip()

        user = g.get_user()
        repo = user.create_repo(
            name=active_repo,
            description=description,
            private=False,
            auto_init=True,
            gitignore_template="Python",
        )
        print(f"✅ Repository '{active_repo}' created successfully!")

        # Update the .env file to reflect the active_repo
        with open(".env", "a") as env_file:
            env_file.write(f"\nACTIVE_REPO={active_repo}")

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
    global active_repo

    active_repo = input("📥 Enter repository name to clone: ").strip()
    clone_url = f"https://{token}@github.com/{user_name}/{active_repo}.git"

    if Path(active_repo).exists():
        print(f"⚠️ Repository '{active_repo}' already exists locally!")
        return

    try:
        subprocess.run(["git", "clone", clone_url], check=True)
        print(f"✅ Repository '{active_repo}' cloned successfully.")
        os.chdir(active_repo)  # Change directory to the cloned repo
        print(f"Now working in repository '{active_repo}'.")

        # Update the .env file to reflect the active_repo
        with open(".env", "a") as env_file:
            env_file.write(f"\nACTIVE_REPO={active_repo}")

    except subprocess.CalledProcessError:
        print("❌ Failed to clone repository! Check repository name or permissions.")


def switch_repo():
    """Switch to a different repository. If not found locally, clone it."""
    global active_repo

    active_repo = input("🔄 Enter repository name to switch to: ").strip()
    repo_path = Path(active_repo)

    if not repo_path.exists():
        print(f"⚠️ Repository '{active_repo}' not found locally! Cloning...")
        clone_repo()  # Call clone_repo() if the repo doesn't exist locally
        return  # Exit after cloning since the repo will be set up by clone_repo()

    try:
        os.chdir(active_repo)  # Change to the directory of the repo
        print(f"✅ Switched to repository '{active_repo}'.")

        # Update or create the ACTIVE_REPO entry in the .env file
        with open(".env", "r") as env_file:
            lines = env_file.readlines()

        # Check if ACTIVE_REPO is already in the .env file
        with open(".env", "w") as env_file:
            updated = False
            for line in lines:
                if line.startswith("ACTIVE_REPO="):
                    # Replace the old ACTIVE_REPO value with the new one
                    env_file.write(f"ACTIVE_REPO={active_repo}\n")
                    updated = True
                else:
                    env_file.write(line)

            if not updated:
                # If ACTIVE_REPO was not found, append it at the end of the .env file
                env_file.write(f"\nACTIVE_REPO={active_repo}\n")

        print(f"✅ .env file updated with ACTIVE_REPO={active_repo}")

    except Exception as e:
        print(f"❌ Error switching repository: {e}")


# The rest of the functions remain the same...
