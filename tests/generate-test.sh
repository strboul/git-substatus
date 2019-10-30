#!/usr/bin/env bash

## the script below creates dummy project folders,
## which each of them can represent a different case,
## that are possible situations which can be encountered 
## during the use of git-substatus.

## create a project folder keeping the individual project folders:
mkdir -p test-project-folder
cd test-project-folder
## --------------------------------------------------------
## projA
## scenario:
## local files changed
## structure:
## 1 local repo
## outcome:
## 2 files changed, 1 file added, 1 file removed
## --------------------------------------------------------
mkdir -p projA
cd projA
touch fruits.txt
touch vegetables.txt
touch dairy.txt
echo "apple, orange, banana" > fruits.txt
echo "broccoli, avocado" > vegetables.txt
git init
git add -A && git commit -m 'Initial commit'
echo "watermelon" >> fruits.txt
echo "spinach, lettuce" > vegetables.txt
touch drinks.txt
rm dairy.txt
cd ..
## --------------------------------------------------------
## projB
## scenario:
## showing changes between local and remote
## structure:
## 1 remote repo
## 2 local repos doing their own development
## outcome:
## 1 local commit, 1 commit fetched from remote that
## they are different (no conflicts)
## --------------------------------------------------------
## create a 'local' directory for the remote:
mkdir -p projB-remote
cd projB-remote
git init --bare ## bare because it's remote
projB_remote_abs_path="$PWD"
cd ..
## first, a developer make change:
git clone "$projB_remote_abs_path" projB
cd projB
touch change.txt
git add -A && git commit -m 'Initial commit'
git push origin master
cd ..
## second user clones remote repo with the changes:
git clone "$projB_remote_abs_path" projB-user1
cd projB-user1
touch new-work.txt
git add -A && git commit -m 'New work'
git push origin master
cd ..
cd projB
## go back to the first user, make a commit and then fetch:
touch work.txt
git add -A && git commit -m 'Work'
git fetch
cd ..
## remove `remote` and `user1` folders of projB to declutter
rm -rf projB-remote projB-user1
## --------------------------------------------------------
## projC
## scenario:
## merge conflict
## structure:
## 1 local repo and 1 branch apart from master
## outcome:
## a merge conflict occurred
## --------------------------------------------------------
mkdir -p projC
cd projC
touch code.py
echo "print('Hello, world!')" > code.py
git init
git add -A && git commit -m 'Implement code'
git checkout -b new-branch
echo "print('Hi there')" > code.py
git add -A && git commit -m 'Change to hi'
git checkout master
echo "print('The quick brown fox jumps over the lazy dog')" > code.py
git add -A && git commit -m 'Change to the quick brown fox'
git merge new-branch
cd ..
## --------------------------------------------------------
## projD
## scenario:
## in a different branch than master but did not commit at all
## --------------------------------------------------------
mkdir -p projD
cd projD
git init
git checkout -b new-branch
touch file.txt
cd ..
## --------------------------------------------------------
## projE
## scenario:
## in a different branch than master and at least one commit done
## --------------------------------------------------------
mkdir -p projE
cd projE
git init
git checkout -b new-model-branch
touch file.txt
git add -A && git commit -m 'Add file'
cd ..
## --------------------------------------------------------
## Adding some extra non-git 
## folders (having no `.git` directory in it):
mkdir -p proj-no-git1
mkdir -p proj-no-git2
printf "\n\n***script PWD (at current level):***: %s\n\n" $PWD
printf " =========\n"
printf " Completed\n"
printf " =========\n\n"
