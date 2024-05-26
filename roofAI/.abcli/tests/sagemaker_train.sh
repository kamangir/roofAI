#! /usr/bin/env bash

function test_roofAI_sagemaker_train() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)

    abcli_log_warning "🚧 may incur cost 💰, disabled."
    do_dryrun=1

    abcli_eval dryrun=$do_dryrun \
        conda activate $(roofAI_conda environment_name sagemaker)

    local dataset_object_name=dataset-$(abcli_string_timestamp)

    abcli_eval dryrun=$do_dryrun \
        roofAI dataset ingest \
        source=AIRS,target=sagemaker,$2 \
        $dataset_object_name \
        --test_count 0 \
        --train_count 16 \
        --val_count 16

    local model_object_name=model-$(abcli_string_timestamp)

    abcli_eval dryrun=$do_dryrun \
        sagesemseg train \
        ,$3 \
        $dataset_object_name \
        $model_object_name \
        --instance_type ml.g4dn.2xlarge \
        "${@:4}"
}
