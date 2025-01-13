#! /usr/bin/env bash

function roofAI_dataset_review() {
    local options=${1:-help}

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        local options="download,dryrun,open"
        local args="[--count <1>]$ABCUL[--index <index>]$ABCUL[--subset <subset>]"
        abcli_show_usage "roofAI dataset review$ABCUL[$options]$ABCUL<object-name>$ABCUL$args" \
            "review <object-name>."
        return
    fi

    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_download=$(abcli_option_int "$options" download 0)
    local do_open=$(abcli_option_int "$options" open 0)

    local dataset_object_name=$(abcli_clarify_object $2 .)
    [[ "$do_download" == 1 ]] &&
        abcli_download - $dataset_object_name

    local dataset_object_path=$ABCLI_OBJECT_ROOT/$dataset_object_name
    [[ "$do_open" == 1 ]] &&
        open $dataset_object_path

    abcli_eval dryrun=$do_dryrun \
        python3 -m roofAI.dataset review \
        --dataset_path $dataset_object_path \
        "${@:3}"
}
