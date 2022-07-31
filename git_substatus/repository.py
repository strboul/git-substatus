import os
from collections.abc import Iterator

from git_substatus.utils import run_git_command


class Repository:
    def __init__(self, dirs: tuple[str, ...]):
        self.dirs = dirs

    def get_git_repository_paths(self) -> tuple[str, ...]:
        """
        Get the git repositories in a directory.
        """
        sub_git_repos = tuple(self.__git_repositories())
        return sub_git_repos

    def get_repo_names(self) -> tuple[str, ...]:
        sub_git_repos = tuple(self.__git_repositories())
        repo_names = tuple(os.path.basename(repo) for repo in sub_git_repos)
        return repo_names

    def __git_repositories(self) -> Iterator[str]:
        for d in self.dirs:
            is_git_repo = self.__is_git_repository(d)
            if is_git_repo:
                yield d

    def __is_git_repository(self, path: str) -> bool:
        cmd = run_git_command(path, ["rev-parse", "--show-toplevel"])
        output = "".join(cmd["output"].split())
        base_cmd = os.path.basename(output)
        base_path = os.path.basename(path)
        return bool(True if base_cmd == base_path else False)
