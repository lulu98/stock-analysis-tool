#!/bin/bash

CODE_DIR="../../main"
LATEX_DIR="$CODE_DIR/resources/template"

collect_sources () {
    latex_files=("$LATEX_DIR/chapters/*")
}

execute_lacheck () {
    for file in "${latex_files[@]}"; do
        lacheck "$file"
    done
}

execute_chktex () {
    for file in "${latex_files[@]}"; do
        chktex -q -n 8 -n 44 "$file"
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
