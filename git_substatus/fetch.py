from git_substatus.base import *

from git_substatus.utils import run_git_command


class Fetch:
    def __init__(self, repos: Tuple[str, ...]):
        self.repos = repos

    def do_fetch(self) -> bool:
        """
        Performs a git fetch on the repositories.
        """
        for repo in self.repos:
            self.__do_git_fetch(repo)
        print("All fetched.")
        return True

    def __do_git_fetch(self, path) -> bool:
        repo_name = os.path.basename(path)
        print(f'Fetching from remote "{repo_name}"')
        run_git_command(path, ["fetch"])
        return True
