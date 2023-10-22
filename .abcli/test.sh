#! /usr/bin/env bash

function roofAI_test() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        abcli_show_usage "roofAI test [~dataset,dryrun,~semseg]" \
            "test roofAI."
        return
    fi

    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local test_dataset=$(abcli_option_int "$options" dataset 1)
    local test_semseg=$(abcli_option_int "$options" semseg 1)

    if [ "$test_dataset" == 1 ]; then
        abcli_log "testing dataset..."
        local dataset_object_name=dataset-$(@timestamp)

        abcli_eval dryrun=$do_dryrun \
            roofAI dataset ingest \
            source=AIRS \
            $dataset_object_name \
            --test_count 5 \
            --train_count 5 \
            --val_count 5

        abcli_eval dryrun=$do_dryrun \
            roofAI dataset review - \
            $dataset_object_name \
            --count 1 \
            --index 1 \
            --subset test
    fi

    if [ "$test_semseg" == 1 ]; then
        local dataset_source
        for dataset_source in AIRS CamVid; do
            abcli_log "testing semseg on $dataset_source..."

            local classes=car
            [[ "$dataset_source" == AIRS ]] && local classes=roof

            abcli_cache write roofAI_semseg_model_${dataset_source}_test void

            abcli_eval dryrun=$do_dryrun \
                roofAI semseg train \
                profile=VALIDATION,register,suffix=test \
                $(@ref roofAI_ingest_${dataset_source}_v1) \
                roofAI-${dataset_source}-semseg-model-$(@timestamp) \
                --classes $classes

            abcli_eval dryrun=$do_dryrun \
                roofAI semseg predict \
                profile=VALIDATION \
                $(@ref roofAI_semseg_model_${dataset_source}_test) \
                $(@ref roofAI_ingest_${dataset_source}_v1) \
                roofAI-${dataset_source}-semseg-prediction-$(@timestamp)
        done
    fi
}
