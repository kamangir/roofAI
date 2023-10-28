#! /usr/bin/env bash

function roofAI_conda() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        abcli_show_usage "roofAI conda create_env$ABCUL[dryrun]" \
            "create conda environmnt."
        abcli_show_usage "roofAI conda validate" \
            "validate conda environmnt."
        return
    fi

    if [ "$task" == "create_env"]; then
        local do_dryrun=$(abcli_option_int "$options" dryrun 0)

        conda activate base
        conda remove -y --name roofAI --all

        conda create -y --name roofAI --clone base
        conda activate roofAI

        pushd $abcli_path_git/awesome-bash-cli >/dev/null
        pip3 install -e .
        popd >/dev/null

        abcli_eval \
            dryrun=$do_dryrun,path=$abcli_path_git/roofAI \
            pip3 install -e .

        pip3 install pymysql==0.10.1
        pip3 install -U albumentations[imgaug]
        pip3 install timm
        pip3 install pretrainedmodels
        pip3 install efficientnet_pytorch
        pip3 install segmentation_models_pytorch

        return
    fi

    if [ "$task" == validate ]; then
        abcli_eval - aws
        python3 -c "import torch; print(torch.__version__)"
        return
    fi

    abcli_log_error "-roofAI: conda: $task: command not found."
}