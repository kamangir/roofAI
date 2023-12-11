#! /usr/bin/env bash

function roofAI_inference() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ]; then
        for task in create delete list pull; do
            roofAI_inference "$task" "$@"
        done
        return
    fi
    local options=$2

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        case $task in
        "create")
            local options="dryrun,model|endpoint_config"
            abcli_show_usage "roofAI inference create$ABCUL[$options]$ABCUL[.|<object-name>]" \
                "create inference object."

            local options="dryrun,endpoint,config_name=<config-name>"
            abcli_show_usage "roofAI inference create$ABCUL[$options]$ABCUL[.|<object-name>]" \
                "create inference endpoint."
            ;;
        "delete")
            local options="dryrun,model|endpoint_config|endpoint"
            abcli_show_usage "roofAI inference delete$ABCUL[$options]$ABCUL[.|<object-name>]" \
                "delete inference object."
            ;;
        "list")
            local options="dryrun,model|endpoint_config|endpoint,contains=<string>"
            abcli_show_usage "roofAI inference list$ABCUL[$options]" \
                "list inference objects."
            ;;
        "pull")
            local options="dryrun"
            abcli_show_usage "roofAI inference pull$ABCUL[$options]" \
                "pull the inference image."
            ;;
        esac
        return
    fi

    if [[ ",create,delete,list," == *",$task,"* ]]; then
        local object_type=$(abcli_option_choice "$options" model,endpoint_config,endpoint model)
        local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    fi

    if [[ ",create,delete," == *",$task,"* ]]; then
        local object_name=$(abcli_clarify_object $3 .)

        abcli_eval dryrun=$do_dryrun \
            python3 -m roofAI.inference $task \
            --config_name $(abcli_option "$options" config_name void) \
            --object_type "$object_type" \
            --object_name "$object_name" \
            "${@:4}"
        return
    fi

    if [[ "$task" == "list" ]]; then
        abcli_eval dryrun=$do_dryrun \
            python3 -m roofAI.inference $task \
            --config_name $(abcli_option "$options" config_name void) \
            --object_type "$object_type" \
            --object_name $(abcli_option "$options" contains -) \
            "${@:3}"
        return
    fi

    if [ "$task" == "pull" ]; then
        # https://github.com/aws/deep-learning-containers/blob/master/available_images.md
        local repository_name=pytorch-inference
        local image_tag=2.1.0-gpu-py310-cu118-ubuntu20.04-ec2
        local image_name=763104351884.dkr.ecr.us-east-2.amazonaws.com/$repository_name:$image_tag

        aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 763104351884.dkr.ecr.us-east-2.amazonaws.com
        [[ $? -ne 0 ]] && return 1

        abcli_eval dryrun=$do_dryrun \
            docker pull $image_name

        return
    fi

    abcli_log_error "-roofAI: inference: $task: command not found."
}
