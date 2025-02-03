from typing import Dict, Tuple

from blue_objects import file

from blue_assistant.script.actions.generic import GenericAction
from blue_assistant.logger import logger


class GenerateImageAction(GenericAction):
    name = file.name(__file__)

    def perform(self) -> Tuple[bool, Dict]:
        success, generic_metadata = super().perform()
        if not success:
            return success, generic_metadata

        logger.info(f"🪄 generating image ...: {self.node}")
        metadata = {}

        metadata.update(generic_metadata)
        return True, metadata
