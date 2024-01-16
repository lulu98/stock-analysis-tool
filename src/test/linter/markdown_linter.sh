#!/bin/bash

PROJECT_DIR="../../.."
status=0

collect_sources () {
    mapfile -t markdown_files < <( find $PROJECT_DIR -iname "*.md" )
}

process () {
    for file in "${markdown_files[@]}"; do
        echo "linting $file"
        # ignore 'MD024 Multiple headers with the same content' because it's
        # needed for the changelog
        if ! mdl -r ~MD024 "$file"; then
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
