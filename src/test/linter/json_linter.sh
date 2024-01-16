#!/bin/bash

status=0

collect_sources () {
    json_files=("../../../src/main/config/stocks.json")
}

process () {
    for file in "${json_files[@]}"; do
        echo "linting $file"
        if ! jsonlint-php "$file"; then
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
