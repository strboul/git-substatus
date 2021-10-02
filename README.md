# git-substatus

<!-- badges: start -->
[![CI status](https://github.com/strboul/git-substatus/workflows/CI/badge.svg)](https://github.com/strboul/git-substatus/actions)
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
docker run --rm -t -v "$(pwd)":/"$(pwd)" -w "$(pwd)" strboul/git-substatus:latest <optional-path>
```

To shorten the command, it's also possible to add an alias in the `.bashrc` or
`.zshrc`, e.g.:

```bash
_git_substatus() {
  docker run --rm -t -v "$(pwd)":/"$(pwd)" -w "$(pwd)" strboul/git-substatus:latest "$@"
}
alias git-substatus="_git_substatus"
```

Benchmark: I measured that the container solution is about 70% slower than the
native operation, most likely due to the overhead; however, the container is
still useful when portability matters.

## Development

This module has no module dependency outside
[The Python Standard Library](https://docs.python.org/3/library/index.html).

<details>

<summary>Development docs</summary>

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

### Sending a PR

+ Bump up the version - `major.minor.path` (depends on the change) Change the
  version in the file `git_substatus/__init__.py`.

+ Write/update unit tests (where relevant). You can start by adding/modifying a
  case to generator file `tests/gen_test_repos.sh`.

### Release

*(needs credentials)*

+ Release to PyPi

```bash
make release-pypi
```

+ Release to Docker Hub

```bash
make docker-build
make docker-release
```

</details>
