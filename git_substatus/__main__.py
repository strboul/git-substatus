from git_substatus.utils import fancy_text


def run():
    from git_substatus.utils import check_git_installed

    check_git_installed()

    from git_substatus.cmdline import CmdLine

    args = CmdLine().get_args()

    from git_substatus.gitsubstatus import GitSubstatusApplication

    GitSubstatusApplication(args).exec()


def main():
    try:
        run()
    except Exception as e:
        msg = str(e)
        if msg.startswith("Error:"):
            msg = fancy_text(msg, "red")
        raise SystemExit(msg)


if __name__ == "__main__":
    main()
