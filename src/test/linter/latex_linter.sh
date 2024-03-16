#!/bin/bash

CODE_DIR="../../main"
LATEX_DIR="$CODE_DIR/resources/template/latex"
status=0

collect_sources () {
    mapfile -t latex_files < <( find $LATEX_DIR/chapters -iname "*.tex" )
}

execute_lacheck () {
    for file in "${latex_files[@]}"; do
        echo "linting $file"
        if ! lacheck "$file"; then
            status=1
        fi
    done
}

execute_chktex () {
    for file in "${latex_files[@]}"; do
        echo "linting $file"
        if ! chktex -q -n 8 -n 44 "$file"; then
            status=1
        fi
    done
}

process () {
    echo "Execute lacheck"
    execute_lacheck

    echo "Execute chktex"
    execute_chktex
}

collect_sources
process
if [ $status -eq 0 ]; then
    echo "$0 success"
else
    echo "$0 failure"
fi
exit $status
