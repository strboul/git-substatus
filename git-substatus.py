#!/usr/bin/env python3

# Standard modules:
# which are from the Python Standard Library:
# https://docs.python.org/3/library/index.html
import os
import subprocess
import argparse
from collections import Counter

# Custom modules:
try:
    import pygit2
except ModuleNotFoundError:
    raise SystemExit(
        """
        module \"pygit2\" required to make git-substatus work,
        please install it
        """
    )

# # ---------------------------------------------------------------- # #
# # -- UTILS ------
# # ---------------------------------------------------------------- # #


def fancy_text(text, color, style=None):
    """
    Examples:
    print(fancy_text("Grass", "green"))
    print(fancy_text("Sky", "blue", style="bold"))
    print(fancy_text("Apple", "red", style=["bold", "underline"]))
    """
    reset = "\033[0m"
    ansi_colors = {
        "black": "",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "white": "\033[37m"
    }
    ansi_styles = {
        "bold": "\033[1m",
        "italic": "\033[3m",
        "underline": "\033[4m"
    }
    ansi_color = ansi_colors[color]
    if style is not None:
        if type(style) is list:
            ansi_style = "".join([ansi_styles.get(k) for k in style])
        else:
            ansi_style = ansi_styles[style]
    else:
        ansi_style = ""
    text = "{style}{color}{text}{reset}".format(
        style=ansi_style,
        color=ansi_color,
        text=text,
        reset=reset
    )
    return text


def get_basename(path):
    return os.path.basename(os.path.normpath(path))


def match_string_in_list(x, string):
    """
    Find a string inside list elements
    """
    assert isinstance(x, list)
    assert isinstance(string, str)
    return [s for s in x if string in s]


def commit_text(x):
    """
    It changes the 'commit' text based on one or many.
    """
    txt = "commits" if x > 1 else "commit"
    return txt


def exit_program(message):
    """
    sends SIGHUP 1 signal and exits:
    """
    raise SystemExit(fancy_text(message, "red"))

# # ---------------------------------------------------------------- # #
# # -- GIT CALLS------
# # ---------------------------------------------------------------- # #


def get_git_dirs(path, get_hidden_dirs=False):
    """
    Only returns directories that have a `.git` directory
    """
    count = 0
    var = []
    for root, dirs, files in os.walk(path):
        if count != 1:
            for Dir in dirs:
                if Dir.startswith(".") and not get_hidden_dirs:
                    continue
                fullpat = os.path.join(root, Dir)
                gitpat = os.path.join(fullpat, ".git")
                if os.path.exists(gitpat):
                    var.append(fullpat)
                else:
                    continue
            count += 1
        else:
            break
    return var


def get_cmd_args():
    """
    Command line arguments
    Returns the path argument
    Notes:
    nargs="?" makes the argument optional.
    """
    parser = argparse.ArgumentParser(
        description="""
        See subfolders' git status
        """
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="""
        path indicating where you want to see substatuses.
        If left empty, current working directory will be chosen.
        """
    )
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="git fetch from remote repositories"
    )
    parser.add_argument(
        "--dont-ignore-hidden",
        action="store_true",
        help="if selected, the directories starting with dot are not ignored"
    )
    args = parser.parse_args()

    # return the current working directory
    # if the path arg is empty:
    path_arg = "."

    if args.path is not None:
        expanded_path = os.path.expanduser(args.path)
        # check if dir exists:
        if os.path.exists(expanded_path):
            path_arg = expanded_path
        else:
            txt = "Error: cannot find the specified directory '{path}'".format(
                path=expanded_path
            )
            exit_program(txt)

    out = {
        "path_arg": path_arg,
        "fetch": args.fetch,
        "dont_ignore_hidden": args.dont_ignore_hidden
    }
    return out


def as_pygit_repo(dirlist):
    assert isinstance(dirlist, list)
    repo = []
    for Dir in dirlist:
        repo.append(pygit2.Repository(Dir))
    return repo


def git_status(repolist):
    assert isinstance(repolist, list)

    status_codes = {
        "new": pygit2.GIT_STATUS_WT_NEW,  # 128
        "modified": pygit2.GIT_STATUS_WT_MODIFIED,  # 256
        "deleted": pygit2.GIT_STATUS_WT_DELETED,  # 512
        "renamed": pygit2.GIT_STATUS_WT_RENAMED,  # 2048
        "added": pygit2.GIT_STATUS_INDEX_MODIFIED,  # 2
        "merge conflict": pygit2.GIT_STATUS_CONFLICTED  # 32768
    }
    # inversing status codes useful:
    inverse_status_codes = {v: k for k, v in status_codes.items()}

    repo_status_list = []
    for repo in repolist:
        try:
            branch = repo.head.shorthand
        except pygit2.GitError:  # return None if no branch found
            branch = None
        status = repo.status()

        # diverging commits between the remote and local branch:
        try:
            local_head = repo.revparse_single("HEAD")
        except KeyError:
            local_head = None

        # same origin as the current branch:
        if branch is not None:
            ref = "refs/remotes/origin/" + branch
            # be sure that that ref exist in the repo references:
            assert len(match_string_in_list(repo.listall_references(), ref)) > 0
        else:
            ref = "HEAD"

        try:
            origin_head = repo.revparse_single(ref)
        except KeyError:
            origin_head = None

        if origin_head is not None:
            diff = repo.ahead_behind(local_head.id, origin_head.id)
        else:
            diff = None

        repo_status_list.append([repo.workdir, branch, status, diff])

    info = []
    for stat in repo_status_list:
        repo_status_items = []
        workdir = stat[0]
        branch = stat[1]
        items = list(stat[2].items())
        for s in range(0, len(items)):
            single_items = list(items[s])
            value = single_items[1]
            if value in status_codes.values():
                repo_status_items.append(inverse_status_codes[value])
            else:
                continue
        diverging_commits = stat[3]
        workdir_base = get_basename(workdir)
        info.append([workdir_base, branch, repo_status_items, diverging_commits])

    # sort list alphabetically by the workdir name:
    info = sorted(info, key=lambda i: i[0])
    return info


