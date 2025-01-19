#! /usr/bin/env bash

function roofai_action_git_before_push() {
    roofai build_README
    [[ $? -ne 0 ]] && return 1

    [[ "$(abcli_git get_branch)" != "main" ]] &&
        return 0

    roofai pypi build
}
