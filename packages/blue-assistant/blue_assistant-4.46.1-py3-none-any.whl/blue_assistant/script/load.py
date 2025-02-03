from typing import Tuple

from blue_assistant.script.repository import list_of_script_classes
from blue_assistant.script.repository.generic import GenericScript
from blue_assistant.logger import logger


def load_script(
    script_name: str,
    verbose: bool = False,
) -> Tuple[bool, GenericScript]:
    for script_class in list_of_script_classes:
        if script_class.name == script_name:
            return True, script_class(verbose=verbose)

    logger.error(f"{script_name}: script not found.")
    return False, GenericScript(verbose=verbose)
