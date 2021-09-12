from git_substatus.base import *

from git_substatus.numstatus import NumStatus
from git_substatus.utils import run_git_command


def get_worktree_num(path: str) -> str:
    list_worktrees: str = run_git_command(path, ["worktree", "list"])
    worktrees_lst: List[str] = list_worktrees.split("\n")
    wt = list(filter(None, worktrees_lst))
    wt_len = len(wt)
    out = [str(wt_len - 1) if wt_len > 1 else ""][0]
    return out


txt = {"singular": "worktree", "plural": "worktrees"}


class Worktree(NumStatus):
    def __init__(self, repos, txt=txt, fun_get_num=get_worktree_num):
        super().__init__(repos, txt, fun_get_num)
