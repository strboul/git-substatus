import sys


def main():
    from git_substatus.utils import check_git_installed

    check_git_installed()

    from git_substatus.cmdline import CmdLine

    args = CmdLine().get_args()

    from git_substatus.gitsubstatus import GitSubstatusApplication

    GitSubstatusApplication(args).exec()


if __name__ == "__main__":
    sys.exit(main())
