#! /usr/bin/env bash

function roofAI_action_git_before_push() {
    roofAI build_README
    [[ $? -ne 0 ]] && return 1

    [[ "$(abcli_git get_branch)" != "main" ]] &&
        return 0

    roofAI pypi build
}
