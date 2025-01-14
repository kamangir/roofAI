#! /usr/bin/env bash

function test_roofAI_help() {
    local options=$1

    local module
    for module in \
        "roofAI dataset" \
        "roofAI dataset ingest" \
        "roofAI dataset review" \
        \
        "roofAI semseg" \
        "roofAI semseg predict" \
        "roofAI semseg train" \
        \
        "roofAI"; do
        abcli_eval ,$options \
            abcli_help $module
        [[ $? -ne 0 ]] && return 1

        abcli_hr
    done

    return 0
}
