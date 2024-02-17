#! /usr/bin/env bash

function roofAI_conda() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ]; then
        abcli_show_usage "roofAI conda create_env [~validate,~recreate,sagemaker|semseg]" \
            "create conda environment."
        abcli_show_usage "roofAI conda validate" \
            "validate conda environment."
        return
    fi

    if [ "$task" == "create_env" ]; then
        local options=$2
        local do_recreate=$(abcli_option_int "$options" recreate 1)
        local do_validate=$(abcli_option_int "$options" validate 1)
        local target=$(abcli_option_choice "$options" sagemaker,semseg sagemaker)

        local environment_name=roofAI-$target

        abcli_log "creating conda environment: $environment_name"

        if [[ "$do_recreate" == 0 ]] && [[ $(abcli_conda exists $environment_name) == 1 ]]; then
            abcli_eval - conda activate $environment_name
            return
        fi

        abcli_conda create_env name=$environment_name

        pip3 install pymysql==0.10.1

        if [[ "$target" == sagemaker ]]; then
            pip3 install 'sagemaker>=2,<3'
        else
            pip3 install -U albumentations[imgaug]
            pip3 install timm
            pip3 install kaggle
            pip3 install pretrainedmodels
            pip3 install efficientnet_pytorch
            pip3 install segmentation_models_pytorch
        fi

        abcli_plugins install notebooks_and_scripts

        [[ "$do_validate" == 1 ]] && roofAI_conda validate

        return
    fi

    if [ "$task" == validate ]; then
        abcli_eval - aws --version
        python3 -c "import torch; print(f'pytorch-{torch.__version__}')"
        python3 -c "import sagemaker; print(f'sagemaker-{sagemaker.__version__}')"
        return
    fi

    abcli_log_error "-roofAI: conda: $task: command not found."
}
