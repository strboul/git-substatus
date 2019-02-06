#!/usr/bin/env python3

import os
import pygit2
import argparse

def get_gitdirs(path):
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
    parser = argparse.ArgumentParser(description="See subfolders' git status")
    parser.add_argument("path", help="path where you see status. Current directory will be displayed if left empty.")
    args = parser.parse_args()
    args.path
    # return current if path is empty:
    if args.path is not None:
        path_arg = arg
    else:
        path_arg = "."
    path_arg

def repo(dirlist):
    assert isinstance(dirlist, list)
    repo = []
    for dir in dirlist:
        repo.append(pygit2.Repository(dir))
    return repo

def status(repolist):
    assert isinstance(repolist, list)

    codes = {
        'new': pygit2.GIT_STATUS_WT_NEW, #128
        'modified': pygit2.GIT_STATUS_WT_MODIFIED, #256
        'added': pygit2.GIT_STATUS_INDEX_MODIFIED #2
    }
    # inversing is just more useful:
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
    # path_arg = cmdarg()
    path_arg = "~/proj"
    path = os.path.expanduser(path_arg)
    dirs = get_gitdirs(path)
    repo_dirs = repo(dirs)
    statuses = status(repo_dirs)
    # print(statuses)

if __name__ == "__main__":
    main()
