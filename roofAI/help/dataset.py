from typing import List

from blue_options.terminal import show_usage, xtra


def help_ingest(
    tokens: List[str],
    mono: bool,
) -> str:
    options = "".join(
        [
            "source=AIRS",
            xtra(",dryrun,upload,target=<target>", mono=mono),
        ]
    )

    args = [
        "[--test_count <10>]",
        "[--train_count <80>]",
        "[--val_count <10>]",
    ]

    usage_1 = show_usage(
        [
            "roofAI",
            "dataset",
            "ingest",
            f"[{options}]",
            "[-|<object-name>]",
        ]
        + args,
        "ingest AIRS -> <object-name>.",
        {
            "target: sagemaker | torch": [],
        },
        mono=mono,
    )

    # ---

    options = "".join(
        [
            "source=CamVid",
            xtra(",dryrun,upload", mono=mono),
        ]
    )

    usage_2 = show_usage(
        [
            "roofAI",
            "dataset",
            "ingest",
            f"[{options}]",
            "[-|<object-name>]",
        ],
        "ingest CamVid -> <object-name>.",
        mono=mono,
    )

    # ---

    return "\n".join(
        [
            usage_1,
            usage_2,
        ]
    )


def help_review(
    tokens: List[str],
    mono: bool,
) -> str:
    options = "".join(
        [
            "download",
            xtra(",dryrun", mono=mono),
        ]
    )

    args = [
        "[--count <1>]",
        "[--index <index>]",
        "[--subset <subset>]",
    ]

    return show_usage(
        [
            "roofAI",
            "dataset",
            "review",
            f"[{options}]",
            "[.|<object-name>]",
        ]
        + args,
        "review <object-name>.",
        mono=mono,
    )


help_functions = {
    "ingest": help_ingest,
    "review": help_review,
}
