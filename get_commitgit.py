from pathlib import Path
from git import Repo


def get_diff(working_dir: str = Path().absolute()) -> str:
    repo = Repo(working_dir)
    current_head = repo.head.commit.hexsha

    try:
        master_head = repo.refs.master.commit.hexsha
    except AttributeError:
        master_head = repo.refs.main.commit.hexsha
    diff_text = repo.git.diff(master_head, current_head, "--unified=0", "-W")
    return diff_text
