#! /usr/bin/env bash

function roofAI() {
    local task=$(abcli_unpack_keyword $1 version)

    abcli_generic_task \
        plugin=roofAI,task=$task \
        "${@:2}"
}

abcli_source_caller_suffix_path /tests
