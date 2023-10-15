#! /usr/bin/env bash

export roofAI_ingest_sources="CamVid|AIRS"
export roofAI_ingest_AIRS_cache_object_name=AIRS-v1

function roofAI_ingest() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        local options="~download,dryrun,~from_cache,source=$roofAI_ingest_sources,upload"
        abcli_show_usage "roofAI ingest$ABCUL[$options]$ABCUL<object-name>" \
            "ingest -> <object-name>."
        return
    fi

    local object_name=$(abcli_clarify_object $2 .)
    local object_path=$abcli_object_root/$object_name
    mkdir -p $object_path

    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_download=$(abcli_option_int "$options" download 1)
    local do_upload=$(abcli_option_int "$options" upload 0)
    local source=$(abcli_option "$options" source)

    if [[ "|$roofAI_ingest_sources|" != *"|$source|"* ]]; then
        abcli_log_error "-roofAI: ingest: $source: source not found."
        return 1
    fi

    abcli_log "ingesting $source -> $object_name"

    local args=""

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
        local from_cache=$(abcli_option_int "$options" from_cache 1)

        local cache_object_name=$roofAI_ingest_AIRS_cache_object_name
        local cache_object_path=$abcli_object_root/$cache_object_name

        # https://arash-kamangir.medium.com/roofai-1-airs-b440ebb54968
        if [[ "$from_cache" == 0 ]]; then
            abcli_log "caching $source -> $cache_object_name"

            abcli_eval dryrun=$do_dryrun,path=$cache_object_path \
                "kaggle datasets download \
                -d atilol/aerialimageryforroofsegmentation \
                -p ./; \
                unzip aerialimageryforroofsegmentation.zip"

            [[ "$do_upload" == 1 ]] &&
                abcli_upload - $cache_object_name
        else
            [[ "$do_download" == 1 ]] &&
                abcli_download - $cache_object_name

            abcli_log "using $source cache: $cache_object_name"
        fi

        local args="--cache_path $cache_object_path"
    fi

    abcli_eval dryrun=$do_dryrun \
        python3 -m roofAI.ingest \
        --source $source \
        --ingest_path $object_path \
        "$args" \
        "${@:3}"

    [[ "$do_upload" == 1 ]] &&
        abcli_upload - $object_name
}
