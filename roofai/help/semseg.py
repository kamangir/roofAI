from typing import List

from blue_options.terminal import show_usage, xtra

from roofai.semseg import Profile

list_of_profiles = [profile.name for profile in Profile]

device_and_profile_details = {
    "device: cpu | cuda": [],
    "profile: {}".format(" | ".join(list_of_profiles)): [],
}


def help_predict(
    tokens: List[str],
    mono: bool,
) -> str:
    options = "".join(
        [
            xtra("device=<device>,~download,dryrun,profile=<profile>,", mono=mono),
            "upload",
        ]
    )

    return show_usage(
        [
            "roofai",
            "semseg",
            "predict",
            f"[{options}]",
            "[..|<model-object-name>]",
            "[.|<dataset-object-name>]",
            "[-|<prediction-object-name>]",
        ],
        "semseg[<model-object-name>].predict(<dataset-object-name>) -> <prediction-object-name>.",
        device_and_profile_details,
        mono=mono,
    )


def help_train(
    tokens: List[str],
    mono: bool,
) -> str:
    options = "".join(
        [
            xtra("device=<device>,~download,dryrun,profile=<profile>,", mono=mono),
            "upload",
        ]
    )

    args = [
        "[--activation <sigmoid>]",
        "[--classes <one+two+three+four>]",
        "[--encoder_name <se_resnext50_32x4d>]",
        "[--encoder_weights <imagenet>]",
        "[--epoch_count <-1>]",
    ]

    return show_usage(
        [
            "roofai",
            "semseg",
            "train",
            f"[{options}]",
            "[.|<dataset-object-name>]",
            "[-|<model-object-name>]",
        ]
        + args,
        "semseg.train(<dataset-object-name>) -> <model-object-name>.",
        device_and_profile_details,
        mono=mono,
    )


help_functions = {
    "predict": help_predict,
    "train": help_train,
}
