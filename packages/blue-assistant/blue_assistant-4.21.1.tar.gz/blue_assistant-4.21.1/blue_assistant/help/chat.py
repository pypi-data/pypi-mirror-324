from typing import List

from blue_options.terminal import show_usage, xtra


def help_chat(
    tokens: List[str],
    mono: bool,
) -> str:
    options = xtra("download,dryrun,~upload", mono=mono)

    chat_options = xtra("~interact", mono=mono)

    args = ["--verbose 1"]

    return show_usage(
        [
            "@assistant",
            "chat",
            f"[{options}]",
            f"[{chat_options}]",
            "[-|<object-name>]",
        ]
        + args,
        "chat with @assistant.",
        mono=mono,
    )
