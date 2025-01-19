#! /usr/bin/env bash

function roofai_semseg_train() {
    local options=$1
    $abcli_gpu_status_cache && local device=cuda || local device=cpu
    local device=$(abcli_option "$options" device $device)
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_download=$(abcli_option_int "$options" download $(abcli_not $do_dryrun))
    local do_upload=$(abcli_option_int "$options" upload $(abcli_not $do_dryrun))

    local dataset_object_name=$(abcli_clarify_object $2 .)
    [[ "$do_download" == 1 ]] &&
        abcli_download - $dataset_object_name

    local model_object_name=$(abcli_clarify_object $3 $dataset_object_name-model-$(abcli_string_timestamp_short))

    abcli_log "semseg.train($dataset_object_name) -$device-> $model_object_name."

    abcli_eval dryrun=$do_dryrun \
        python3 -m roofai.semseg train \
        --device $device \
        --dataset_path $ABCLI_OBJECT_ROOT/$dataset_object_name \
        --model_path $ABCLI_OBJECT_ROOT/$model_object_name \
        --profile $(abcli_option "$options" profile VALIDATION) \
        "${@:4}"
    local status="$?"

    [[ "$do_upload" == 1 ]] &&
        abcli_upload - $model_object_name

    return $status
}
