CODE_DIR="../../main"
CONFIG_DIR="$CODE_DIR/config"

collect_sources () {
    json_files=($CONFIG_DIR/stocks.json)
}

process () {
    for file in "${json_files[@]}"; do
        jsonlint-php $file
    done
}

collect_sources 
process
