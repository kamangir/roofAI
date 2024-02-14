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

        local dataset_object_name=roofAI_dataset_${source}_$(abcli_string_timestamp)

        abcli_eval dryrun=$do_dryrun \
            roofAI dataset ingest \
            source=$source \
            $dataset_object_name \
            --test_count 16 \
            --train_count 16 \
            --val_count 16

        abcli_eval dryrun=$do_dryrun \
            roofAI dataset review - \
            $dataset_object_name \
            --count 1 \
            --index 1 \
            --subset test

        abcli_log "📜 training on $source..."

        local classes=car
        [[ "$source" == AIRS ]] && local classes=roof

        local model_object_name=roofAI_semseg_model_${source}_$(abcli_string_timestamp)

        abcli_eval dryrun=$do_dryrun \
            roofAI semseg train \
            profile=VALIDATION \
            $dataset_object_name \
            $model_object_name \
            --classes $classes

        abcli_log "📜 predicting on $source..."

        local prediction_object_name=roofAI_semseg_${source}_prediction_$(abcli_string_timestamp)

        abcli_eval dryrun=$do_dryrun \
            roofAI semseg predict \
            profile=VALIDATION \
            $model_object_name \
            $dataset_object_name \
            $prediction_object_name

        [[ "$source" != AIRS ]] && continue

        abcli_log "📜 ingesting $source for training on SageMaker ..."

        local dataset_object_name=roofAI_dataset_${source}_for_sagemaker_$(abcli_string_timestamp)

        abcli_eval dryrun=$do_dryrun \
            roofAI dataset ingest \
            source=$source,target=sagemaker \
            $dataset_object_name \
            --test_count 16 \
            --train_count 16 \
            --val_count 16
    done
}
