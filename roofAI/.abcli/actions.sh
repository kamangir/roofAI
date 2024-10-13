#! /usr/bin/env bash

function roofAI_action_git_before_push() {
    [[ "$(abcli_git get_branch)" != "main" ]] &&
        return 0

    roofAI pypi build
}
