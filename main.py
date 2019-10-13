#!/usr/bin/env python3

import os
import pygit2
import argparse

def get_git_dirs(path):
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


def cmdarg():
    '''
    Command line arguments
    Returns path argument
    '''
    parser = argparse.ArgumentParser(description = "See subfolders' git status")
    parser.add_argument("path", help = "path indicating where you want to see substatuses. If left empty, current working directory will be chosen.")
    args = parser.parse_args()

    ## return the current working directory 
    ## if the path arg is empty:
    if args.path is not None:
        ## check if dir exists:
        if os.path.exists(args.path):
            path_arg = args.path
        else:
            print("folder '%s' not exist" %(args.path))
            raise FileNotFoundError
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

    codes = {
        'new': pygit2.GIT_STATUS_WT_NEW, #128
        'modified': pygit2.GIT_STATUS_WT_MODIFIED, #256
        'added': pygit2.GIT_STATUS_INDEX_MODIFIED #2
    }
    ## inversing is just more useful:
    inverse_codes = {v: k for k, v in codes.items()}

    status = []
    for repo in repolist:
        status.append([repo.workdir, repo.status()])

    status_items = []
    info = []
    for stat in status:
        workdir = stat[0]
        items = list(stat[1].items())
        for s in range(0, len(items)):
            single_items = list(items[s])
            value = single_items[1]
            if value in codes.values():
                status_items.append([single_items[0], inverse_codes[value]])
            else:
                continue
        info.append([workdir, status_items[-1]])

    print(info)
    return info

def main():
    path_arg = cmdarg()
    print(path_arg)
    # full_path = os.path.expanduser(path_arg)
    # dirs = get_git_dirs(full_path)
    # repo_dirs = as_pygit_repo(dirs)
    # statuses = git_status(repo_dirs)
    # print(statuses)

if __name__ == "__main__":
    main()
