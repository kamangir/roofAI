#! /usr/bin/env bash

export semseg_profiles="FULL|DECENT|QUICK|DEBUG|VALIDATION"

function semseg() {
    roofAI_semseg "$@"
}

function roofAI_semseg() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ]; then
        roofAI_semseg list "$@"
        roofAI_semseg predict "$@"
        roofAI_semseg train "$@"

        [[ "$(abcli_keyword_is $2 verbose)" == true ]] &&
            python3 -m roofAI.semseg --help

        return
    fi

    local options=$2
    $abcli_gpu_status_cache && local device=cuda || local device=cpu
    local device=$(abcli_option "$options" device $device)
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_download=$(abcli_option_int "$options" download $(abcli_not $do_dryrun))
    local do_register=$(abcli_option_int "$options" register 0)
    local do_upload=$(abcli_option_int "$options" upload $do_register)

    if [ "$task" == "list" ]; then
        if [ $(abcli_option_int "$options" help 0) == 1 ]; then
            abcli_show_usage "semseg list" \
                "list registered semseg models."
            return
        fi

        local reference
        for reference in $(abcli_tags search \
            registered_semseg_model \
            --delim space \
            --log 0); do
            abcli_log "⚡️ $reference: $(abcli_cache read $reference)"
        done

        return
    fi

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

        [[ "$do_upload" == 1 ]] &&
            abcli_upload - $prediction_object_name

        return 0
    fi

    if [ "$task" == "train" ]; then
        if [ $(abcli_option_int "$options" help 0) == 1 ]; then
            local options="device=cpu|cuda,~download,dryrun,profile=$semseg_profiles,register,suffix=<v1>,upload"
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
            --register $do_register \
            --suffix $(abcli_option "$options" suffix v1) \
            "${@:5}"

        [[ "$do_upload" == 1 ]] &&
            abcli_upload - $model_object_name

        return 0
    fi

    abcli_log_error "-semseg: $task: command not found."
    return 1
}

function roofAI_semseg_cache() {
    local filename="/root/.cache/torch/hub/checkpoints/se_resnext50_32x4d-a260b3a4.pth"

    [[ -f "$filename" ]] && return

    abcli_eval - \
        curl \
        --insecure \
        -L http://data.lip6.fr/cadene/pretrainedmodels/se_resnext50_32x4d-a260b3a4.pth \
        -o $filename
}

[[ "$abcli_is_sagemaker_system" == false ]] &&
    [[ "$abcli_is_mac" == false ]] &&
    [[ "$abcli_is_github_workflow" == false ]] &&
    roofAI_semseg_cache
