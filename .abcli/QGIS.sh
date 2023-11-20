#! /usr/bin/env bash

export abcli_QGIS_path_profile="$HOME/Library/Application Support/QGIS/QGIS3/profiles/default"
export abcli_QGIS_path_expressions=$abcli_QGIS_path_profile/python/expressions
export abcli_QGIS_path_expressions_git=$abcli_path_git/roofAI/roofAI/QGIS/expressions
export abcli_QGIS_path_templates=$abcli_QGIS_path_profile/project_templates

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

function roofAI_QGIS_expressions() {
    local task=$1

    if [ "$task" == help ]; then
        abcli_show_usage "QGIS expressions pull" \
            "pull QGIS expressions."
        abcli_show_usage "QGIS expressions push [push]" \
            "push QGIS expressions."

        abcli_log " 📂 $abcli_QGIS_path_expressions"
        abcli_log " 📂 $abcli_QGIS_path_expressions_git"
        return
    fi

    if [[ "$task" == pull ]]; then
        rsync -av \
            "$abcli_QGIS_path_expressions_git/" \
            "$abcli_QGIS_path_expressions/"
        return
    fi

    if [[ "$task" == push ]]; then
        local options=$2
        local do_push=$(abcli_option_int "$options" push 0)

        rsync -av \
            --exclude='__pycache__' \
            --exclude='default.py' \
            --exclude='__init__.py' \
            "$abcli_QGIS_path_expressions/" \
            "$abcli_QGIS_path_expressions_git/"

        if [[ "$do_push" == 1 ]]; then
            abcli_git push \
                roofAI \
                accept_no_issue \
                "$(python3 -m roofAI version) QGIS expressions"
        else
            abcli_git roofAI status
        fi

        return
    fi

    abcli_log_error "-QGIS: expressions: $task: command not found."
}
