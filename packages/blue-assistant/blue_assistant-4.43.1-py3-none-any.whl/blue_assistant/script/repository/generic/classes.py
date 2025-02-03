import os

from blueness import module
from blue_objects import file, path
from blue_objects.metadata import post_to_object

from blue_assistant import NAME
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
        success, self.metadata = file.load_yaml(metadata_filename)

        self.script = self.metadata.get("script", [])

        assert success, f"cannot load {self.name}/metadata.yaml"

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

        return post_to_object(
            object_name,
            "input",
            self.script,
        )
