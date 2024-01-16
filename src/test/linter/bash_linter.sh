#!/bin/bash

PROJECT_DIR="../../.."
status=0

collect_sources () {
    mapfile -t bash_files < <( find $PROJECT_DIR -iname "*.sh" )
}

process () {
    for file in "${bash_files[@]}"; do
        echo "linting $file"
        if ! shellcheck "$file"; then
            status=1
        fi
    done
}

collect_sources
process
if [ $status -eq 0 ]; then
    echo "$0 success"
else
    echo "$0 failure"
fi
exit $status
