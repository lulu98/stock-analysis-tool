#!/bin/bash

PROJECT_DIR="../../.."
TEST_DIR="$PROJECT_DIR/src/test"
CODE_DIR="$PROJECT_DIR/src/main/code"
status=0

collect_sources () {
    mapfile -t python_files < <( find $TEST_DIR -iname "*.py" )
    mapfile -t -O "${#python_files[@]}" python_files < <( find $CODE_DIR -iname "*.py" )
}
    
for file in "${python_files[@]}"; do
    echo "$file"
done

process_pycodestyle () {
    echo "Linting with pycodestyle."
    for file in "${python_files[@]}"; do
        echo "linting $file"
        if ! pycodestyle --ignore=E501 "$file"; then 
            status=1
        fi
    done
}

process_pylint () {
    echo "Linting with pylint."
    for file in "${python_files[@]}"; do
        echo "linting $file"
        if ! pylint "$file"; then
            status=1
        fi
    done
}

process_pyflakes() {
    echo "Linting with pyflakes."
    for file in "${python_files[@]}"; do
        echo "linting $file"
        if ! pyflakes "$file"; then
            status=1
        fi
    done
}

process_mccabe() {
    echo "Linting with mccabe."
    for file in "${python_files[@]}"; do
        echo "linting $file"
        if ! python3 -m mccabe --min 10 "$file"; then
            status=1
        fi
    done
}

collect_sources
process_pycodestyle
#process_pylint
#process_pyflakes
process_mccabe
if [ $status -eq 0 ]; then
    echo "$0 success"
else
    echo "$0 failure"
fi
exit $status
