from setuptools import setup, find_packages

setup(
    name='engr_colab_github',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'PyGithub',
    ],
    entry_points={
        'console_scripts': [
            'setup-git=engr_colab_github.git_utils:setup',
            'clone-repo=engr_colab_github.git_utils:clone_repo',
        ],
    },
)
