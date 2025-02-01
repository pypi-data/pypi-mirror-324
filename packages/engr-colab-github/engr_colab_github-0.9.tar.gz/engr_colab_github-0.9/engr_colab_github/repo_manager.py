import subprocess
from pathlib import Path
import webbrowser
import sys
from github import Github
from dotenv import load_dotenv, set_key, dotenv_values

# Load environment variables from the .env file located in the root directory
env_vars = dotenv_values(
    Path(__file__).parent.parent / ".env"
)  # Assuming .env is in the parent directory

g = None

# Retrieve the variables from the environment
token = env_vars.get("GITHUB_TOKEN")
user_name = env_vars.get("GITHUB_USER_NAME")
user_email = env_vars.get("GITHUB_EMAIL")
active_repo = env_vars.get("ACTIVE_REPO", "")

# Check if the environment variables are loaded
if not user_name:
    print("❌ GitHub username not found in .env file. Please check the file.")
    sys.exit(1)

if not token:
    print("❌ GitHub token not found. Please set it in the .env file.")
    sys.exit(1)


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
        env_file_path = Path(__file__).parent.parent / ".env"
        with env_file_path.open("a") as env_file:
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
    # Load environment variables directly from the .env file
    load_dotenv()

    # Retrieve the necessary environment variables
    user_name = env_vars.get("GITHUB_USER_NAME")
    token = env_vars.get("GITHUB_TOKEN")  # GitHub token

    active_repo = input("📥 Enter repository name to clone: ").strip()
    clone_url = f"https://{token}@github.com/{user_name}/{active_repo}.git"

    active_repo_path = Path(active_repo)

    if active_repo_path.exists():
        print(f"⚠️ Repository '{active_repo}' already exists locally!")
        return

    try:
        subprocess.run(["git", "clone", clone_url], check=True)
        print(f"✅ Repository '{active_repo}' cloned successfully.")

        # Check if the script is running locally (for example, on Windows)
        if sys.platform == "win32":
            # Use os.chdir() on Windows or other local systems
            Path(active_repo).resolve()
        else:
            # Use pathlib for non-local environments (e.g., Google Colab)
            path = Path(active_repo).resolve()
            print(f"Now working in repository '{active_repo}' located at {path}.")
            # Optionally, handle directory changes for other environments

        print(f"Now working in repository '{active_repo}'.")

        # Update the .env file to reflect the active_repo
        env_file_path = Path(__file__).parent.parent / ".env"
        with env_file_path.open("a") as env_file:
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
        # Change to the directory of the repo
        repo_path.chmod(0o755)
        print(f"✅ Switched to repository '{active_repo}'.")

        # Update or create the ACTIVE_REPO entry in the .env file
        env_file_path = Path(__file__).parent.parent / ".env"
        with env_file_path.open("r") as env_file:
            lines = env_file.readlines()

        # Check if ACTIVE_REPO is already in the .env file
        with env_file_path.open("w") as env_file:
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
