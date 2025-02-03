from typing import Dict
from tqdm import tqdm

from blue_objects import file, path

from blue_assistant.script.repository.generic.classes import GenericScript


class MiningOnMoonScript(GenericScript):
    name = path.name(file.path(__file__))

    def __init__(
        self,
        verbose: bool = False,
    ):
        super().__init__(verbose=verbose)
