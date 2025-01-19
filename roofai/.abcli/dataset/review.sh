#! /usr/bin/env bash

function roofai_dataset_review() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_download=$(abcli_option_int "$options" download 0)

    local dataset_object_name=$(abcli_clarify_object $2 .)
    [[ "$do_download" == 1 ]] &&
        abcli_download - $dataset_object_name

    local dataset_object_path=$ABCLI_OBJECT_ROOT/$dataset_object_name

    abcli_eval dryrun=$do_dryrun \
        python3 -m roofai.dataset review \
        --dataset_path $dataset_object_path \
        "${@:3}"
}
