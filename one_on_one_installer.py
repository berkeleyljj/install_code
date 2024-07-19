import os
import sys

from paths import REPOS_DIR, PDM_BIN_DIR
from bash_utils import run_subprocess_shell
from install_single_repo import install_single_repo


def main():
    # Ensure a repository name is provided
    if len(sys.argv) < 2:
        print("Usage: python parallel_installer.py <repo_name>")
        sys.exit(1)

    repo_name = sys.argv[1]

    # Modify pdm
    print(f"Setting up pdm...")

    result = run_subprocess_shell(
        f"export PATH={PDM_BIN_DIR} \
            && pdm --version \
            && pdm config install.cache on \
            && pdm config venv.with_pip on \
            && pdm config venv.backend virtualenv \
            && pdm add -g setuptools \
            && pdm add -g wheel \
            && pip install pipreqs\
        ",
    )

    if result.returncode != 0:
        print("Failed to set up pdm")
        sys.exit(1)


    # Install the single repository
    try:
        install_single_repo(repo_name)
    except Exception as e:
        print(f"Failed to install {repo_name}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
