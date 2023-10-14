#! /usr/bin/env bash

function abcli_install_roofAI() {
    pip3 install kaggle
    pip3 install torch
    pip3 install -U albumentations[imgaug]
    pip3 install segmentation_models_pytorch
}

abcli_install_module roofAI 103
