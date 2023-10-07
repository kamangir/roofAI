#! /usr/bin/env bash

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
        return
    fi

    if [ "$task" == "seed" ]; then
        abcli_log "exec(Path(f'{os.getenv(\"HOME\")}/git/roofAI/roofAI/QGIS.py').read_text())"
        return
    fi

    abcli_log_error "-QGIS: $task: command not found."
}
