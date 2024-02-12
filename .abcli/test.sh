#! /usr/bin/env bash

function roofAI_test() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        abcli_show_usage "roofAI test [dryrun]" \
            "test roofAI."
        return
    fi

    local do_dryrun=$(abcli_option_int "$options" dryrun 0)

    local source
    for source in AIRS CamVid; do
        abcli_log "📜 ingesting $source..."

        abcli_cache write roofAI_ingest_${source}_test void

        abcli_eval dryrun=$do_dryrun \
            roofAI dataset ingest \
            source=$source,register,suffix=test \
            roofAI_dataset_$(abcli_string_timestamp) \
            --test_count 16 \
            --train_count 16 \
            --val_count 16

        abcli_eval dryrun=$do_dryrun \
            roofAI dataset review - \
            $(abcli_cache read roofAI_ingest_${source}_test) \
            --count 1 \
            --index 1 \
            --subset test

        abcli_log "📜 training on $source..."

        local classes=car
        [[ "$source" == AIRS ]] && local classes=roof

        abcli_cache write roofAI_semseg_model_${source}_test void

        abcli_eval dryrun=$do_dryrun \
            roofAI semseg train \
            profile=VALIDATION,register,suffix=test,~upload \
            $(abcli_cache read roofAI_ingest_${source}_test) \
            roofAI-${source}-semseg-model-$(abcli_string_timestamp) \
            --classes $classes

        abcli_log "📜 predicting on $source..."

        abcli_eval dryrun=$do_dryrun \
            roofAI semseg predict \
            profile=VALIDATION \
            $(abcli_cache read roofAI_semseg_model_${source}_test) \
            $(abcli_cache read roofAI_ingest_${source}_test) \
            roofAI-${source}-semseg-prediction-$(abcli_string_timestamp)
    done
}
