#! /usr/bin/env bash

export roofAI_ingest_sources="CamVid|AIRS"

function roofAI_ingest() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        abcli_show_usage "roofAI ingest$ABCUL[dryrun,source=$roofAI_ingest_sources,upload]$ABCUL<object-name>" \
            "ingest -> <object-name>."
        return
    fi

    local object_name=$(abcli_clarify_object $2 .)
    local object_path=$abcli_object_root/$object_name
    mkdir -p $object_path

    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_upload=$(abcli_option_int "$options" upload 0)
    local source=$(abcli_option "$options" source)

    if [[ "|$roofAI_ingest_sources|" != *"|$source|"* ]]; then
        abcli_log_error "-roofAI: ingest: $source: source not found."
        return 1
    fi

    abcli_log "ingesting $source -> $object_name"

    if [ "$source" == "CamVid" ]; then
        abcli_log """
The CamVid dataset is a set of:
 - **train** images + segmentation masks
 - **validation** images + segmentation masks
 - **test** images + segmentation masks
 
All images have 320 pixels height and 480 pixels width.
For more inforamtion about dataset visit http://mi.eng.cam.ac.uk/research/projects/VideoRec/CamVid/.

Dataset is downloaded from https://github.com/alexgkendall/SegNet-Tutorial
"""

        # https://github.com/qubvel/segmentation_models.pytorch/blob/master/examples/cars%20segmentation%20(camvid).ipynb
        abcli_eval dryrun=$do_dryrun,path=$object_path \
            abcli_git clone https://github.com/alexgkendall/SegNet-Tutorial object
    fi

    if [ "$source" == "AIRS" ]; then
        echo "wip"
    fi

    [[ "$do_upload" == 1 ]] &&
        abcli_upload - $object_name
}
