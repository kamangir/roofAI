#! /usr/bin/env bash

export abcli_QGIS_path_profile="$abcli_path_home/Library/Application Support/QGIS/QGIS3/profiles/default"
export abcli_QGIS_path_expressions=$abcli_QGIS_path_profile/python/expressions
export abcli_QGIS_path_expressions_git=$abcli_path_git/roofAI/roofAI/QGIS/expressions
export abcli_QGIS_path_templates=$abcli_QGIS_path_profile/project_templates
export abcli_QGIS_path_cache=$abcli_path_home/Downloads/QGIS
export abcli_QGIS_path_server=$abcli_path_home/Downloads/QGIS/server

mkdir -p $abcli_QGIS_path_server

function QGIS() {
    roofAI_QGIS "$@"
}

function QGIS_seed() {
    roofAI_QGIS seed "$@"
}

function roofAI_QGIS() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ]; then
        abcli_show_usage "QGIS seed" \
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
        echo "exec(Path(f'{os.getenv(\"HOME\")}/git/roofAI/roofAI/QGIS/seed.py').read_text())"
        return
    fi

    abcli_log_error "-QGIS: $task: command not found."
}

abcli_source_path $abcli_path_git/roofAI/.abcli/QGIS
