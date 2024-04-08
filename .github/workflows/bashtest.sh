#! /usr/bin/env bash

function runme() {
    # set -x # verbose-mode

    python -m pip install --upgrade pip
    pip3 install -e .
    pip3 install -r requirements.txt

    local git_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
    for i in {1..3}; do
        git_root=$(dirname $git_root)
    done
    echo "git_root: $git_root"

    pushd $git_root >/dev/null
    git clone https://github.com/kamangir/awesome-bash-cli.git
    cd awesome-bash-cli
    pip3 install -e .
    pip3 install -r requirements.txt
    popd >/dev/null

    source $git_root/awesome-bash-cli/bash/abcli.sh ~terraform

    blue_plugin test "$@"

    return
}

runme "$@"
