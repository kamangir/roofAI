#! /usr/bin/env bash

function roofAI_test() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        abcli_show_usage "roofAI test [all|sagemaker|semseg,dryrun]" \
            "test roofAI."
        return
    fi

    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local target=$(abcli_option_choice "$options" sagemaker,semseg all)

    local test_sagemaker=false
    local test_semseg=false
    [[ "|all|sagemaker|" == *"|$target|"* ]] && test_sagemaker=true
    [[ "|all|semseg|" == *"|$target|"* ]] && test_semseg=true

    local source
    for source in AIRS CamVid; do
        abcli_eval dryrun=$do_dryrun \
            conda activate $(roofAI_conda environment_name semseg)

        abcli_log "📜 ingesting $source..."

        local dataset_object_name=roofAI-dataset-${source}-$(abcli_string_timestamp)

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

        if [[ "$test_semseg" == true ]]; then
            abcli_log "📜 training on $source..."

            local classes=car
            [[ "$source" == AIRS ]] && local classes=roof

            local model_object_name=roofAI-semseg-model-${source}-$(abcli_string_timestamp)

            abcli_eval dryrun=$do_dryrun \
                roofAI semseg train \
                profile=VALIDATION \
                $dataset_object_name \
                $model_object_name \
                --classes $classes

            abcli_log "📜 predicting on $source..."

            local prediction_object_name=roofAI-semseg-prediction-${source}-$(abcli_string_timestamp)

            abcli_eval dryrun=$do_dryrun \
                roofAI semseg predict \
                profile=VALIDATION \
                $model_object_name \
                $dataset_object_name \
                $prediction_object_name
        fi

        [[ "$source" != AIRS ]] && continue

        abcli_log "📜 ingesting $source for training on SageMaker ..."

        local dataset_object_name=roofAI-sagemaker-dataset-${source}-$(abcli_string_timestamp)

        abcli_eval dryrun=$do_dryrun \
            roofAI dataset ingest \
            source=$source,target=sagemaker,upload \
            $dataset_object_name \
            --test_count 0 \
            --train_count 16 \
            --val_count 16

        if [[ "$test_sagemaker" == true ]]; then
            abcli_log "📜 training $source on SageMaker ..."

            local model_object_name=roofAI-sagemaker-semseg-${source}-$(abcli_string_timestamp)

            abcli_eval dryrun=$do_dryrun \
                conda activate $(roofAI_conda environment_name sagemaker)

            abcli_eval dryrun=$do_dryrun \
                sagesemseg train - \
                $dataset_object_name \
                $model_object_name \
                --instance_type ml.g4dn.2xlarge
        fi

    done
}
