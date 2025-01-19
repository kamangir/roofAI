#! /usr/bin/env bash

function abcli_install_roofai() {

    [[ "$abcli_is_sagemaker_system" == true ]] && return 0

    # done in .github/workflows
    [[ "$abcli_is_github_workflow" == true ]] && return 0

    local filename="$HOME/.cache/torch/hub/checkpoints/se_resnext50_32x4d-a260b3a4.pth"

    [[ -f "$filename" ]] && return 0

    local path=$(dirname "$filename")
    mkdir -pv "$path"

    abcli_eval - \
        curl \
        --insecure \
        -L http://data.lip6.fr/cadene/pretrainedmodels/se_resnext50_32x4d-a260b3a4.pth \
        -o $filename
}

abcli_install_module roofai 1.2.1
