from setuptools import setup, find_packages

setup(
    name='engr_colab_github',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'PyGithub',
    ],
    entry_points={
        'console_scripts': [
            'setup-git=engr_colab_github.setup:setup',
            'create-repo=engr_colab_github.repo_manager:create_repo',
            'clone-repo=engr_colab_github.repo_manager:clone_repo',
            'switch-repo=engr_colab_github.repo_manager:switch_repo',
            'git-add=engr_colab_github.git_operations:git_add',
            'git-commit=engr_colab_github.git_operations:git_commit',
            'git-push=engr_colab_github.git_operations:git_push',
            'force_push=engr_colab_github.git_operations:force_push',
            'git-status=engr_colab_github.git_operations:git_status',
            'git-log=engr_colab_github.git_operations:git_log',
            'merge-branch=engr_colab_github.git_operations:merge_branch',
            'delete-path=engr_colab_github.utils:delete_path',
            'author=engr_colab_github.utils:author',
        ],
    },
)
