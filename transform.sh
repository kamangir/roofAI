#! /usr/bin/env bash

# run this script to transform the plugin to a repo with the given name.

function transform() {
    local plugin_name=$(basename $(pwd))

    abcli_log "blue_plugin transformer $version -> $plugin_name"

    git mv blue_plugin $plugin_name
    git mv .abcli/blue_plugin.sh .abcli/$plugin_name.sh
    git mv .abcli/install/blue_plugin.sh .abcli/install/$plugin_name.sh
    rm -v  .abcli/session.sh

    local filename
    for filename in \
        bats/.abcli/install/bats.sh \
        bats/.abcli/bats.sh \
        bats/bats/__init__.py \
        bats/setup.py ; do

        python3 -m abcli.file replace \
            --filename ~/git/$filename \
            --this blue_plugin \
            --that $plugin_name
    done

    echo "# $plugin_name" > README.md
}

transform "$@"