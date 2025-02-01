[<img src="https://i.postimg.cc/nrTbcvNQ/pypi.png" alt="pypi" style="width:100%;"/>](https://pypi.org/project/engr-colab-github/)

# GitHub Automation Script

This script automates common GitHub-related operations, including setup, repository management, and file handling.

## Table of Contents
1. [Setup Process](#setup-process)
2. [Functions](#functions)
   - [author()](#author)
   - [setup()](#setup)
   - [create_repo()](#create_repo)
   - [clone_repo()](#clone_repo)
   - [upload_file_to_repo()](#upload_file_to_repo)
   - [delete_path()](#delete_path)
   - [git_add()](#git_add)
   - [git_commit()](#git_commit)
   - [git_push()](#git_push)
   - [git_pull()](#git_pull)
   - [git_status()](#git_status)
   - [git_log()](#git_log)
   - [merge_branch()](#merge_branch)
   - [git_reset()](#git_reset)
3. [Author](#author)

---

## Setup Process

1. **GitHub Authentication**: The script requires a GitHub personal access token (PAT) for authentication. You can create one from [here](https://github.com/settings/personal-access-tokens).
2. **Configure Git**: You'll be prompted to enter your GitHub username and email for global Git configuration.

---

## Functions

### 1. `author()`
   - Opens your LinkedIn profile in a new browser tab.

### 2. `setup()`
   - Prompts you to enter your GitHub personal access token, username, and email.
   - Configures Git with the provided username and email.

### 3. `create_repo()`
   - Prompts you to enter the repository name and description.
   - Creates a new public GitHub repository with the provided details.

### 4. `clone_repo()`
   - Prompts you to enter the repository name you want to clone.
   - Clones the specified GitHub repository to your local machine.

### 5. `stage_specific_path()`
   - Prompts you to enter the file path of the file you want to stage for commit.
   - Stages the file and reminds you to commit and push it manually.

### 6. `delete_path()`
   - Prompts you to enter the path of a file or folder you want to delete.
   - Deletes the specified file or folder.

### 7. `git_add()`
   - Prompts you to enter the path of a file or folder you want to add to the staging area.
   - Adds the specified file or folder to the staging area.

### 8. `git_commit()`
   - Prompts you to enter a commit message and an optional description.
   - Commits the staged changes with the provided message and description.

### 9. `git_push()`
   - Prompts you to enter a version number and pushes the changes to the remote repository.
   - Commits the changes with a versioned commit message and includes the current date.

### 10. `git_pull()`
   - Pulls the latest updates from the remote repository.
   - Updates your local repository with the latest changes.

### 11. `git_status()`
   - Runs `git status` to display the state of the working directory and staging area.

### 12. `git_log()`
   - Runs `git log` to show the commit history.

### 13. `merge_branch()`
   - Prompts you to enter a branch name and merges that branch into the current branch.

### 14. `git_reset()`
   - Resets the working directory to the latest commit, discarding all local changes.

---

## Author 
- **LinkedIn**: [engrshishir](https://www.linkedin.com/in/engrshishir/)
- **GitHub**: [engrshishir](https://github.com/engrshishir)
