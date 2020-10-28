from git_substatus.base import *

from git_substatus.utils import run_git_command


class Branch:
    def __init__(self, dirs: Tuple[str, ...]) -> None:
        assert type(dirs) in [tuple]
        self.dirs = dirs

    def get_branch_head(self) -> Tuple[str, ...]:
        """
        Get the current branch head.
        """
        branch_head = tuple(self.__branch_heads())
        return branch_head

    def __branch_heads(self) -> Iterator[str]:
        for d in self.dirs:
            branch_head = self.__current_branch_name(d)
            yield branch_head

    def __current_branch_name(self, path) -> str:
        cmd = run_git_command(path, ["symbolic-ref", "--short", "HEAD"])
        out = cmd.replace("\n", "")
        return out
