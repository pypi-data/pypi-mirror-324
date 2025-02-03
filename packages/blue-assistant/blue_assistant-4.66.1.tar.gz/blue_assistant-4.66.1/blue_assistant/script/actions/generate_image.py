from typing import Dict, Tuple

from blue_objects import file

from blue_assistant.script.actions.generic import GenericAction
from blue_assistant.logger import logger


class GenerateImageAction(GenericAction):
    name = file.name(__file__)

    def perform(
        self,
        node_name: str,
    ) -> bool:
        if not super().perform(node_name=node_name):
            return False

        logger.info(f"🪄 generating image ...: {node_name}")

        return True
