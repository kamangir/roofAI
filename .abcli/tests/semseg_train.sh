#! /usr/bin/env bash

function test_roofAI_semseg_train() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)

    local source=$(abcli_option "$options" source)
    if [[ -z "$source" ]]; then
        abcli_log_error "unknown source."
        return 1
    fi

    abcli_eval dryrun=$do_dryrun \
        conda activate $(roofAI_conda environment_name semseg)

    abcli_log "📜 ingesting $source..."

    local dataset_object_name=dataset-$(abcli_string_timestamp)

    abcli_eval dryrun=$do_dryrun \
        roofAI dataset ingest \
        source=$source,$2 \
        $dataset_object_name \
        --test_count 16 \
        --train_count 16 \
        --val_count 16

    abcli_log "📜 training on $source..."

    local classes=car
    [[ "$source" == AIRS ]] && local classes=roof

    local model_object_name=model-$(abcli_string_timestamp)

    abcli_eval dryrun=$do_dryrun \
        roofAI semseg train \
        profile=VALIDATION,$3 \
        $dataset_object_name \
        $model_object_name \
        --classes $classes

    abcli_log "📜 predicting on $source..."

    local prediction_object_name=prediction-$(abcli_string_timestamp)

    abcli_eval dryrun=$do_dryrun \
        roofAI semseg predict \
        profile=VALIDATION,$4 \
        $model_object_name \
        $dataset_object_name \
        $prediction_object_name \
        "${@:5}"
}

function test_roofAI_semseg_train_batch() {
    local source
    for source in AIRS CamVid; do
        test_roofAI_semseg_train \
            "arg=$arg,$1" \
            "${@:2}"
    done
}
