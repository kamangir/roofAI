#! /usr/bin/env bash

export roofAI_ingest_sources="CamVid|AIRS"

function roofAI_ingest() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        local common_options="dryrun,suffix=<v1>,register,upload"

        abcli_show_usage "roofAI ingest$ABCUL[cache,,~from_cache,source=AIRS,$common_options]$ABCUL<object-name>" \
            "ingest AIRS -> <object-name>."

        abcli_show_usage "roofAI ingest$ABCUL[source=CamVid,$common_options]$ABCUL<object-name>" \
            "ingest CamVid -> <object-name>."
        return
    fi

    local from_cache=$(abcli_option_int "$options" from_cache 1)
    local do_cache=$(abcli_option_int "$options" cache $(abcli_not $from_cache))
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_register=$(abcli_option_int "$options" register 0)
    local do_upload=$(abcli_option_int "$options" upload 0)
    local suffix=$(abcli_option "$options" suffix v1)
    local source=$(abcli_option "$options" source)

    local cache_keyword=roofAI_ingest_${source}_cache

    if [[ "|$roofAI_ingest_sources|" != *"|$source|"* ]]; then
        abcli_log_error "-roofAI: ingest: $source: source not found."
        return 1
    fi

    local object_name=$(abcli_clarify_object $2 roofAI_ingest_${source}_$(abcli_string_timestamp))
    local object_path=$abcli_object_root/$object_name
    mkdir -p $object_path

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
        local cache_object_name=""
        [[ "$from_cache" == 1 ]] &&
            local cache_object_name=$(abcli_cache read $cache_keyword)

        if [[ -z "$cache_object_name" ]]; then
            local cache_object_name=roofAI_ingest_${source}_cache_$(abcli_string_timestamp)

            abcli_log "caching $source -> $cache_object_name"

            # https://arash-kamangir.medium.com/roofai-1-airs-b440ebb54968
            abcli_eval dryrun=$do_dryrun,path=$abcli_object_root/$cache_object_name \
                "kaggle datasets download \
                -d atilol/aerialimageryforroofsegmentation \
                -p ./; \
                unzip aerialimageryforroofsegmentation.zip;
                rm -v aerialimageryforroofsegmentation.zip"
        fi

        [[ "$do_cache" == 1 ]] &&
            abcli_cache write \
                $cache_keyword \
                $cache_object_name

        local args="--cache_path $abcli_object_root/$cache_object_name"
        abcli_log "using cache: $cache_object_name"

    fi

    abcli_eval dryrun=$do_dryrun \
        python3 -m roofAI.ingest \
        --source $source \
        --ingest_path $object_path \
        "$args" \
        "${@:3}"

    [[ "$do_dryrun" == 0 ]] &&
        abcli_log_file $object_path/metadata.yaml

    [[ "$do_upload" == 1 ]] &&
        abcli_upload - $object_name

    [[ "$do_register" == 1 ]] &&
        abcli_cache write roofAI_ingest_${source}_${suffix} $object_name
}
