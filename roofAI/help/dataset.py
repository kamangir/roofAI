from typing import List

from blue_options.terminal import show_usage, xtra


def help_ingest(
    tokens: List[str],
    mono: bool,
) -> str:
    options = "".join(
        [
            "source=AIRS",
            xtra(",dryrun,upload,", mono=mono),
            "target=<target>",
        ]
    )

    args = [
        "[--test_count <10>]",
        "[--train_count <10>]",
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
    options = "actions|repo"

    return show_usage(
        [
            "@plugin",
            "browse",
            f"[{options}]",
        ],
        "browse blue_plugin.",
        mono=mono,
    )


help_functions = {
    "ingest": help_ingest,
    "review": help_review,
}
