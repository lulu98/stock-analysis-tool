#!/bin/bash

PROJECT_DIR="../../.."

collect_sources () {
    markdown_files=("$PROJECT_DIR/*.md")
}

process () {
    for file in "${markdown_files[@]}"; do
        mdl -r ~MD024 "$file"
    done
}

collect_sources
process
