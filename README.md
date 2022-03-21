# git-substatus

<!-- badges: start -->
[![CI status](https://github.com/strboul/git-substatus/workflows/CI/badge.svg)](https://github.com/strboul/git-substatus/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-success)](https://github.com/strboul/git-substatus/blob/master/.pre-commit-config.yaml)
[![PyPI version](https://img.shields.io/pypi/v/git-substatus?color=%230073b7&label=pypi)](https://pypi.org/project/git-substatus/)
[![hub.docker.com](https://img.shields.io/docker/v/strboul/git-substatus?color=%230db7ed&label=docker)](https://hub.docker.com/r/strboul/git-substatus)
<!-- badges: end -->

A command-line tool to inspect the status of git repositories from a directory,
like a projects folder keeping the git projects. You can therefore view:

+ status

    - added, removed, modified, renamed

    - merge conflicts

    - *etc.*

+ stash

+ [worktree](https://git-scm.com/docs/git-worktree)

## Usage

<img src="https://user-images.githubusercontent.com/25015317/97109790-8cbd6680-16d5-11eb-9c2e-b1626368ba62.gif" align="center" height="145"/>

See more at `git-substatus --help`

<!-- help-output: start -->
```
usage: git-substatus [-h] [-v] [--include-hidden] [--fetch] [path]

See subfolders' git status
===========================

The output consists of four columns:

repo name | branch head | status | git stashes (if any)

The string (*WT) seen next to the repo names shows that the
repo has some git worktrees. See more:
<https://git-scm.com/docs/git-worktree>

positional arguments:
  path              a path to where you want to see git substatuses. If empty, the
                    current working directory is selected.

optional arguments:
  -h, --help        show this help message and exit
  -v, --version     show program's version number and exit
  --include-hidden  repositories starting with a dot (.) are included.
  --fetch           perform git fetch from remote on all sub repositories.
```
<!-- help-output: end -->

## Installation

Install from the [PyPI](https://pypi.org/project/git-substatus/):

```bash
pip install git-substatus
```

Install from the repo:

```bash
pip install git+https://github.com/strboul/git-substatus.git
```

* * *

Alternatively, the [Docker](https://hub.docker.com/r/strboul/git-substatus)
image can be used:

```bash
docker run --rm -t -v "$(pwd)":/"$(pwd)" -w "$(pwd)" strboul/git-substatus:latest
```

To shorten the command, it's also possible to add an alias in the `.bashrc` or
`.zshrc`, e.g.:

```bash
_git_substatus() {
  docker run --rm -t -v "$(pwd)":/"$(pwd)" -w "$(pwd)" strboul/git-substatus:latest "$@"
}
alias git-substatus="_git_substatus"
```

Benchmark: it's measured that the container solution is ~70% slower than the
native operation due to the overhead; however, the container solution is still
useful for portability matters.

## Development

This tool has **no module dependency** outside
[The Python Standard Library](https://docs.python.org/3/library/index.html).

<details>

<summary>Development docs</summary>

### Versioning and release

1. Bump up the `__version__` in `git_substatus/__init__.py` and commit the
   change in the batch where you changed the files.

2. (For the codeowner) Create a version tag with `make tag-create` number. Push
   the tag to the origin with `make tag-push`. Upon the push, the release
   workflow will be triggered that distributes the new version to the
   platforms, like *PyPI*, *DockerHub*.

### pre-commit

Run pre-commit git hooks on every commit that run checks against the files
added to a commit.

Upon cloning the repo, set up `pre-commit`:
- Install pre-commit https://pre-commit.com/#installation
- Run `pre-commit install` that installs the hook scripts at `.git/hooks`

### Add tests

+ Write/update unit tests (if relevant). You can start by adding/modifying a
  case to generator file `tests/gen_test_repos.sh`.

### Run tests && debugging

```bash
virtualenv venv
source venv/bin/activate # deactivate
pip install -r dev-requirements.txt # pip freeze > dev-requirements.txt
make all
```

Put a `breakpoint()` at a relevant place and run:

```bash
make test
```

### Add new methods

+ Use the reference to name the functions/methods in the module:
https://mirrors.edge.kernel.org/pub/software/scm/git/docs/gitglossary.html

</details>
