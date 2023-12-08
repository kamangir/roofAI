#! /usr/bin/env bash

function roofAI_inference() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ]; then
        abcli_show_usage "roofAI inference start" \
            "start the inference image."
        return
    fi

    if [ "$task" == "start" ]; then

        return
    fi

    abcli_log_error "-roofAI: inference: $task: command not found."
}
