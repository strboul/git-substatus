#!/usr/bin/env bash

# Get the package versions as listed in the init file

variable="$1"
sed -n "s/$variable = *\"\([^ ]*\)\"/\1/p" git_substatus/__init__.py
