import subprocess
from pathlib import Path
import webbrowser
import sys
from github import Github
from dotenv import load_dotenv, set_key, dotenv_values
import os

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

        if env_file_path.exists():
            # Read the existing .env file
            with env_file_path.open("r") as env_file:
                lines = env_file.readlines()

            # Check if ACTIVE_REPO is already in the file
            found = False
            for i, line in enumerate(lines):
                if line.startswith("ACTIVE_REPO="):
                    lines[i] = (
                        f"ACTIVE_REPO={active_repo}\n"  # Update the ACTIVE_REPO value
                    )
                    found = True
                    break

            # If ACTIVE_REPO is not found, append it to the end
            if not found:
                lines.append(f"ACTIVE_REPO={active_repo}\n")

            # Write the updated content back to the .env file
            with env_file_path.open("w") as env_file:
                env_file.writelines(lines)

        else:
            # If the .env file doesn't exist, create it and add ACTIVE_REPO
            with env_file_path.open("w") as env_file:
                env_file.write(f"ACTIVE_REPO={active_repo}\n")

        return repo

    except Exception as e:
        print(f"❌ Failed to create repository! Error: {e}")

    except Exception as e:
        if "Bad credentials" in str(e):
            print(
                "❌ Invalid GitHub token!"
            )
        elif "Requires authentication" in str(e):
            print("❌ You must authenticate using a Personal Access Token (PAT).")
        elif "403" in str(e):
            print("⚠️ Permission denied! Check token permissions at:")
            print("➡️ https://github.com/settings/tokens")
            print("Enable 'Repository' and 'Account' permissions.")
        else:
            print(f"❌ Error: {e}")


def clone_repo():
    load_dotenv()  # Load the environment variables from the .env file

    # Retrieve GitHub username and token from the environment variables
    user_name = os.getenv("GITHUB_USER_NAME")
    token = os.getenv("GITHUB_TOKEN")

    if not user_name or not token:
        print("❌ GitHub credentials are missing from the .env file.")
        return

    active_repo = input("📥 Enter repository name to clone: ").strip()

    # Automatically detect if running in Google Colab or locally
    if "COLAB_GPU" in os.environ:  # Check if it's Google Colab
        print("🌐 Running in Google Colab!")
        clone_location = "/content"  # Clone into Colab's default directory

    else:  # If running locally
        print("💻 Running locally!")
        clone_location = input(
            "Enter the local path where you want to clone the repository: "
        ).strip()

    # Create the full clone URL
    clone_url = f"https://{token}@github.com/{user_name}/{active_repo}.git"
    active_repo_path = Path(clone_location) / active_repo

    # Check if the repository already exists locally
    if active_repo_path.exists():
        print(f"⚠️ Repository '{active_repo}' already exists at '{clone_location}'!")
        return

    # Try to clone the repository
    try:
        subprocess.run(["git", "clone", clone_url, str(active_repo_path)], check=True)
        print(
            f"✅ Repository '{active_repo}' cloned successfully to {active_repo_path}."
        )

        # Update the .env file to reflect the active_repo
        # Update the .env file to reflect the active_repo
        env_file_path = Path(__file__).parent.parent / ".env"

        if env_file_path.exists():
            # Read the existing .env file
            with env_file_path.open("r") as env_file:
                lines = env_file.readlines()

            # Check if ACTIVE_REPO is already in the file
            found = False
            for i, line in enumerate(lines):
                if line.startswith("ACTIVE_REPO="):
                    lines[i] = (
                        f"ACTIVE_REPO={active_repo}\n"  # Update the ACTIVE_REPO value
                    )
                    found = True
                    break

            # If ACTIVE_REPO is not found, append it to the end
            if not found:
                lines.append(f"ACTIVE_REPO={active_repo}\n")

            # Write the updated content back to the .env file
            with env_file_path.open("w") as env_file:
                env_file.writelines(lines)

        else:
            # If the .env file doesn't exist, create it and add ACTIVE_REPO
            with env_file_path.open("w") as env_file:
                env_file.write(f"ACTIVE_REPO={active_repo}\n")

    except subprocess.CalledProcessError:
        print("❌ Failed to clone repository! Check repository name or permissions.")


def switch_repo():
    global active_repo

    active_repo = input("🔄 Enter repository name to switch to: ").strip()
    repo_path = Path(active_repo)

    if not repo_path.exists():
        print(f"⚠️ Repository '{active_repo}' not found locally! Cloning...")
        clone_repo()  # Call clone_repo() if the repo doesn't exist locally
        return  # Exit after cloning since the repo will be set up by clone_repo()

    try:
        repo_path.chmod(0o755)
        print(f"✅ Switched to repository '{active_repo}'.")

        env_file_path = Path(__file__).parent.parent / ".env"
        with env_file_path.open("r") as env_file:
            lines = env_file.readlines()

        with env_file_path.open("w") as env_file:
            updated = False
            for line in lines:
                if line.startswith("ACTIVE_REPO="):
                    env_file.write(f"ACTIVE_REPO={active_repo}\n")
                    updated = True
                else:
                    env_file.write(line)

            if not updated:
                env_file.write(f"\nACTIVE_REPO={active_repo}\n")

        print(f"✅ .env file updated with ACTIVE_REPO={active_repo}")

    except Exception as e:
        print(f"❌ Error switching repository: {e}")
