#! /usr/bin/env bash

function roofAI_dataset_ingest() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_upload=$(abcli_option_int "$options" upload 0)
    local source=$(abcli_option "$options" source)
    local target=$(abcli_option "$options" target torch)

    if [[ "|CamVid|AIRS|" != *"|$source|"* ]]; then
        abcli_log_error "roofAI: dataset: ingest: $source: source not found."
        return 1
    fi

    local object_name=$(abcli_clarify_object $2 roofAI_ingest_${source}_$(abcli_string_timestamp_short))
    local object_path=$ABCLI_OBJECT_ROOT/$object_name
    mkdir -pv $object_path

    abcli_log "ingesting $source -$target-> $object_name"

    local args=""

    if [ "$source" == "CamVid" ]; then
        # https://github.com/qubvel/segmentation_models.pytorch/blob/master/examples/cars%20segmentation%20(camvid).ipynb
        abcli_eval dryrun=$do_dryrun,path=$object_path \
            abcli_git clone https://github.com/alexgkendall/SegNet-Tutorial object
    fi

    if [ "$source" == "AIRS" ]; then
        local cache_object_name=$ROOFAI_AIRS_CACHE_OBJECT_NAME

        local cache_from_source=0
        if [[ ! -f $ABCLI_OBJECT_ROOT/$cache_object_name/train.txt ]]; then
            abcli_log "cache is empty: $cache_object_name"
            cache_from_source=1
        fi

        if [[ "$cache_from_source" == 1 ]]; then
            abcli_log "caching from $source -> $cache_object_name"

            # https://arash-kamangir.medium.com/roofai-1-airs-b440ebb54968
            abcli_eval dryrun=$do_dryrun,path=$ABCLI_OBJECT_ROOT/$cache_object_name \
                "kaggle datasets download \
                -d atilol/aerialimageryforroofsegmentation \
                -p ./"
            [[ $? -ne 0 ]] && return 1

            abcli_eval dryrun=$do_dryrun,path=$ABCLI_OBJECT_ROOT/$cache_object_name \
                "unzip aerialimageryforroofsegmentation.zip"
        fi

        local args="--cache_path $ABCLI_OBJECT_ROOT/$cache_object_name"
    fi

    abcli_eval dryrun=$do_dryrun \
        python3 -m roofAI.dataset ingest \
        --source $source \
        --target $target \
        --ingest_path $object_path \
        "$args" \
        "${@:3}"
    local status="$?"

    [[ "$do_dryrun" == 0 ]] &&
        abcli_cat $object_path/metadata.yaml

    [[ "$do_upload" == 1 ]] &&
        abcli_upload - $object_name

    return $status
}
