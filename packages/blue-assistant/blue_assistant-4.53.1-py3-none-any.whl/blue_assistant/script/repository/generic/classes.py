from typing import Dict, List
import os
from tqdm import tqdm


from blueness import module
from blue_objects import file, path
from blue_objects.metadata import post_to_object

from blue_assistant import NAME
from blue_assistant.script.actions import perform_action
from blue_assistant.logger import logger


NAME = module.name(__file__, NAME)


class GenericScript:
    name = path.name(file.path(__file__))

    def __init__(
        self,
        verbose: bool = False,
    ):
        self.verbose = verbose

        metadata_filename = os.path.join(
            file.path(__file__),
            f"../{self.name}",
            "metadata.yaml",
        )
        self.metadata: Dict
        success, self.metadata = file.load_yaml(metadata_filename)
        assert success, f"cannot load {self.name}/metadata.yaml"

        logger.info("loaded {} node(s)".format(len(self.nodes)))

        logger.info("loaded {} variable(s)".format(len(self.vars)))
        if verbose:
            for var_name, var_value in self.vars.items():
                logger.info("{}: {}".format(var_name, var_value))

    @property
    def script(self) -> str:
        return self.metadata.get("script", {})

    @property
    def nodes(self) -> str:
        return self.metadata.get("script", {}).get("nodes", [])

    @property
    def vars(self) -> str:
        return self.metadata.get("script", {}).get("vars", {})

    def run(
        self,
        object_name: str,
    ) -> bool:
        logger.info(
            "{}.run: {}:{} -> {}".format(
                NAME,
                self.__class__.__name__,
                self.name,
                object_name,
            )
        )

        if not post_to_object(
            object_name,
            "script",
            self.script,
        ):
            return False

        metadata: Dict[Dict] = {"nodes": {}}
        success: bool = True
        for node_name, node in tqdm(self.nodes.items()):
            logger.info(
                "{}{}".format(
                    node_name,
                    f": {node}" if self.verbose else " ...",
                )
            )

            assert isinstance(node, dict)
            success, output = perform_action(
                action_name=node.get("action", "unknown"),
                node=node,
            )
            metadata["nodes"][node_name] = {
                "success": success,
                "output": output,
            }
            if not success:
                break

        if not post_to_object(
            object_name,
            "output",
            metadata,
        ):
            return False

        return success
