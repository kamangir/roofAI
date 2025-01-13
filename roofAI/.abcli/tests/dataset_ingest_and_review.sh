#! /usr/bin/env bash

function test_roofAI_dataset_ingest_and_review() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)

    local source=$(abcli_option "$options" source CamVid)

    abcli_log "📜 ingesting $source..."

    local dataset_object_name=test_roofAI_dataset_ingest_and_review-$(abcli_string_timestamp_short)

    abcli_eval dryrun=$do_dryrun \
        roofAI dataset ingest \
        source=$source,$2 \
        $dataset_object_name \
        --test_count 16 \
        --train_count 16 \
        --val_count 16
    [[ $? -ne 0 ]] && return 1

    abcli_eval dryrun=$do_dryrun \
        roofAI dataset review \
        ,$3 \
        $dataset_object_name \
        --count 1 \
        --index 1 \
        --subset test \
        "${@:4}"
}
