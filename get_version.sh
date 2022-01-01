#!/usr/bin/env bash

variable="$1"
sed -n "s/$variable = *\"\([^ ]*\)\"/\1/p" git_substatus/__init__.py
