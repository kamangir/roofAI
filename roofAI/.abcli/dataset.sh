#! /usr/bin/env bash

function roofAI_dataset() {
    local task=$(abcli_unpack_keyword $1 version)

    local function_name=roofAI_dataset_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
        return
    fi

    python3 -m roofAI.dataset "$@"
}

abcli_source_caller_suffix_path /dataset
