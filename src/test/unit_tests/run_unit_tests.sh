#!/bin/bash

CODE_DIR="../../main/code"
TEST_FILES="unit_tests.py"

coverage run --source="$CODE_DIR" -m pytest -v "$TEST_FILES" && coverage report -m
