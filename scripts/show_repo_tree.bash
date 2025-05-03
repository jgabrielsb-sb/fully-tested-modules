#!/bin/bash

: <<'END_COMMENT'

This script shows the tree of the repository, excluding:
    * __pycache__
    * venv
    * .git
    * .idea
    * .mypy_cache

END_COMMENT

tree -I '__pycache__|venv|\.git|\.idea|\.mypy_cache'