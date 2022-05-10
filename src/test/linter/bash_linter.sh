#!/bin/bash

PROJECT_DIR="../../.."

collect_sources () {
    IFS=" " read -r -a bash_files <<< "$(find $PROJECT_DIR -iname '*.sh')"
}

process () {
    for file in "${bash_files[@]}"; do
        shellcheck "$file"
    done
}

collect_sources
process
