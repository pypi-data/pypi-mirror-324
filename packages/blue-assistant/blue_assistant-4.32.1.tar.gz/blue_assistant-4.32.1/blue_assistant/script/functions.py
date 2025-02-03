from typing import Tuple, Union, Type

from blueness import module
from blue_objects.metadata import get_from_object

from blue_assistant import NAME
from blue_assistant.script.generic import GenericScript
from blue_assistant.script.blue_amo import BlueAmoScript
from blue_assistant.logger import logger


NAME = module.name(__file__, NAME)


def load_script(
    object_name: str,
    verbose: bool = False,
    download: bool = False,
) -> Tuple[bool, Union[GenericScript, None]]:
    script_kind = get_from_object(
        object_name=object_name,
        key="script.kind",
        default="generic",
    )

    script_class: Type[GenericScript] = GenericScript
    if script_kind == "blue_amo":
        script_class = BlueAmoScript
    if verbose:
        logger.info(f"script class: {script_class.__name__}")

    script = script_class(
        object_name=object_name,
        verbose=verbose,
        download=download,
    )
    if verbose:
        logger.info(f"script kind: {script.kind}")

    return True, script
