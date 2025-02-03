from typing import Dict
from tqdm import tqdm

from blue_objects import file, path
from blue_objects.metadata import post_to_object

from blue_assistant.script.repository.generic.classes import GenericScript
from blue_assistant.logger import logger


class BlueAmoScript(GenericScript):
    name = path.name(file.path(__file__))

    def __init__(
        self,
        verbose: bool = False,
    ):
        super().__init__(verbose=verbose)

    def run(
        self,
        object_name: str,
    ) -> bool:
        if not super().run(object_name=object_name):
            return False

        metadata: Dict[Dict] = {"nodes": {}}
        for node_name, node in tqdm(self.nodes.items()):
            logger.info(
                "{}{}".format(
                    node_name,
                    f": {node}" if self.verbose else " ...",
                )
            )

            metadata["nodes"][node_name] = "..."

        return post_to_object(
            object_name,
            "output",
            metadata,
        )
