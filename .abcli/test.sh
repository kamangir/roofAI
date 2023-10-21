#! /usr/bin/env bash

function roofAI_test() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        abcli_show_usage "roofAI test [dryrun]" \
            "test roofAI."
        return
    fi

    local do_dryrun=$(abcli_option_int "$options" dryrun 0)

    abcli_cache write roofAI_semseg_model_CamVid_void void

    abcli_eval dryrun=$do_dryrun \
        roofAI dataset review - \
        $(@cache read roofAI_ingest_CamVid_v1) \
        --count 1 \
        --index 10 \
        --subset test

    abcli_eval dryrun=$do_dryrun \
        roofAI semseg train \
        profile=VALIDATION,register,suffix=void \
        $(@cache read roofAI_ingest_CamVid_v1) \
        roofAI-CamVid-semseg-model-$(@timestamp)

    abcli_eval dryrun=$do_dryrun \
        roofAI semseg predict \
        profile=VALIDATION \
        $(@cache read roofAI_semseg_model_CamVid_void) \
        $(@cache read roofAI_ingest_CamVid_v1) \
        roofAI-CamVid-semseg-prediction-$(@timestamp)
}
