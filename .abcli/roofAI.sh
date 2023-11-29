#! /usr/bin/env bash

function roof() {
    roofAI "$@"
}

function roofAI() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ]; then
        roofAI version \\n

        roofAI_conda "$@"
        roofAI_QGIS "$@"
        roofAI_semseg "$@"
        roofAI dataset "$@"
        roofAI pytest "$@"
        roofAI_test "$@"

        if [ "$(abcli_keyword_is $2 verbose)" == true ]; then
            python3 -m roofAI --help
        fi
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
        abcli_init roofAI "${@:2}"
        conda activate roofAI
        return
    fi

    if [ "$task" == "pytest" ]; then
        abcli_pytest plugin=roofAI,$2 \
            --ignore=$abcli_path_git/roofAI/notebooks/data/Scripts/ \
            "${@:3}"
        return
    fi

    if [ "$task" == "version" ]; then
        abcli_log "🏛️  $(python3 -m roofAI version --show_description 1)${@:2}"
        return
    fi

    python3 -m roofAI \
        "$task" \
        "${@:2}"
}
