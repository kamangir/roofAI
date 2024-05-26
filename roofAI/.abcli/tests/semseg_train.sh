#! /usr/bin/env bash

function test_roofAI_semseg_train() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)

    local source=$(abcli_option "$options" source AIRS)
    if [[ -z "$source" ]]; then
        abcli_log_error "unknown source."
        return 1
    fi

    [[ "$abcli_is_github_workflow" == false ]] &&
        abcli_eval dryrun=$do_dryrun \
            conda activate $(roofAI_conda environment_name semseg)

    local dataset_object_name=$(abcli_cache read roofAI_ingest_${source}_v1)

    abcli_log "📜 training on $source - dataset: $dataset_object_name"

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
