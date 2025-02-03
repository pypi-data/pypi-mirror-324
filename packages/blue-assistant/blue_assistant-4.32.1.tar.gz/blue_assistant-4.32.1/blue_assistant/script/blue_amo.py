from blue_assistant.script.generic import GenericScript
from blue_assistant.script.kinds import ScriptKind


class BlueAmoScript(GenericScript):
    def __init__(
        self,
        object_name: str,
        verbose: bool = False,
        download: bool = False,
    ):
        super().__init__(
            object_name=object_name,
            verbose=verbose,
            download=download,
        )

        self.kind = ScriptKind.BLUE_AMO
