#!/usr/bin/env python3

import pygit2

def status(repo):
    codes = {
        'new': pygit2.GIT_STATUS_WT_NEW,
        'modified': pygit2.GIT_STATUS_WT_MODIFIED,
        'added': pygit2.GIT_STATUS_INDEX_MODIFIED
    }

    status = repo.status()

    for i in status:
        if status[i] in codes.values():
            print("%s  %s" % (status[i], i))

def main():
    workdir = "."
    repo = pygit2.Repository(workdir)
    status(repo)


if __name__ == "__main__":
    main()
