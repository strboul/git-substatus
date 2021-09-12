from git_substatus.base import *

from git_substatus.directory import Directory
from git_substatus.repository import Repository
from git_substatus.worktree import Worktree
from git_substatus.fetch import Fetch
from git_substatus.branch import Branch
from git_substatus.status import Status
from git_substatus.stash import Stash

from git_substatus.utils import display_table, fancy_text


class GitSubstatusApplication:
    def __init__(self, args: Dict[str, str]):
        self.args = args

    def exec(self) -> int:
        """
        The main function to execute git-substatus with given arguments.
        """
        directory = Directory(self.args["path"], bool(self.args["dont_ignore_hidden"]))
        sub_dirs = directory.get_sub_directories()

        repository = Repository(sub_dirs)
        git_repos = repository.get_git_repository_paths()

        if len(git_repos) is 0:
            print("no sub git repositories found", file=sys.stderr)
            sys.exit(1)

        if self.args["fetch"]:
            fetch = Fetch(git_repos)
            fetch.do_fetch()

        worktree = Worktree(git_repos)

        branch = Branch(git_repos)
        status = Status(git_repos)
        stash = Stash(git_repos)

        repos = repository.get_repo_names()
        worktrees = worktree.get_num()

        if any(worktrees):
            repo_wt = zip(repos, worktrees)

            def append_worktrees(repo_wt):
                for repo in repo_wt:
                    out = repo[0] + " (*WT)" if repo[1] else repo[0]
                    yield out

            repos = append_worktrees(repo_wt)

        branch_heads = branch.get_branch_head()
        statuses = status.get_status()
        stashes = stash.get_num()

        # Color columns ------------
        def color_comp(elem, **aesthetics):
            return tuple(fancy_text(el, **aesthetics) for el in elem)

        repos = color_comp(repos, color="blue", styles=("bold",))

        branch_heads = color_comp(branch_heads, color="white", styles=("underline",))

        stashes = color_comp(stashes, color="cyan")

        worktrees = color_comp(worktrees, color="magenta")

        def colorize_status(s):
            if s == "<sync>":
                return fancy_text(s, "green", styles=("italic",))
            return fancy_text(s, "yellow")

        statuses = tuple(colorize_status(status) for status in statuses)

        comp_cols = (
            repos,
            branch_heads,
            statuses,
            stashes,
            worktrees,
        )

        print(fancy_text(f" directory: <{directory.path}>", "gray"))
        display_table(comp_cols)

        print("")

        return 0
