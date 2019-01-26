# git-substatus

A small Python 3 script to find the git status in subdirectories (e.g. project/ folder) where I'd like to see what changes I have regarding uncommitted/unpushed.

A similar bash command:
```
find . -maxdepth 1 -mindepth 1 -type d -exec sh -c '(echo {} && cd {} && git status -s && echo)' \;
```