from git_substatus.numstatus import NumStatus
from git_substatus.utils import run_git_command


def get_stash_num(path: str) -> str:
    cmd = run_git_command(path, ["rev-list", "--walk-reflogs", "--count", "refs/stash"])
    output = cmd["output"].replace("\n", "")
    return output


txt = {"singular": "stash", "plural": "stashes"}


class Stash(NumStatus):
    def __init__(self, repos, txt=txt, fun_get_num=get_stash_num):
        super().__init__(repos, txt, fun_get_num)
