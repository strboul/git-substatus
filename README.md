# git-substatus

A small script to find the git status in subdirectories 
(e.g. in a *common project folder*) where I'd like to see what changes has been done in the states of:

+ changed
+ unpushed
+ unmerged
+ merge conflicts

<p align="center"><img src="media/sample.gif"/></p>

## Usage

```bash
git-substatus projects-folder
```

Go to help with `git-substatus -h`.
<!-- try to keep the help output up to date -->
```
usage: git-substatus.py [-h] [--fetch] [--dont-ignore-hidden] [path]

See subfolders' git status

positional arguments:
  path                  path indicating where you want to see substatuses. If
                        left empty, current working directory will be chosen.

optional arguments:
  -h, --help            show this help message and exit
  --fetch               git fetch from remote repositories
  --dont-ignore-hidden  if selected, the directories starting with dot are not
                        ignored
```

## Installation

Place the `git-substatus.py` file into your PATH and set executable permissions:

```bash
curl -L https://raw.githubusercontent.com/strboul/git-substatus/master/git-substatus.py > /usr/local/bin/git-substatus && \
chmod u+x /usr/local/bin/git-substatus
```

Please note that *libgit2* `C` library and *pygit2* `Python` module are required.

## Development

Install requirements:
```bash
pip3 install -r requirements.txt
```

After generating sample test directory with `./tests/generate-test.sh`, 
run the unit tests:
```bash
python3 -m unittest tests/test-git-substatus.py
```

Run manually:
```bash
python3 git-substatus.py tests/test-project-folder
```

