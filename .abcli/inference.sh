#! /usr/bin/env bash

function roofAI_inference() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ]; then
        local options="dryrun"
        abcli_show_usage "roofAI inference start$ABCUL[$options]" \
            "start the inference image."
        return
    fi

    if [ "$task" == "start" ]; then
        local options=$2
        local do_dryrun=$(abcli_option_int "$options" dryrun 0)

        # https://github.com/aws/deep-learning-containers/blob/master/available_images.md
        local repository_name=pytorch-inference
        local image_tag=2.1.0-gpu-py310-cu118-ubuntu20.04-ec2
        local image_name=763104351884.dkr.ecr.us-east-2.amazonaws.com/$repository_name:$image_tag

        aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 763104351884.dkr.ecr.us-east-2.amazonaws.com
        [[ $? -ne 0 ]] && return 1

        abcli_eval dryrun=$do_dryrun \
            docker pull image_name

        return
    fi

    abcli_log_error "-roofAI: inference: $task: command not found."
}
