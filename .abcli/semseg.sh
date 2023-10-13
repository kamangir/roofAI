#! /usr/bin/env bash

function semseg() {
    roofAI_semseg "$@"
}

function roofAI_semseg() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ]; then
        local options="~download,dryrun,profile=FULL|QUICK|VALIDATION,~upload"
        abcli_show_usage "semseg predict$ABCUL[$options]$ABCUL<model_object_name>$ABCUL<dataset_object_name>$ABCUL<prediction_object_name>" \
            "semseg[<model_object_name>].predict(<dataset_object_name>) -> <prediction_object_name>."

        if [ "$(abcli_keyword_is $2 verbose)" == true ]; then
            python3 -m roofAI.semseg --help
        fi
        return
    fi

    if [ "$task" == "predict" ]; then
        local options=$2

        local do_dryrun=$(abcli_option_int "$options" dryrun 0)
        local do_download=$(abcli_option_int "$options" download $(abcli_not $du_dryrun))
        local do_upload=$(abcli_option_int "$options" upload $(abcli_not $du_dryrun))

        local model_object_name=$(abcli_clarify_object $3 ...)
        [[ "$do_download" == 1 ]] &&
            abcli_download object $model_object_name

        local dataset_object_name=$(abcli_clarify_object $4 ..)
        [[ "$do_download" == 1 ]] &&
            abcli_download object $dataset_object_name

        local prediction_object_name=$(abcli_clarify_object $5 .)

        abcli_log "semseg[$model_object_name].predict($dataset_object_name) -> $prediction_object_name."

        abcli_eval dryrun=$do_dryrun \
            python3 -m roofAI.semseg predict \
            --model_path $abcli_object_root/$model_object_name \
            --dataset_path $abcli_object_root/$dataset_object_name \
            --prediction_path $abcli_object_root/$prediction_object_name \
            --profile $(abcli_option "$options" profile VALIDATION) \
            "${@:6}"

        if [ "$do_upload" == 1 ]; then
            abcli_upload object $prediction_object_name
        fi

        return
    fi

    abcli_log_error "-semseg: $task: command not found."
}
