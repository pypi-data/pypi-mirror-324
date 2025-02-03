from typing import Dict, Tuple

from blueness import module
from blue_objects import file

from blue_assistant import NAME
from blue_assistant.logger import logger

NAME = module.name(__file__, NAME)


class GenericAction:
    name = file.name(__file__)

    def __init__(self, node: Dict):
        self.node = node

    def perform(self) -> Tuple[bool, Dict]:
        logger.info(
            "{}.perform({}) ...".format(
                NAME,
                self.__class__.__name__,
            ),
        )
        return True, {}
