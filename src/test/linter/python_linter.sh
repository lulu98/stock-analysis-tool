#!/bin/bash

PROJECT_DIR="../../.."
TEST_DIR="$PROJECT_DIR/src/test"
CODE_DIR="$PROJECT_DIR/src/main/code"

PYTHON_FILES=($(find $TEST_DIR -iname "*.py") $(find $CODE_DIR -iname "*.py"))

process_pycodestyle () {
    for file in "${PYTHON_FILES[@]}"; do
        pycodestyle "$file"
    done
}

process_pylint () {
    for file in "${PYTHON_FILES[@]}"; do
        pylint "$file"
    done
}

process_pyflakes() {
    for file in "${PYTHON_FILES[@]}"; do
        pyflakes "$file"
    done
}

process_mccabe() {
    for file in "${PYTHON_FILES[@]}"; do
        echo "$file"
        python3 -m mccabe --min 10 "$file"
    done
}

process_pycodestyle
process_pylint
process_pyflakes
process_mccabe
