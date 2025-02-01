import os
import subprocess
import sys
from github import Github
from dotenv import load_dotenv, set_key

def get_token():
    """Retrieve the GitHub token from a .env file or prompt the user for it."""
    dotenv_path = os.path.join(os.getcwd(), ".env")  # Save it in the current working directory

    # Load environment variables from the predefined .env file if it exists
    load_dotenv(dotenv_path)

    token = os.getenv("GITHUB_TOKEN")

    if token:
        print("✅ Found saved GitHub token in .env file.")
    else:
        # If no token in the .env file, ask the user for it
        has_token = input("Do you already have a GitHub personal access token? (yes/no): ").strip().lower()

        if has_token == "no":
            print("🔗 Create a GitHub personal access token here:")
            print("➡️ https://github.com/settings/personal-access-tokens")
            print("⚠️ Ensure you enable 'Repository' and 'Account' permissions!")

        token = input("🔑 Enter your GitHub personal access token: ").strip()

        # Save the token in the .env file for future use
        set_key(dotenv_path, "GITHUB_TOKEN", token)
        print(f"✅ GitHub token saved in .env file at {dotenv_path}")

    return token

def get_git_user_details():
    """Retrieve GitHub username and email from the .env file or prompt the user for it."""
    dotenv_path = os.path.join(os.getcwd(), ".env")

    # Load environment variables from the predefined .env file if it exists
    load_dotenv(dotenv_path)

    user_name = os.getenv("GITHUB_USER_NAME")
    user_email = os.getenv("GITHUB_USER_EMAIL")

    if user_name and user_email:
        print(f"✅ Found saved GitHub username: {user_name} and email: {user_email} in .env file.")
    else:
        # If no username or email, prompt the user for input
        print("⚠️ Git username and email not set. Please enter them below.")
        user_name = input("👤 Enter your GitHub username: ").strip()
        user_email = input("📧 Enter your GitHub email: ").strip()

        # Save the username and email in the .env file for future use
        set_key(dotenv_path, "GITHUB_USER_NAME", user_name)
        set_key(dotenv_path, "GITHUB_USER_EMAIL", user_email)
        print(f"✅ GitHub username and email saved in .env file at {dotenv_path}")

    return user_name, user_email

def setup():
    """Set up the GitHub configuration, including authentication token, username, and email."""
    # Ensure the token is available
    token = get_token()

    try:
        g = Github(token)
        g.get_user().login  # Validate token
        print("✅ GitHub authentication successful!")
    except Exception:
        print("❌ Invalid GitHub token! Please check and try again.")
        sys.exit(1)

    # Ensure the username and email are available and set them if not
    user_name, user_email = get_git_user_details()

    # Now set the Git configuration globally
    try:
        subprocess.run(["git", "config", "--global", "user.name", user_name], check=True)
        subprocess.run(["git", "config", "--global", "user.email", user_email], check=True)
        print(f"✅ Git configured with username: {user_name}, email: {user_email}")
    except subprocess.CalledProcessError:
        print("❌ Failed to configure Git. Ensure Git is installed and try again.")
        sys.exit(1)
