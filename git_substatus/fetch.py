import os

from git_substatus.utils import run_git_command


class Fetch:
    def __init__(self, repos: tuple[str, ...]):
        self.repos = repos

    def do_fetch(self) -> bool:
        """
        Performs a git fetch on the repositories.
        """
        for repo in self.repos:
            self.__do_git_fetch(repo)
        return True

    def __do_git_fetch(self, path) -> bool:
        remote_url = self.__get_remote_url(path)
        if not remote_url["status"]:
            repo_name = os.path.basename(path)
            print(f'can\'t fetch "{repo_name}" remote not exist')
            return False
        print(f'fetching from remote "{remote_url["output"]}"', end="")
        res = run_git_command(path, ["fetch"])
        if not res["status"]:
            print(" ❌")
            return False
        print(" ✅")
        return True

    def __get_remote_url(self, path) -> dict:
        cmd = run_git_command(path, ["config", "--get", "remote.origin.url"])
        cmd["output"] = cmd["output"].strip("\n")
        return cmd
