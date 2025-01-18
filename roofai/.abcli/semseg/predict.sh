#! /usr/bin/env bash

function roofAI_semseg_predict() {
    local options=$1
    $abcli_gpu_status_cache && local device=cuda || local device=cpu
    local device=$(abcli_option "$options" device $device)
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_download=$(abcli_option_int "$options" download $(abcli_not $do_dryrun))
    local do_upload=$(abcli_option_int "$options" upload $(abcli_not $do_dryrun))

    local model_object_name=$(abcli_clarify_object $2 ..)
    [[ "$do_download" == 1 ]] &&
        abcli_download - $model_object_name

    local dataset_object_name=$(abcli_clarify_object $3 .)
    [[ "$do_download" == 1 ]] &&
        abcli_download - $dataset_object_name

    local prediction_object_name=$(abcli_clarify_object $4 $dataset_object_name-prediction-$(abcli_string_timestamp_short))

    abcli_log "semseg[$model_object_name].predict($dataset_object_name) -$device-> $prediction_object_name."

    abcli_eval dryrun=$do_dryrun \
        python3 -m roofAI.semseg predict \
        --device $device \
        --model_path $ABCLI_OBJECT_ROOT/$model_object_name \
        --dataset_path $ABCLI_OBJECT_ROOT/$dataset_object_name \
        --prediction_path $ABCLI_OBJECT_ROOT/$prediction_object_name \
        --profile $(abcli_option "$options" profile VALIDATION) \
        "${@:5}"
    local status="$?"

    [[ "$do_upload" == 1 ]] &&
        abcli_upload - $prediction_object_name

    return $status
}
