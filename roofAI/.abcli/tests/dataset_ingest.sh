#! /usr/bin/env bash

function test_roofAI_dataset_ingest() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)

    local source=$(abcli_option "$options" source CamVid)
    if [[ -z "$source" ]]; then
        abcli_log_error "unknown source."
        return 1
    fi

    [[ "$abcli_is_github_workflow" == false ]] &&
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

    abcli_eval dryrun=$do_dryrun \
        roofAI dataset review \
        ,$3 \
        $dataset_object_name \
        --count 1 \
        --index 1 \
        --subset test \
        "${@:4}"
}
