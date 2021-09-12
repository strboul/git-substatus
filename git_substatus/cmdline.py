from git_substatus.base import *

from git_substatus import __version__

from git_substatus.utils import exit_program

import argparse
import textwrap

CmdArgs = Union[Dict[str, str], Dict[str, bool], Dict[str, bool]]


class CmdLine:
    def get_args(self) -> CmdArgs:
        """
        Get and parse the command line arguments of the program.
        """

        parser = argparse.ArgumentParser(
            prog="git-substatus",
            description=textwrap.dedent(
                """
                See subfolders' git status
                ===========================

                The output consists of four columns:

                repo name | branch head | status | git stashes (if any)

                The string (*WT) seen next to the repo names shows that the
                repo has some git worktrees. See more:
                <https://git-scm.com/docs/git-worktree>
                """
            ),
            formatter_class=argparse.RawTextHelpFormatter,
        )

        parser.add_argument(
            "-v", "--version", action="version", version="%(prog)s " + __version__
        )

        parser.add_argument(
            "path",
            nargs="?",
            help=textwrap.dedent(
                """
                a path to where you want to see git substatuses. If empty, the
                current working directory is selected.
                """
            ),
        )
        parser.add_argument(
            "--fetch",
            action="store_true",
            help="perform git fetch from remote on all sub repositories.",
        )
        parser.add_argument(
            "--dont-ignore-hidden",
            action="store_true",
            help=textwrap.dedent(
                """
                if selected, the repositories starting with a dot are no longer
                ignored.
                """
            ),
        )

        args = parser.parse_args()

        path_arg = self.__settle_path_arg(args.path)

        args_out = {
            "path": path_arg,
            "fetch": args.fetch,
            "dont_ignore_hidden": args.dont_ignore_hidden,
        }

        return args_out

    def __settle_path_arg(self, path_arg: str) -> str:

        if path_arg is None:
            current_wd = os.getcwd()
            settled_path_arg = current_wd
        else:
            expanded_path = os.path.expanduser(path_arg)
            if os.path.exists(expanded_path):
                settled_path_arg = expanded_path
            else:
                exit_program(
                    f"Error: cannot find the specified directory: '{expanded_path}'"
                )

        return settled_path_arg
