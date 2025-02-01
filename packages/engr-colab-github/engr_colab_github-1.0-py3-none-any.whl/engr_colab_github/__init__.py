from .setup import setup
from .repo_manager import create_repo, clone_repo, switch_repo
from .git_operations import git_add, git_commit, git_push,force_push, git_status, git_log, merge_branch
from .utils import author, delete_path

__all__ = [
    "setup",
    "create_repo",
    "clone_repo",
    "switch_repo",
    "git_add",
    "git_commit",
    "git_push",
    "force_push",
    "git_status",
    "git_log",
    "merge_branch",
    "delete_path",
    "author"
]

# Track the active repository (shared state)
active_repo = None
