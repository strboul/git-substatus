#!/usr/bin/env python3

## standard modules:
import os
from collections import Counter

## project-specific modules:
import pygit2
import argparse

### ----------------------------------------------------------------- ###
### UTILS ----
### ----------------------------------------------------------------- ###
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
        "bold" : "\033[1m",
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
    str = "{style}{color}{text}{reset}".format(
        style=ansi_style, 
        color=ansi_color, 
        text=text, 
        reset=reset
    )
    return str

def get_basename(path):
    return os.path.basename(os.path.normpath(path))

def match_string_in_list(x, string):
    """
    Find a string inside list elements
    """
    assert isinstance(x, list)
    assert isinstance(string, str)
    return [s for s in x if string in s]

### ----------------------------------------------------------------- ###
### GIT CALLS ----
### ----------------------------------------------------------------- ###
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
                gitpat = os.path.join(fullpat, '.git')
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
    nargs='?' makes the argument optional.
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

    ## return the current working directory 
    ## if the path arg is empty:
    if args.path is not None:
        expanded_path = os.path.expanduser(args.path)
        ## check if dir exists:
        if os.path.exists(expanded_path):
            path_arg = expanded_path
        else:
            s = "Error: cannot find the specified directory '%s'" %(expanded_path)
            ## send signal SIGHUP 1 and exit:
            raise SystemExit(fancy_text(s, "red"))
    else:
        path_arg = "."
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
        "new": pygit2.GIT_STATUS_WT_NEW, #128
        "modified": pygit2.GIT_STATUS_WT_MODIFIED, #256
        "deleted": pygit2.GIT_STATUS_WT_DELETED, #512
        "renamed": pygit2.GIT_STATUS_WT_RENAMED, #2048
        "added": pygit2.GIT_STATUS_INDEX_MODIFIED, #2
        "merge conflict": pygit2.GIT_STATUS_CONFLICTED #32768
    }
    ## inversing status codes useful:
    inverse_status_codes = {v: k for k, v in status_codes.items()}

    repo_status_list = []
    for repo in repolist:
        try:
            branch = repo.head.shorthand
        except pygit2.GitError: ## return None if no branch found
            branch = None
        status = repo.status()

        ## diverging commits between the remote and local branch:
        try: 
            local_head = repo.revparse_single("HEAD")
        except KeyError:
            local_head = None
        try: 
            ## origin/master vs origin/HEAD
            origin_master = repo.revparse_single('origin/master')
        except KeyError:
            origin_master = None
        if origin_master is not None:
            diff = repo.ahead_behind(local_head.id, origin_master.id)
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
    
    ## sort list alphabetically by the workdir name:
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
            codes_fmt = []
            for code in unique_codes:
                count = codes_counter.get(code)
                str = "{count} {code}".format(count=count,code=code)
                codes_fmt.append(str)
                collapsed_codes = ", ".join(codes_fmt)
            codes_out.append(fancy_text(collapsed_codes, "yellow"))
        if not diverging is None:
            div_local=diverging[0]
            div_remote=diverging[1]
            if div_local is not 0 and div_remote is not 0:
                text = "{local} local commit, {remote} remote commit diverged".format(
                    local=div_local, 
                    remote=div_remote
                )
                codes_out.append(text)
        
        ## if there's no codes and no diverging, just out "sync" text,
        ## else, concat items in the list
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
    print("") # one-line padding after listing repos.

def do_git_fetch(repolist):
    """
    Perform fetch on each repository
    """
    for repo in repolist:
        repo_refs = list(repo.references)
        src = match_string_in_list(repo_refs, "head")
        target = match_string_in_list(repo_refs, "remote")
        if not len(target) > 0:
            continue
        remote = repo.remotes[0]
        print(" Fetching repository: %s" %(get_basename(repo.workdir)))
        remote.fetch()

def main():
    cmd_args = get_cmd_args()
    git_dirs = get_git_dirs(
        cmd_args.get("path_arg"),
        cmd_args.get("dont_ignore_hidden")
    )
    if len(git_dirs) is 0:
        return print("no sub git directories found")
    else:
        print(" directory: <%s>" %(cmd_args.get("path_arg")))
    pygit_repos = as_pygit_repo(git_dirs)
    if cmd_args.get("fetch"):
        do_git_fetch(pygit_repos)
    statuses = git_status(pygit_repos)
    git_status_print(statuses)

### ----------------------------------------------------------------- ###
### MAIN ----
### ----------------------------------------------------------------- ###
if __name__ == "__main__":
    main()

