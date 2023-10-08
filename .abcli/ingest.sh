#! /usr/bin/env bash

function roofAI_ingest() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        abcli_show_usage "eoofAI ingest$ABCUL[CamVid]$ABCUL<object-name>" \
            "ingest -> <object-name>."
        return
    fi

    local object_name=$(abcli_clarify_object $2 .)
    local object_path=$abcli_object_root/$object_name
    mkdir -p $object_path

    local source=$(abcli_option_choice "$options" CamVid CamVid)
    local do_upload=$(abcli_option_int "$options" upload 0)

    if [ "$source" == "CamVid" ]; then
        abcli_log "ingesting $source -> $object_name"

        pushd $object_path >/dev/null
        # https://github.com/qubvel/segmentation_models.pytorch/blob/master/examples/cars%20segmentation%20(camvid).ipynb
        abcli_git clone https://github.com/alexgkendall/SegNet-Tutorial object
        popd >/dev/null

        [[ "$do_upload" == 1 ]] &&
            abcli_upload - $object_name
        return
    fi

    abcli_log_error "-roofAI: ingest: $source: source not found."

}
