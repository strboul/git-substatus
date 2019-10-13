# git-substatus

A small Python 3 script to find the git status in subdirectories (e.g. a project/ folder) where I'd like to see what changes I have in the state of uncommitted/unpushed/unmerged.

Usage
```bash
python3 main.py ~/proj_github
```

Install requirements:
```bash
pip install -r requirements.txt
```

A similar, more basic, bash command:
```bash
find . -maxdepth 1 -mindepth 1 -type d -exec sh -c '(echo {} && cd {} && git status -s && echo)' \;
```