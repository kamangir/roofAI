#! /usr/bin/env bash

function semseg() {
    roofAI_semseg "$@"
}

function roofAI_semseg() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ]; then
        roofAI_semseg predict "$@"
        roofAI_semseg train "$@"

        [[ "$(abcli_keyword_is $2 verbose)" == true ]] &&
            python3 -m roofAI.semseg --help

        return
    fi

    local options=$2

    local device=$(abcli_option "$options" device cpu)
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_download=$(abcli_option_int "$options" download $(abcli_not $do_dryrun))
    local do_register=$(abcli_option_int "$options" register 0)
    local do_upload=$(abcli_option_int "$options" upload $do_register)

    if [ "$task" == "predict" ]; then
        if [ $(abcli_option_int "$options" help 0) == 1 ]; then
            local options="device=cpu|cuda,~download,dryrun,profile=FULL|QUICK|VALIDATION,upload"
            abcli_show_usage "semseg predict$ABCUL[$options]$ABCUL<model_object_name>$ABCUL<dataset_object_name>$ABCUL<prediction_object_name>" \
                "semseg[<model_object_name>].predict(<dataset_object_name>) -> <prediction_object_name>."
            return
        fi

        local model_object_name=$(abcli_clarify_object $3 ...)
        [[ "$do_download" == 1 ]] &&
            abcli_download object $model_object_name

        local dataset_object_name=$(abcli_clarify_object $4 ..)
        [[ "$do_download" == 1 ]] &&
            abcli_download object $dataset_object_name

        local prediction_object_name=$(abcli_clarify_object $5 .)

        abcli_log "semseg[$model_object_name].predict($dataset_object_name) -$device-> $prediction_object_name."

        local prediction_object_path=$abcli_object_root/$prediction_object_name
        mkdir -pv $prediction_object_path

        abcli_eval dryrun=$do_dryrun \
            python3 -m roofAI.semseg predict \
            --device $device \
            --model_path $abcli_object_root/$model_object_name \
            --dataset_path $abcli_object_root/$dataset_object_name \
            --prediction_path $prediction_object_path \
            --profile $(abcli_option "$options" profile VALIDATION) \
            "${@:6}"

        [[ "$do_upload" == 1 ]] &&
            abcli_upload object $prediction_object_name

        return
    fi

    if [ "$task" == "train" ]; then
        if [ $(abcli_option_int "$options" help 0) == 1 ]; then
            local options="device=cpu|cuda,~download,dryrun,profile=FULL|QUICK|VALIDATION,register,suffix=<v1>,upload"
            local args="[--activation <sigmoid>]$ABCUL[--classes <one+two+three+four>]$ABCUL[--encoder_name <se_resnext50_32x4d>]$ABCUL[--encoder_weights <imagenet>]"
            abcli_show_usage "semseg train$ABCUL[$options]$ABCUL<dataset_object_name>$ABCUL<model_object_name>$ABCUL$args" \
                "semseg.train(<dataset_object_name>) -> <model_object_name>."
            return
        fi

        local dataset_object_name=$(abcli_clarify_object $3 ..)
        [[ "$do_download" == 1 ]] &&
            abcli_download object $dataset_object_name

        local model_object_name=$(abcli_clarify_object $4 .)

        abcli_log "semseg.train($dataset_object_name) -$device-> $model_object_name."

        abcli_eval dryrun=$do_dryrun \
            python3 -m roofAI.semseg train \
            --device $device \
            --dataset_path $abcli_object_root/$dataset_object_name \
            --model_path $abcli_object_root/$model_object_name \
            --profile $(abcli_option "$options" profile VALIDATION) \
            --register $do_register \
            --suffix $(abcli_option "$options" suffix v1) \
            "${@:5}"

        [[ "$do_upload" == 1 ]] &&
            abcli_upload object $model_object_name

        return
    fi

    abcli_log_error "-semseg: $task: command not found."
}
