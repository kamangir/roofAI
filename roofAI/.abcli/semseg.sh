#! /usr/bin/env bash

export semseg_profiles="FULL|DECENT|QUICK|DEBUG|VALIDATION"

function roofAI_semseg() {
    local task=$(abcli_unpack_keyword $1 help)

    local options=$2
    $abcli_gpu_status_cache && local device=cuda || local device=cpu
    local device=$(abcli_option "$options" device $device)
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_download=$(abcli_option_int "$options" download $(abcli_not $do_dryrun))
    local do_upload=$(abcli_option_int "$options" upload $(abcli_not $do_dryrun))

    if [ "$task" == "predict" ]; then
        if [ $(abcli_option_int "$options" help 0) == 1 ]; then
            local options="device=cpu|cuda,~download,dryrun,profile=$semseg_profiles,upload"
            abcli_show_usage "semseg predict$ABCUL[$options]$ABCUL[...|<model-object-name>]$ABCUL[..|<dataset-object-name>]$ABCUL[-|<prediction-object-name>]" \
                "semseg[<model-object-name>].predict(<dataset-object-name>) -> <prediction-object-name>."
            return
        fi

        local model_object_name=$(abcli_clarify_object $3 ...)
        [[ "$do_download" == 1 ]] &&
            abcli_download - $model_object_name

        local dataset_object_name=$(abcli_clarify_object $4 ..)
        [[ "$do_download" == 1 ]] &&
            abcli_download - $dataset_object_name

        local prediction_object_name=$(abcli_clarify_object $5 $(abcli_string_timestamp))

        abcli_log "semseg[$model_object_name].predict($dataset_object_name) -$device-> $prediction_object_name."

        abcli_eval dryrun=$do_dryrun \
            python3 -m roofAI.semseg predict \
            --device $device \
            --model_path $ABCLI_OBJECT_ROOT/$model_object_name \
            --dataset_path $ABCLI_OBJECT_ROOT/$dataset_object_name \
            --prediction_path $ABCLI_OBJECT_ROOT/$prediction_object_name \
            --profile $(abcli_option "$options" profile VALIDATION) \
            "${@:6}"
        local status="$?"

        [[ "$do_upload" == 1 ]] &&
            abcli_upload - $prediction_object_name

        return $status
    fi

    if [ "$task" == "train" ]; then
        if [ $(abcli_option_int "$options" help 0) == 1 ]; then
            local options="device=cpu|cuda,~download,dryrun,profile=$semseg_profiles,upload"
            local args="[--activation <sigmoid>]$ABCUL[--classes <one+two+three+four>]$ABCUL[--encoder_name <se_resnext50_32x4d>]$ABCUL[--encoder_weights <imagenet>]"
            abcli_show_usage "semseg train$ABCUL[$options]$ABCUL<dataset-object-name>$ABCUL<model-object-name>$ABCUL$args" \
                "semseg.train(<dataset-object-name>) -> <model-object-name>."
            return
        fi

        local dataset_object_name=$(abcli_clarify_object $3 ..)
        [[ "$do_download" == 1 ]] &&
            abcli_download - $dataset_object_name

        local model_object_name=$(abcli_clarify_object $4 .)

        abcli_log "semseg.train($dataset_object_name) -$device-> $model_object_name."

        abcli_eval dryrun=$do_dryrun \
            python3 -m roofAI.semseg train \
            --device $device \
            --dataset_path $ABCLI_OBJECT_ROOT/$dataset_object_name \
            --model_path $ABCLI_OBJECT_ROOT/$model_object_name \
            --profile $(abcli_option "$options" profile VALIDATION) \
            "${@:5}"
        local status="$?"

        [[ "$do_upload" == 1 ]] &&
            abcli_upload - $model_object_name

        return $status
    fi

    abcli_log_error "semseg: $task: command not found."
    return 1
}
