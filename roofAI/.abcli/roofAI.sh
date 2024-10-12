#! /usr/bin/env bash

function roofAI() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ]; then
        roofAI_cloudwatch "$@"
        roofAI_conda "$@"
        roofAI_inference "$@"
        roofAI_semseg "$@"
        roofAI dataset "$@"
        return
    fi

    if [ "$task" == "dataset" ]; then
        local task=$2

        if [ "$task" == "help" ]; then
            roofAI_dataset_ingest "${@:2}"
            roofAI_dataset_review "${@:2}"
            return
        fi

        local function_name=roofAI_dataset_$task
        if [[ $(type -t $function_name) == "function" ]]; then
            $function_name "${@:3}"
            return
        fi

        python3 -m roofAI.dataset "${@:2}"

        return
    fi

    if [[ "|ingest|review|" == *"|$task|"* ]]; then
        roofAI_dataset_${task} "${@:2}"
        return
    fi
    if [[ "|predict|train|" == *"|$task|"* ]]; then
        roofAI_semseg $task "${@:2}"
        return
    fi

    if [ "$task" == "init" ]; then
        local options=$2

        abcli_init roofAI "${@:2}"

        abcli_eval - \
            conda activate \
            $(roofAI_conda environment_name $options)
        return
    fi

    if [ "$task" == "pytest" ]; then
        abcli_${task} plugin=roofAI,$2 \
            --ignore=$abcli_path_git/roofAI/notebooks/data/Scripts/ \
            "${@:3}"
        return
    fi

    abcli_generic_task \
        plugin=roofAI,task=$task \
        "${@:2}"
}

abcli_source_caller_suffix_path /tests
