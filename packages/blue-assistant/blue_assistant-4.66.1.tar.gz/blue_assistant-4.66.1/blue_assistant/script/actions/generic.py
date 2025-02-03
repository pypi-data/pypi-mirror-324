from typing import Dict, Tuple

from blueness import module
from blue_objects import file

from blue_assistant import NAME
from blue_assistant.script.repository.base.classes import BaseScript
from blue_assistant.logger import logger

NAME = module.name(__file__, NAME)


class GenericAction:
    name = file.name(__file__)

    def __init__(
        self,
        script: BaseScript,
    ):
        self.script = script

    def perform(
        self,
        node_name: str,
    ) -> bool:
        logger.info(
            "{}.perform({}) on {}.{} ...".format(
                NAME,
                self.__class__.__name__,
                self.script.name,
                node_name,
            ),
        )
        return True
