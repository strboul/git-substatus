# git-substatus

A small script to find the git status in subdirectories 
(e.g., in a *common project folder*), where I'd like to see what changes have been done in the states of:

+ added, removed, modified, renamed
+ unpushed, unmerged
+ merge conflicts

## Installation

Put the `git-substatus.py` file into one of locations in your `PATH` and set executable permissions:

```bash
curl -L https://raw.githubusercontent.com/strboul/git-substatus/master/git-substatus.py > /usr/local/bin/git-substatus && \
chmod u+x /usr/local/bin/git-substatus
```

Please note that *libgit2* `C` library and *pygit2* `Python` module are required.

## Usage

<img src="media/sample.gif" align="center" height="145"/>

See more at `git-substatus --help`

## Development

```bash
## Install requirements:
pip3 install -r requirements.txt
## After generating sample test directory with `./tests/generate-test.sh`, 
## run the unit tests:
python3 tests/test-git-substatus.py
## Run the sample test directory manually:
python3 git-substatus.py tests/test-project-folder
```
