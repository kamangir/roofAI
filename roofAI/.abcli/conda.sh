#! /usr/bin/env bash

function roofAI_conda() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ]; then
        abcli_show_usage "roofAI conda activate [sagemaker|semseg]" \
            "activate conda environment."
        abcli_show_usage "roofAI conda create [~validate,~recreate,sagemaker|semseg]" \
            "create conda environment."
        abcli_show_usage "roofAI conda environment_name [sagemaker|semseg]" \
            "return conda environment_name"
        abcli_show_usage "roofAI conda validate" \
            "validate conda environment."
        return
    fi

    local options=$2
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)

    if [ "$task" == "activate" ]; then
        abcli_eval dryrun=$do_dryrun \
            conda activate \
            $(roofAI_conda environment_name $options)
        return
    fi

    if [ "$task" == "create" ]; then
        local do_recreate=$(abcli_option_int "$options" recreate 1)
        local do_validate=$(abcli_option_int "$options" validate 1)
        local target=$(abcli_option_choice "$options" sagemaker,semseg semseg)
        local environment_name=$(roofAI_conda environment_name $options)

        if [[ "$environment_name" == base ]]; then
            abcli_log "using: $environment_name"
            abcli_eval dryrun=$do_dryrun \
                conda activate $environment_name
        else
            if [[ "$do_recreate" == 0 ]] && [[ $(abcli_conda exists $environment_name) == 1 ]]; then
                abcli_eval dryrun=$do_dryrun \
                    conda activate $environment_name
                return
            fi

            abcli_log "creating: $environment_name"

            abcli_conda create \
                name=$environment_name,repo=roofAI
        fi

        pip3 install pymysql
        pip3 install matplotlib
        pip3 install boto3

        if [[ "$target" == sagemaker ]]; then
            [[ "$abcli_is_sagemaker" == false ]] &&
                pip3 install 'sagemaker>=2,<3'

            # don't know why - benign, nevertheless. :)
            abcli_plugins install roofAI
        fi

        abcli_plugins install notebooks_and_scripts

        [[ "$do_validate" == 1 ]] && roofAI_conda validate

        return
    fi

    if [ "$task" == "environment_name" ]; then
        local target=$(abcli_option_choice "$options" sagemaker,semseg semseg)

        if [[ "$target" == sagemaker ]] && [[ "$abcli_is_sagemaker" == true ]]; then
            echo base
        else
            echo roofAI-$target
        fi
        return
    fi

    if [ "$task" == validate ]; then
        abcli_eval dryrun=$do_dryrun \
            aws --version

        if [[ "$CONDA_DEFAULT_ENV" == "roofAI-semseg" ]]; then
            python3 -c "import torch; print(f'pytorch-{torch.__version__}')"
        else
            python3 -c "import sagemaker; print(f'sagemaker-{sagemaker.__version__}')"
        fi
        return
    fi

    abcli_log_error "-roofAI: conda: $task: command not found."
    return 1
}
