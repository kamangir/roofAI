#! /usr/bin/env bash

function blue_plugin() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ] ; then
        abcli_show_usage "blue_plugin task [<thing_1+thing_2>|all]" \
            "task things."

        # blue_plugin_task $@

        if [ "$(abcli_keyword_is $2 verbose)" == true ] ; then
            python3 -m blue_plugin --help
        fi
        return
    fi

    local function_name=blue_plugin_$task
    if [[ $(type -t $function_name) == "function" ]] ; then
        $function_name "${@:2}"
        return
    fi

    if [ "$task" == "task" ] ; then
        python3 -m blue_plugin \
            task \
            --what $(abcli_clarify_input $2 all) \
            ${@:3}
        return
    fi

    python3 -m blue_plugin \
        $task \
        ${@:2}
}