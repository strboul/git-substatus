from git_substatus.base import *

from git_substatus.utils import run_git_command


class Stash:
    def __init__(self, repos: Tuple[str, ...]):
        self.repos = repos

    def get_stash_num(self) -> Tuple[str, ...]:
        """
        Get the number of stashes.
        """
        stash_num = tuple(self.__num_stashes())
        return stash_num

    def __num_stashes(self) -> Iterator[str]:
        for repo in self.repos:
            num_stash = self.__get_num_stash(repo)
            if len(num_stash) > 0:
                num_stash = self.__get_num_stash_text(num_stash)
            yield num_stash

    def __get_num_stash_text(self, num: str) -> str:
        txt = "stashes" if int(num) > 1 else "stash"
        return f"{num} {txt}"

    def __get_num_stash(self, path) -> str:
        cmd = run_git_command(
            path,
            ["rev-list", "--walk-reflogs", "--count", "refs/stash"]
        )
        out = cmd.replace("\n", "")
        return out
