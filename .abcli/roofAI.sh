#! /usr/bin/env bash

function roofAI() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ]; then
        roofAI version \\n

        abcli_show_usage "roofAI task [<thing_1+thing_2>|all]" \
            "task things."

        # blue_plugin_task $@

        if [ "$(abcli_keyword_is $2 verbose)" == true ]; then
            python3 -m roofAI --help
        fi
        return
    fi

    local function_name=blue_plugin_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
        return
    fi

    if [ "$task" == "init" ]; then
        abcli_init roofAI "${@:2}"
        return
    fi

    if [ "$task" == "task" ]; then
        python3 -m roofAI \
            task \
            --what $(abcli_clarify_input $2 all) \
            ${@:3}
        return
    fi

    if [ "$task" == "version" ]; then
        abcli_log "🏠 $(python3 -m roofAI version --show_description 1)${@:2}"
        return
    fi

    python3 -m roofAI \
        $task \
        ${@:2}
}
