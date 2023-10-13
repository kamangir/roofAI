#! /usr/bin/env bash

function semseg() {
    roofAI_semseg "$@"
}

function roofAI_semseg() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ]; then
        local options="dryrun,profile=FULL,QUICK,VALIDATION"
        abcli_show_usage "semseg predict$ABCUL[$options]$ABCUL<dataset_object_name>$ABCUL<model_object_name>$ABCUL<prediction_object_name>" \
            "semseg[<model_object_name>].predict(<dataset_object_name>) -> <prediction_object_name>."
        return
    fi

    if [ "$task" == "predict" ]; then
        echo "wip"
        return
    fi

    abcli_log_error "-semseg: $task: command not found."
}
