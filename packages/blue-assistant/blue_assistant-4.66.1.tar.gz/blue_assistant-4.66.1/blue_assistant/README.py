import os

from blue_objects import file, README

from blue_assistant import NAME, VERSION, ICON, REPO_NAME


items = [
    "{}[`{}`](#) [![image]({})](#) {}".format(
        ICON,
        f"feature {index}",
        "https://github.com/kamangir/assets/raw/main/blue-assistant/marquee.png?raw=true",
        f"description of feature {index} ...",
    )
    for index in range(1, 4)
]


def build():
    return all(
        README.build(
            items=readme.get("items", []),
            path=os.path.join(file.path(__file__), readme["path"]),
            ICON=ICON,
            NAME=NAME,
            VERSION=VERSION,
            REPO_NAME=REPO_NAME,
        )
        for readme in [
            {"items": items, "path": ".."},
            {"path": "docs/blue-amo-01.md"},
        ]
    )
