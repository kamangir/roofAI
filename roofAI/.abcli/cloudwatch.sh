#! /usr/bin/env bash

function cloudwatch() {
    roofAI_cloudwatch "$@"
}

function roofAI_cloudwatch() {
    local task=${1:=help}

    if [ "$task" == "help" ]; then
        local options="endpoint"
        abcli_show_usage "cloudwatch browse$EOP$ABCUL[$options]$ABCUL[<endpoint-name>]$EOPE" \
            "browse endpoint on cloudwatch." \
            "default endpoint: $(roofAI_inference_default_endpoint)"
        return
    fi

    local options=$2

    # https://docs.aws.amazon.com/sagemaker/latest/dg/logging-cloudwatch.html
    if [ "$task" == "browse" ]; then
        local object_type=$(abcli_option_choice "$options" endpoint endpoint)

        local url=""
        if [[ "$object_type" == endpoint ]]; then
            local endpoint_name=$(abcli_clarify_input $3 $(roofAI_inference_default_endpoint))
            abcli_log "🔗 endpoint: $endpoint_name"
            url="https://$ABCLI_AWS_REGION.console.aws.amazon.com/cloudwatch/home?region=$ABCLI_AWS_REGION#logEventViewer:group=/aws/sagemaker/Endpoints/$endpoint_name"
        else
            abcli_log_error "-cloudwatch: $task: $object_type: object type not found."
            return 1
        fi

        abcli_browse $url
        return
    fi

    abcli_log_error "-roofAI: cloudwatch: $task: command not found."
    return 1
}
