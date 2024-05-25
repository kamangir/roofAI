#! /usr/bin/env bash

function roofAI_action_git_before_push() {
    roofAI pypi build
}
