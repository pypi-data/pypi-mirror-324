from blueness import module

from blue_assistant import NAME
from blue_assistant.logger import logger


NAME = module.name(__file__, NAME)


def chat(
    object_name: str,
    interactive: bool = True,
    verbose: bool = False,
) -> bool:
    logger.info(
        "{}.chat -{}> {}".format(
            NAME,
            "interactive-" if interactive else "",
            object_name,
        )
    )

    logger.info("🪄")

    return True
