# git-substatus

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

### Run tests

```bash
virtualenv venv
source venv/bin/activate
pip install -r dev-requirements.txt
make all
```

### Add new methods

+ Use the reference to name the functions/methods in the module:
https://mirrors.edge.kernel.org/pub/software/scm/git/docs/gitglossary.html

+ Run `black git_substatus` https://github.com/psf/black but be careful as it
overwrites the files, so do it when you have a clean git status.

</details>
