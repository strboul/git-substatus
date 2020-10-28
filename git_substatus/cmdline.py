from git_substatus.base import *

from git_substatus import __version__

from git_substatus.utils import exit_program

import argparse
import textwrap


class CmdLine:
    def get_args(self) -> Union[Dict[str, str], Dict[str, bool], Dict[str, bool]]:
        """
        Get and parse the command line arguments of the program.
        """

        parser = argparse.ArgumentParser(description="See subfolders' git status")

        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version="%(prog)s " + __version__
        )

        parser.add_argument(
            "path",
            nargs="?",
            help=textwrap.dedent(
                """
                a path indicating where you want to see git sub-statuses. If
                left empty, the current working directory is selected.
                """
            ),
        )
        parser.add_argument(
            "--fetch", action="store_true", help="git fetch from remote repositories"
        )
        parser.add_argument(
            "--dont-ignore-hidden",
            action="store_true",
            help=textwrap.dedent(
                """
                if selected, the directories starting with dot are not ignored
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
