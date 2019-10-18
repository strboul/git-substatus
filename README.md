# git-substatus

A small script to find the git status in subdirectories 
(e.g. in a *common project folder*) where I'd like to see what changes has been done in the states of:

+ changed
+ unpushed
+ unmerged
+ merge conflicts

## Usage

```bash
git-substatus projects-folder
```

Go to help with `git-substatus -h`.

## Installation

Place the `git-substatus.py` file into your PATH and set executable permissions:

```bash
curl -L https://raw.githubusercontent.com/strboul/git-substatus/master/git-substatus.py > /usr/local/bin/git-substatus && \
chmod u+x /usr/local/bin/git-substatus
```

## Development

Install requirements:
```bash
pip3 install -r requirements.txt
```

Run tests:
```bash
python3 -m unittest tests/test-main.py
```

or (after generating test files with `./generate-test.sh`)

```bash
python3 git-substatus.py tests/test-project-folder
```

