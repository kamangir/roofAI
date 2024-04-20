#! /usr/bin/env bash

function runme() {
    # set -x # verbose-mode

    local git_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
    for i in {1..3}; do
        git_root=$(dirname $git_root)
    done
    echo "git_root: $git_root"

    pushd $git_root >/dev/null
    git clone https://github.com/kamangir/awesome-bash-cli.git
    popd >/dev/null

    source $git_root/awesome-bash-cli/bash/abcli.sh ~terraform

    roofAI test "$@"

    return
}

runme "$@"
