#! /usr/bin/env bash

function roof() {
    roofAI "$@"
}

function roofAI() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ]; then
        roofAI version \\n

        abcli_show_usage "roofAI create_conda_env$ABCUL[dryrun,~pip]" \
            "create conda environmnt."

        roofAI_ingest "$@"
        roofAI_QGIS "$@"
        roofAI_semseg "$@"
        abcli_pytest plugin=roofAI,"$@"
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

    if [ "$task" == "create_conda_env" ]; then
        abcli_conda create_env \
            "$2,torch" roofAI \
            "${@:3}"
        pip3 install -U albumentations[imgaug]
        pip3 install timm
        pip3 install pretrainedmodels
        pip3 install efficientnet_pytorch
        return
    fi

    if [ "$task" == "init" ]; then
        abcli_init roofAI "${@:2}"
        conda activate roofAI
        return
    fi

    if [ "$task" == "pytest" ]; then
        abcli_pytest plugin=roofAI,$1 \
            "${@:2}"
        return
    fi

    if [ "$task" == "version" ]; then
        abcli_log "🏠 $(python3 -m roofAI version --show_description 1)${@:2}"
        return
    fi

    python3 -m roofAI \
        "$task" \
        "${@:2}"
}
