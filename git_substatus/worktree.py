from git_substatus.base import *

from git_substatus.utils import run_git_command


class Worktree:
    def __init__(self, repos: Tuple[str, ...]):
        self.repos = repos

    def have_worktree(self) -> Tuple[bool, ...]:
        worktrees = tuple(self.__worktrees())
        return worktrees

    def __worktrees(self) -> Iterator[bool]:
        for repo in self.repos:
            has_worktree = self.__has_worktree(repo)
            yield has_worktree

    def __has_worktree(self, path: str) -> bool:
        list_worktrees: str = run_git_command(path, ["worktree", "list"])
        worktrees_lst: List[str] = list_worktrees.split("\n")
        worktrees_lst = list(filter(None, worktrees_lst))
        if len(worktrees_lst) > 1:
            return True
        return False
