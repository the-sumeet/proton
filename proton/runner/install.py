import subprocess
from pathlib import Path


def fe_install(fe_path: str | Path):

    # Just execute "fe:install" of a project.
    # Execute shell command
    subprocess.run(["ls", "-l"])
