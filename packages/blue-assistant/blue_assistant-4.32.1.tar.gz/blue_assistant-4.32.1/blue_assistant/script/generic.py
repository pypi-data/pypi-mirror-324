from blueness import module
from blue_objects.metadata import get_from_object

from blue_assistant import NAME
from blue_assistant.script.kinds import ScriptKind
from blue_assistant.logger import logger


NAME = module.name(__file__, NAME)


class GenericScript:
    def __init__(
        self,
        object_name: str,
        verbose: bool = False,
        download: bool = False,
    ):
        self.verbose = verbose

        self.object_name = object_name

        self.kind = ScriptKind.GENERIC

        self.script = get_from_object(
            object_name=object_name,
            key="script",
            default={},
            download=download,
        )

    def run(self) -> bool:
        logger.info(
            "{}.run({} @ {})".format(
                NAME,
                self.__class__.__name__,
                self.object_name,
            )
        )

        return True
