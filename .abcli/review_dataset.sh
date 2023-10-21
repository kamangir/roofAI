#! /usr/bin/env bash

function roofAI_review_dataset() {
    local options=${1:-help}

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        local options="download,dryrun"
        local args="[--count <1>]$ABCUL[--index <index>]$ABCUL[--subset <subset>]"
        abcli_show_usage "roofAI review_dataset$ABCUL[$options]$ABCUL<dataset_object_name>$ABCUL$args" \
            "review <dataset_object_name>."
        return
    fi

    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_download=$(abcli_option_int "$options" download 0)

    local dataset_object_name=$(abcli_clarify_object $2 .)
    [[ "$do_download" == 1 ]] &&
        abcli_download object $dataset_object_name

    abcli_eval dryrun=$do_dryrun \
        python3 -m roofAI.dataset review \
        --dataset_path $abcli_object_root/$dataset_object_name \
        "${@:3}"
}
