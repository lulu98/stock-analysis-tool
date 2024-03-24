#!/bin/bash

CODE_DIR="../../main/code"
MIN_COVERAGE=90

coverage run --source="$CODE_DIR" --omit="$CODE_DIR/stage01.py,$CODE_DIR/stage02.py,$CODE_DIR/web_api.py" -m pytest -vv tests/* && coverage report -m --fail-under=$MIN_COVERAGE
