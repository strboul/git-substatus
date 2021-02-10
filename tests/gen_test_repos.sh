#!/usr/bin/env bash
# This script creates dummy git repositories, which each of them can represent
# a different test case. It is meant to be called from the unit tests but it
# can also be called independently.
INITIAL_WD="$(pwd)"
TESTS_FOLDER="generated-test-proj-dir"
TESTS_DIR="tests"
TESTS_DIR_FOLDER_PATH="$TESTS_DIR"/"$TESTS_FOLDER"
if [ -d "$TESTS_DIR_FOLDER_PATH" ]; then
  rm -rf "${TESTS_DIR_FOLDER_PATH:?}"
fi
mkdir -p "$TESTS_DIR_FOLDER_PATH" && cd "$TESTS_DIR_FOLDER_PATH" || exit
set_local_git_config() {
  git config --local user.email "test@example.com"
  git config --local user.name "git-substatus Test User"
}

# Adding some extra folders (not a git repository) and files
mkdir -p proj-no-git1 .proj-no-git2
touch file1 .file2

# projA - some local files are changed
# structure:
# 1 local repo
# status:
# 2 files modified, 1 file untracked, 1 file deleted
# --------------------------------------------------------
mkdir -p projA && cd projA || exit
touch fruits.txt vegetables.txt dairy.txt
echo "apple, orange, banana" > fruits.txt
echo "broccoli, avocado" > vegetables.txt
git init && set_local_git_config
git add -A && git commit -m "Initial commit"
echo "watermelon" >> fruits.txt
echo "spinach, lettuce" > vegetables.txt
git add vegetables.txt
echo "carrot" >> vegetables.txt
touch drinks.txt
rm dairy.txt
cd .. || exit

# projB - showing changes between local and remote
# structure:
# 1 remote repo
# 2 local repos with different changes
# status:
# -- before fetch --
# 1 local commit
# -- after fetch --
# 2 local commits, 1 commit from remote. 1 untracked. No conflicts.
# --------------------------------------------------------
# create a 'local' directory for the remote:
mkdir -p .projB-remote && cd .projB-remote || exit
# bare init because it's remote
git init --bare && set_local_git_config
PROJB_REMOTE_ABS_PATH="$PWD"
cd .. || exit
# first, a developer make change:
git clone "$PROJB_REMOTE_ABS_PATH" projB && cd projB || exit
set_local_git_config
touch change.txt
git add -A && git commit -m "Initial commit"
git push origin master
cd .. || exit
# second user clones remote repo with the changes:
git clone "$PROJB_REMOTE_ABS_PATH" .projB-user1 && cd .projB-user1 || exit
set_local_git_config
touch new-work.txt
git add -A && git commit -m "New work"
git push origin master && cd ../projB || exit
# go back to the first user, make commits:
touch work.txt && git add -A && git commit -m "Work"
touch work2.txt && git add -A && git commit -m "Work2"
touch work3.txt
git fetch
cd .. || exit

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
git init && set_local_git_config
git add -A && git commit -m "Implement code"
git checkout -b new-branch
echo "print('Hi there')" > code.py
git add -A && git commit -m "Change to hi"
git checkout master
echo "print('The quick brown fox jumps over the lazy dog')" > code.py
git add -A && git commit -m "Change to the quick brown fox"
git merge new-branch
cd .. || exit

# projD
# scenario:
# in a different branch than master but did not commit at all
# --------------------------------------------------------
mkdir -p projD && cd projD || exit
git init && set_local_git_config
git checkout -b new-branch
touch file.txt
cd .. || exit

# projE
# scenario:
# in a different branch than master and at least one commit done
# --------------------------------------------------------
mkdir -p projE && cd projE || exit
git init && set_local_git_config
touch file.txt
git add -A && git commit -m "Initial commit"
git checkout -b branchie
touch file2.txt
git add -A && git commit -m "Add file"
cd .. || exit

# projE-worktree
# this proj is a worktree of projE
# scenario:
# TODO
# --------------------------------------------------------
cd projE || exit
git worktree add ../projE-worktree master
cd .. || exit

# projF
# scenario:
# one renamed, one moved | 2 stashes
mkdir -p projF && cd projF || exit
git init && set_local_git_config
touch apple avocado
git add -A && git commit -m "Add files"
echo "text1" >> apple && echo "text1" >> avocado && git stash
echo "text2" >> apple && echo "text2" >> avocado && git stash
git rm apple
mkdir -p subdir
git mv avocado subdir/mango
cd .. || exit

# get back to the initial working directory
cd "$INITIAL_WD" || exit
