#! /usr/bin/env bash

function roofAI_conda() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ]; then
        abcli_show_usage "roofAI conda create_env [validate]" \
            "create conda environmnt."
        abcli_show_usage "roofAI conda validate" \
            "validate conda environmnt."
        return
    fi

    if [ "$task" == "create_env" ]; then
        local options=$2
        local do_validate=$(abcli_option_int "$options" validate 0)

        abcli_conda create_env clone=base,name=roofAI

        pip3 install pymysql==0.10.1
        pip3 install -U albumentations[imgaug]
        pip3 install timm
        pip3 install pretrainedmodels
        pip3 install efficientnet_pytorch
        pip3 install segmentation_models_pytorch

        [[ "$do_validate" == 1 ]] && roofAI_conda validate

        return
    fi

    if [ "$task" == validate ]; then
        abcli_eval - aws --version
        python3 -c "import torch; print(f'pytorch-{torch.__version__}')"
        return
    fi

    abcli_log_error "-roofAI: conda: $task: command not found."
}
