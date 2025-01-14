#! /usr/bin/env bash

function roofAI_semseg() {
    local task=$(abcli_unpack_keyword $1 version)

    local function_name=roofAI_semseg_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
        return
    fi

    python3 -m roofAI.semseg "$@"
}

abcli_source_caller_suffix_path /semseg