def git_status_print(statuses):
    assert isinstance(statuses, list)
    for status in statuses:
        codes_out = []
        dirname = status[0]
        branch = status[1]
        codes = status[2]
        diverging = status[3]
        if len(codes) > 0:
            codes_counter = Counter(codes)
            unique_codes = list(set(codes))
            collapsed_codes = ""
            codes_fmt = []
            for code in unique_codes:
                count = codes_counter.get(code)
                txt = "{count} {code}".format(count=count, code=code)
                codes_fmt.append(txt)
                collapsed_codes = ", ".join(codes_fmt)
            codes_out.append(fancy_text(collapsed_codes, "yellow"))

        if diverging is not None:
            div_local = diverging[0]
            div_remote = diverging[1]
            div_msg = []

            if div_local is not 0:
                div_local_msg = "{local} {commit} ahead".format(
                    local=div_local,
                    commit=commit_text(div_local)
                )
                div_msg.append(div_local_msg)

            if div_remote is not 0:
                div_remote_msg = "{remote} {commit} behind".format(
                    remote=div_remote,
                    commit=commit_text(div_remote)
                )
                div_msg.append(div_remote_msg)

            if len(div_msg) > 0:
                text = fancy_text(", ".join(div_msg) + " origin", "yellow")
                codes_out.append(text)

        # if there are no codes and no diverging, just out "sync" text,
        # else, concat items in the list:
        if not len(codes_out) > 0:
            codes_out = fancy_text("<sync>", "green", "italic")
        else:
            codes_out = " | ".join(codes_out)
        out_format = "• {dirname} [{branch}] {codes_out}".format(
            dirname=fancy_text(dirname, "blue", style=["bold", "underline"]),
            branch=fancy_text(branch, "white"),
            codes_out=codes_out
        )
        print(out_format)
    print("")  # one-line padding after listing repos.


def do_git_fetch(repolist):
    """
    Perform a `git fetch` on each repository
    """
    # `pygit2.Keypair(username, pubkey, privkey, passphrase)`
    # ssh_keypair=pygit2.Keypair("git", "id_rsa.pub", "id_rsa", "")
    currpat = os.getcwd()
    for repo in repolist:
        repo_refs = repo.listall_references()
        target = match_string_in_list(repo_refs, "remote")
        if not len(target) > 0:
            continue
        # commented out code, replaced with OS system call because
        # of the bug in the libgit2/pygit2.
        # https://github.com/libgit2/pygit2/issues/836
        # remote = repo.remotes[0]
        # try:    
        #     remote.fetch(callbacks=ssh_keypair)
        # except pygit2.GitError as fetch_err:
        #     txt = """
        #     cannot fetch \"{repo}\" repository...
        #     {error_msg}
        #     (If this problem persists, don't use the `--fetch` tag for a while.)
        #     """.format(repo=get_basename(repo.workdir), error_msg=str(fetch_err))
        #     exit_program(txt)
        os.chdir(repo.workdir)
        print("\033[K Fetching repository: {dir}\r".format(dir=os.getcwd()), end="")
        subprocess.call(["git", "fetch"], stdout=subprocess.DEVNULL)
    print("\033[K All fetched.")
    # return to the current path after all:
    os.chdir(currpat)
    return True


# # ---------------------------------------------------------------- # #
# # -- MAIN------
# # ---------------------------------------------------------------- # #

def main():
    cmd_args = get_cmd_args()
    git_dirs = get_git_dirs(
        cmd_args.get("path_arg"),
        cmd_args.get("dont_ignore_hidden")
    )

    if len(git_dirs) is 0:
        return print("no sub git directories found")
    else:
        # turn path into canonical and get basename:
        parg = cmd_args.get("path_arg")
        if parg is ".":
            parg = os.path.realpath(".")
        print(" directory: <%s>" % parg)

    pygit_repos = as_pygit_repo(git_dirs)
    if cmd_args.get("fetch"):
        do_git_fetch(pygit_repos)
    statuses = git_status(pygit_repos)
    git_status_print(statuses)
    return True


if __name__ == "__main__":
    main()

