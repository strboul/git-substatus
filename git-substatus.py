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

### ----------------------------------------------------------------- ###
### GIT CALLS ----
### ----------------------------------------------------------------- ###
def get_git_dirs(path):
    """
    Only returns directories that have a `.git` directory
    """
    count = 0
    var = []
    for root, dirs, files in os.walk(path):
        if count != 1:
            for dir in dirs:
                fullpat = os.path.join(root, dir)
                gitpat = os.path.join(fullpat, '.git')
                if os.path.exists(gitpat):
                    var.append(fullpat)
                else:
                    continue
            count += 1
        else:
            break
    return var

def cmd_args():
    """
    Command line arguments
    Returns the path argument
    Notes:
    nargs='?' makes the argument optional.
    """
    parser = argparse.ArgumentParser(description="See subfolders' git status")
    parser.add_argument("path", nargs="?", help="path indicating where you want to see substatuses. If left empty, current working directory will be chosen.")
    args = parser.parse_args()

    ## return the current working directory 
    ## if the path arg is empty:
    if args.path is not None:
        ## check if dir exists:
        if os.path.exists(args.path):
            path_arg = args.path
        else:
            s = "Error: cannot find the specified directory '%s'" %(args.path)
            ## send signal SIGHUP 1 and exit:
            raise SystemExit(fancy_text(s, "red"))
    else:
        path_arg = "."
    return path_arg

def as_pygit_repo(dirlist):
    assert isinstance(dirlist, list)
    repo = []
    for dir in dirlist:
        repo.append(pygit2.Repository(dir))
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
        repo_status_list.append([repo.workdir, branch, status])

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
        workdir_base = get_basename(workdir)
        info.append([workdir_base, branch, repo_status_items])
    
    ## sort list alphabetically by the workdir name:
    info = sorted(info, key=lambda i: i[0])
    return info

def git_status_print(statuses):
    assert isinstance(statuses, list)
    for status in statuses:
        dirname = status[0]
        branch = status[1]
        codes = status[2]
        if len(codes) > 0:
            codes_counter = Counter(codes)
            unique_codes = list(set(codes))
            codes_fmt = []
            for code in unique_codes:
                count = codes_counter.get(code)
                str = "{count} {code}".format(count=count,code=code)
                codes_fmt.append(str)
                collapsed_codes = ', '.join(codes_fmt)
                codes_out = fancy_text(collapsed_codes, "yellow")
        else:
            codes_out = fancy_text("<sync>", "green", "italic")
        out_fmt = "• {dirname} [{branch}] {codes_out}".format(
            dirname=fancy_text(dirname, "blue", style=["bold", "underline"]),
            branch=fancy_text(branch, "white"),
            codes_out=codes_out
        )
        print(out_fmt)
    print("") # one-line padding after listing repos.

def main():
    path_arg = cmd_args()
    full_path = os.path.expanduser(path_arg)
    dirs = get_git_dirs(full_path)
    if len(dirs) is 0:
        return print("no sub git directories found")
    else:
        print(" directory: <%s>" %(path_arg))
    pygit_repos = as_pygit_repo(dirs)
    statuses = git_status(pygit_repos)
    git_status_print(statuses)

### ----------------------------------------------------------------- ###
### MAIN ----
### ----------------------------------------------------------------- ###
if __name__ == "__main__":
    main()
