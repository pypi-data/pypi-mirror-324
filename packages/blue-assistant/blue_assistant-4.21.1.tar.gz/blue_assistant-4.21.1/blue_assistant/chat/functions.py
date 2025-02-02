from blueness import module

from blue_assistant import NAME
from blue_assistant.chat.context import ChatContext
from blue_assistant.logger import logger


NAME = module.name(__file__, NAME)


def chat(
    object_name: str,
    interactive: bool = True,
    verbose: bool = False,
    load_history: bool = True,
) -> bool:
    logger.info(
        "{}.chat -{}> {}".format(
            NAME,
            "interactive-" if interactive else "",
            object_name,
        )
    )

    context = ChatContext(
        object_name,
        load_history=load_history,
        verbose=verbose,
    )

    if not context.chat(
        interactive=interactive,
    ):
        return False

    return context.save()
