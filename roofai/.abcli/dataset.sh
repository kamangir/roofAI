#! /usr/bin/env bash

function roofai_dataset() {
    local task=$(abcli_unpack_keyword $1 version)

    local function_name=roofai_dataset_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
        return
    fi

    python3 -m roofai.dataset "$@"
}

abcli_source_caller_suffix_path /dataset
