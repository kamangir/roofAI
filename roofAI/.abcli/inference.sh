#! /usr/bin/env bash

function roofAI_inference() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ]; then
        for task in create delete describe invoke list pull; do
            roofAI_inference "$task" "$@"
        done
        return
    fi
    local options=$2

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        case $task in
        "create")
            local args="[--verbose 1]$ABCUL[--verify 0]"
            local options="dryrun,model"
            abcli_show_usage "roofAI inference create$ABCUL[$options]$ABCUL[.|<object-name>]$ABCUL$args" \
                "create inference model."

            local options="dryrun,endpoint_config,suffix=<suffix>"
            abcli_show_usage "roofAI inference create$ABCUL[$options]$ABCUL[.|<object-name>]$ABCUL$args" \
                "create inference endpoint config."

            local options="dryrun,endpoint,config_suffix=<suffix>,suffix=<suffix>"
            abcli_show_usage "roofAI inference create$ABCUL[$options]$ABCUL[.|<object-name>]$ABCUL$args" \
                "create inference endpoint."
            ;;
        "delete")
            local args="[--verbose 1]"
            local options="dryrun,model|endpoint_config|endpoint"
            abcli_show_usage "roofAI inference delete$ABCUL[$options]$ABCUL<name>$ABCUL$args" \
                "delete inference object."
            ;;
        "describe")
            local args="[--verbose 1]"
            local options="dryrun,endpoint"
            abcli_show_usage "roofAI inference describe$ABCUL[$options]$ABCUL<name>$ABCUL$args" \
                "describe inference endpoint."
            ;;
        "invoke")
            local args="[--verbose 1]"
            local options="~download,dryrun,profile=$semseg_profiles,upload"
            abcli_show_usage "roofAI inference invoke$EOP$ABCUL[$options]$ABCUL[-|<endpoint-name>]$ABCUL[..|<dataset-object-name>]$ABCUL[-|<prediction-object-name>]$ABCUL$args$EOPE" \
                "<dataset-object-name> -> inference endpoint -> <prediction-object-name>." \
                "default endpoint: $(roofAI_inference_default_endpoint)"
            ;;
        "list")
            local args="[--verbose 1]"
            local options="dryrun,model|endpoint_config|endpoint,contains=<string>"
            abcli_show_usage "roofAI inference list$ABCUL[$options]$ABCUL$args" \
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

    if [[ ",create,delete,describe,list," == *",$task,"* ]]; then
        local object_type=$(abcli_option_choice "$options" model,endpoint_config,endpoint model)
        local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    fi

    if [[ "$task" == "create" ]]; then
        local object_name=$(abcli_clarify_object $3 .)

        [[ "$object_type" == "model" ]] &&
            abcli_upload solid,~warn_if_exists $object_name

        abcli_eval dryrun=$do_dryrun \
            python3 -m roofAI.inference create \
            --suffix $(abcli_option "$options" suffix -) \
            --config_suffix $(abcli_option "$options" config_suffix -) \
            --object_type "$object_type" \
            --object_name "$object_name" \
            "${@:4}"
        return
    fi

    if [[ ",delete,describe," == *",$task,"* ]]; then
        abcli_eval dryrun=$do_dryrun \
            python3 -m roofAI.inference $task \
            --object_type "$object_type" \
            --object_name "$3" \
            "${@:4}"
        return
    fi

    if [[ "$task" == "invoke" ]]; then
        local do_dryrun=$(abcli_option_int "$options" dryrun 0)
        local do_download=$(abcli_option_int "$options" download $(abcli_not $do_dryrun))
        local do_upload=$(abcli_option_int "$options" upload $(abcli_not $do_dryrun))

        local endpoint_name=$(abcli_clarify_input $3 $(roofAI_inference_default_endpoint))

        local dataset_object_name=$(abcli_clarify_object $4 ..)
        [[ "$do_download" == 1 ]] &&
            abcli_download - $dataset_object_name

        local prediction_object_name=$(abcli_clarify_object $5 $(abcli_string_timestamp))

        abcli_log "endpoint[$endpoint_name].invoke($dataset_object_name) -> $prediction_object_name."

        abcli_eval dryrun=$do_dryrun \
            python3 -m roofAI.inference $task \
            --endpoint_name $endpoint_name \
            --dataset_path $ABCLI_OBJECT_ROOT/$dataset_object_name \
            --prediction_path $ABCLI_OBJECT_ROOT/$prediction_object_name \
            --profile $(abcli_option "$options" profile VALIDATION) \
            "${@:6}"

        [[ "$do_upload" == 1 ]] &&
            abcli_upload - $prediction_object_name

        return
    fi

    if [[ "$task" == "list" ]]; then
        abcli_eval dryrun=$do_dryrun \
            python3 -m roofAI.inference $task \
            --object_type "$object_type" \
            --object_name $(abcli_option "$options" contains -) \
            "${@:3}"
        return
    fi

    if [ "$task" == "pull" ]; then
        aws ecr get-login-password \
            --region $ABCLI_AWS_REGION |
            docker login \
                --username AWS \
                --password-stdin \
                763104351884.dkr.ecr.$ABCLI_AWS_REGION.amazonaws.com
        [[ $? -ne 0 ]] && return 1

        local image_name=$(python3 -m roofAI.inference.image get --what name)
        abcli_log "🔗 image name: $image_name"
        abcli_eval dryrun=$do_dryrun \
            docker pull $image_name

        return
    fi

    abcli_log_error "-roofAI: inference: $task: command not found."
    return 1
}

function roofAI_inference_default_endpoint() {
    echo endpoint-$(abcli_cache read roofAI_semseg_model_AIRS_o2)-pytorch
}
