from typing import List

from blue_options.terminal import show_usage, xtra


def help_run(
    tokens: List[str],
    mono: bool,
) -> str:
    options = xtra("~download,dryrun,~upload", mono=mono)

    args = ["--verbose 1"]

    return show_usage(
        [
            "@assistant",
            "script",
            "run",
            f"[{options}]",
            "[.|<object-name>]",
        ]
        + args,
        "run <object-name>.",
        mono=mono,
    )


help_functions = {"run": help_run}
