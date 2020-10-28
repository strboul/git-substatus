# git-substatus-v2

<!-- badges: start -->
[![CI status](https://github.com/strboul/git-substatus/workflows/CI/badge.svg)](https://github.com/strboul/git-substatus/actions)
[![PyPI version](https://badge.fury.io/py/git-substatus.svg)](https://pypi.org/project/git-substatus/)
<!-- badges: end -->

A command-line tool to inspect the status of git repositories from a directory
(e.g., a common project folder). You can see:

+ status

    - added, removed, modified, renamed

    - merge conflicts

    - *etc.*

+ stash

+ [worktree](https://git-scm.com/docs/git-worktree)


## Usage

<img src="https://user-images.githubusercontent.com/25015317/97109790-8cbd6680-16d5-11eb-9c2e-b1626368ba62.gif" align="center" height="145"/>

See more at `git-substatus --help`

## Installation

```bash
pip install git-substatus
```

This module has no module dependency outside
[The Python Standard Library](https://docs.python.org/3/library/index.html).

## Development

<details>

### Running tests

```bash
virtualenv venv
source venv/bin/activate
pip install -r dev-requirements.txt
make all
```

### To-do

Used the text to name the functions/methods in the package

https://mirrors.edge.kernel.org/pub/software/scm/git/docs/gitglossary.html

+ Remove all "v2" references once everything is done.

+ Once everything is done, add mypy types to every possible "module" call (not
tests) and fortify them.

+ Instead of creating a media/ folder, put the gif into an issue and link to
the readme and close it later.

+ Run black time-to-time https://github.com/psf/black but be careful as it
overwrites the files. Run `black git_substatus` when you have a clean git
status.

+ To fix the coverage: move gitsubstatus.py to __main__.py and see if coverage
works. And then improve test coverage (e.g. some utils missing).

#### Planning

class Worktree (inherits Repository?)
**is_git_worktree https://git-scm.com/docs/git-worktree

**class Worktree (inherits Repository)
**show_worktree

class Stash (inherits Status)

has_stash       there are stashed modifications
num_stash       number of stashed modifications

class Fetch

do_fetch   performs a git fetch.

</details>
