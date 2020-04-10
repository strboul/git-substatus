#!/usr/bin/env bash
# The script creates dummy project folders, which each of them can represent a
# different test case, that are all the possible situations that can be
# encountered during the use of git-substatus.
#
# Dev notes:
# + According to the ShellCheck (SC2164), the `cd` calls are covered with `||
# exit` in case that changing directory fails.
#
# https://github.com/koalaman/shellcheck
#
INITIAL_WD="$(PWD)"
TESTS_FOLDER="test-project-folder"
TESTS_DIR="tests"
TESTS_DIR_FOLDER_PATH="$TESTS_DIR"/"$TESTS_FOLDER"
if [ -d "$TESTS_DIR_FOLDER_PATH" ]; then
  rm -rf "${TESTS_DIR_FOLDER_PATH:?}"
fi
mkdir -p "$TESTS_DIR_FOLDER_PATH" && cd "$TESTS_DIR_FOLDER_PATH" || exit
set_git_config_local() {
  git config --local user.email "$1"
  git config --local user.name "$2"
}
# --------------------------------------------------------
# projA
# scenario:
# local files changed
# structure:
# 1 local repo
# outcome:
# 2 files changed, 1 file added, 1 file removed
# --------------------------------------------------------
mkdir -p projA && cd projA || exit
touch fruits.txt vegetables.txt dairy.txt
echo "apple, orange, banana" > fruits.txt
echo "broccoli, avocado" > vegetables.txt
git init && set_git_config_local "you@example.com" "Test User"
git add -A && git commit -m 'Initial commit'
echo "watermelon" >> fruits.txt
echo "spinach, lettuce" > vegetables.txt
touch drinks.txt
rm dairy.txt
cd ..
# --------------------------------------------------------
# projB
# scenario:
# showing changes between local and remote
# structure:
# 1 remote repo
# 2 local repos having different changes
# outcome:
# -- before fetch --
# 1 local commit
# -- after fetch --
# 1 local commit, 1 commit fetched from remote that
# they are different (no conflicts)
# --------------------------------------------------------
# create a 'local' directory for the remote:
mkdir -p .projB-remote && cd .projB-remote || exit
# bare init because it's remote
git init --bare
PROJB_REMOTE_ABS_PATH="$PWD"
cd ..
# first, a developer make change:
git clone "$PROJB_REMOTE_ABS_PATH" projB && cd projB || exit
set_git_config_local "you@example.com" "Test User"
touch change.txt
git add -A && git commit -m 'Initial commit'
git push origin master
cd ..
# second user clones remote repo with the changes:
git clone "$PROJB_REMOTE_ABS_PATH" .projB-user1 && cd .projB-user1 || exit
set_git_config_local "you@example.com" "Test User"
touch new-work.txt
git add -A && git commit -m 'New work'
git push origin master && cd ../projB || exit
# go back to the first user, make a commit:
touch work.txt
git add -A && git commit -m 'Work'
cd ..
# --------------------------------------------------------
# projC
# scenario:
# merge conflict
# structure:
# 1 local repo and 1 branch apart from master
# outcome:
# a merge conflict occurred
# --------------------------------------------------------
mkdir -p projC && cd projC || exit
touch code.py && echo "print('Hello, world!')" > code.py
git init && set_git_config_local "you@example.com" "Test User"
git add -A && git commit -m 'Implement code'
git checkout -b new-branch
echo "print('Hi there')" > code.py
git add -A && git commit -m 'Change to hi'
git checkout master
echo "print('The quick brown fox jumps over the lazy dog')" > code.py
git add -A && git commit -m 'Change to the quick brown fox'
git merge new-branch
cd ..
# --------------------------------------------------------
# projD
# scenario:
# in a different branch than master but did not commit at all
# --------------------------------------------------------
mkdir -p projD && cd projD || exit
git init && set_git_config_local "you@example.com" "Test User"
git checkout -b new-branch
touch file.txt
cd ..
# --------------------------------------------------------
# projE
# scenario:
# in a different branch than master and at least one commit done
# --------------------------------------------------------
mkdir -p projE && cd projE || exit
git init && set_git_config_local "you@example.com" "Test User"
git checkout -b new-model-branch
touch file.txt
git add -A && git commit -m 'Add file'
cd ..
# --------------------------------------------------------
# Adding some extra non-git
# folders (having no `.git` directory in it):
mkdir -p proj-no-git1 proj-no-git2
# get back to the initial working directory
cd "$INITIAL_WD" || exit
echo "*====================*"
echo "*==== Completed ====*"
echo "*====================*"
