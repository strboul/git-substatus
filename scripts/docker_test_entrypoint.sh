#!/bin/sh
wget https://raw.githubusercontent.com/strboul/git-substatus/master/scripts/generate_test_repos.sh &&\
  chmod +x generate_test_repos.sh &&\
  ./generate_test_repos.sh &&\
  cd tests/generated-test-proj-dir &&\
  git-substatus
