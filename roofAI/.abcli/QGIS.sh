#! /usr/bin/env bash

export abcli_QGIS_path_profile="$HOME/Library/Application Support/QGIS/QGIS3/profiles/default"
export abcli_QGIS_path_expressions=$abcli_QGIS_path_profile/python/expressions
export abcli_QGIS_path_expressions_git=$abcli_path_git/roofAI/roofAI/QGIS/expressions
export abcli_QGIS_path_templates=$abcli_QGIS_path_profile/project_templates
export abcli_QGIS_path_shared=$HOME/Downloads/QGIS
export abcli_QGIS_path_server=$abcli_QGIS_path_shared/server

mkdir -p $abcli_QGIS_path_server

function QGIS() {
    roofAI_QGIS "$@"
}

# internal function to abcli_seed.
function QGIS_seed() {
    # seed is NOT local
    seed=$(python3 -m roofAI.QGIS generate_seed)
}

function roofAI_QGIS() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ]; then
        abcli_show_usage "QGIS seed [screen]" \
            "seed 🌱 QGIS."

        roofAI_QGIS_expressions "$@"
        roofAI_QGIS_server "$@"
        return
    fi

    local function_name=roofAI_QGIS_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
        return
    fi

    if [ "$task" == "seed" ]; then
        abcli_seed QGIS "${@:2}"
        return
    fi

    abcli_log_error "-QGIS: $task: command not found."
    return 1
}

abcli_source_path - caller,suffix=/QGIS
