#! /usr/bin/env bash

export roofAI_ingest_sources="CamVid|AIRS"

function roofAI_dataset_ingest() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        local common_options="dryrun,open,register,suffix=<v1>,upload"

        local options="source=AIRS,$common_options,target=sagemaker|torch"
        local args="[--test_count <10>]$ABCUL[--train_count <10>]$ABCUL[--val_count <10>]"
        abcli_show_usage "roofAI dataset ingest$ABCUL[$options]$ABCUL<object-name>$ABCUL$args" \
            "ingest AIRS -> <object-name>."

        abcli_show_usage "roofAI dataset ingest$ABCUL[source=CamVid,$common_options]$ABCUL<object-name>" \
            "ingest CamVid -> <object-name>."
        return
    fi

    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_open=$(abcli_option_int "$options" open 0)
    local do_register=$(abcli_option_int "$options" register 0)
    local do_upload=$(abcli_option_int "$options" upload 0)
    local suffix=$(abcli_option "$options" suffix v1)
    local source=$(abcli_option "$options" source)
    local target=$(abcli_option "$options" target torch)

    local cache_keyword=roofAI_ingest_${source}_cache

    if [[ "|$roofAI_ingest_sources|" != *"|$source|"* ]]; then
        abcli_log_error "-roofAI: dataset: ingest: $source: source not found."
        return 1
    fi

    local object_name=$(abcli_clarify_object $2 roofAI_ingest_${source}_$(abcli_string_timestamp))
    local object_path=$ABCLI_OBJECT_ROOT/$object_name
    mkdir -p $object_path
    [[ "$do_open" == 1 ]] &&
        open $object_path

    abcli_log "ingesting $source -> $target:$object_name"

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
        local cache_object_name=$(abcli_cache read $cache_keyword)

        local cache_from_source=0
        if [[ -z "$cache_object_name" ]]; then
            local cache_object_name=roofAI_ingest_${source}_cache_$(abcli_string_timestamp)

            abcli_cache write \
                $cache_keyword \
                $cache_object_name

            cache_from_source=1
        else
            abcli_download - $cache_object_name

            if [[ ! -f $ABCLI_OBJECT_ROOT/$cache_object_name/train.txt ]]; then
                abcli_log "cache is empty: $cache_object_name"
                cache_from_source=1
            fi
        fi

        if [[ "$cache_from_source" == 1 ]]; then
            abcli_log "caching from $source -> $cache_object_name"

            # https://arash-kamangir.medium.com/roofai-1-airs-b440ebb54968
            abcli_eval dryrun=$do_dryrun,path=$ABCLI_OBJECT_ROOT/$cache_object_name \
                "kaggle datasets download \
                -d atilol/aerialimageryforroofsegmentation \
                -p ./"

            abcli_eval dryrun=$do_dryrun,path=$ABCLI_OBJECT_ROOT/$cache_object_name \
                "unzip aerialimageryforroofsegmentation.zip"
        fi

        local args="--cache_path $ABCLI_OBJECT_ROOT/$cache_object_name"

        abcli_log "cache: $cache_keyword -> $cache_object_name"
    fi

    abcli_eval dryrun=$do_dryrun \
        python3 -m roofAI.dataset ingest \
        --source $source \
        --target $target \
        --ingest_path $object_path \
        "$args" \
        "${@:3}"

    [[ "$do_dryrun" == 0 ]] &&
        abcli_cat $object_path/metadata.yaml

    [[ "$do_upload" == 1 ]] &&
        abcli_upload - $object_name

    [[ "$do_register" == 1 ]] &&
        abcli_cache write roofAI_ingest_${source}_${suffix} $object_name

    return 0
}
