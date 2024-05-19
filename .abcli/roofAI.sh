#! /usr/bin/env bash

function roof() {
    roofAI "$@"
}

function roofAI() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ]; then
        roofAI_cloudwatch "$@"
        roofAI_conda "$@"
        roofAI_inference "$@"
        roofAI_QGIS "$@"
        roofAI_semseg "$@"
        roofAI dataset "$@"

        $(abcli_keyword_is $2 verbose) &&
            python3 -m roofAI --help

        return
    fi

    local function_name=roofAI_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
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

        python3 -m roofAI.dataset \
            "$task" \
            "${@:3}"

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

    if [ "$task" == "pylint" ]; then
        abcli_${task} ignore=roofAI/QGIS,plugin=roofAI,$2 \
            "${@:3}"
        return
    fi

    if [[ "|pypi|" == *"|$task|"* ]]; then
        abcli_${task} "$2" \
            plugin=roofAI,$3 \
            "${@:4}"
        return
    fi

    if [ "$task" == "pytest" ]; then
        abcli_${task} plugin=roofAI,$2 \
            --ignore=$abcli_path_git/roofAI/notebooks/data/Scripts/ \
            "${@:3}"
        return
    fi

    if [ "$task" == "test" ]; then
        abcli_${task} plugin=roofAI,$2 \
            "${@:3}"
        return
    fi

    if [ "$task" == "version" ]; then
        python3 -m roofAI version "${@:2}"
        return
    fi

    python3 -m roofAI \
        "$task" \
        "${@:2}"
}

abcli_source_path \
    $abcli_path_git/roofAI/.abcli/tests
