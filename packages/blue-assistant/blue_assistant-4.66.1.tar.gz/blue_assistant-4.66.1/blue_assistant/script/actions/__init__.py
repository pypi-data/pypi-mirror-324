from typing import List

from blue_assistant.script.actions.generic import GenericAction
from blue_assistant.script.actions.generate_image import GenerateImageAction
from blue_assistant.script.actions.generate_text import GenerateTextAction
from blue_assistant.script.actions.wip import WorkInProgressAction
from blue_assistant.logger import logger

list_of_actions: List[GenericAction] = [
    GenericAction,
    GenerateImageAction,
    GenerateTextAction,
    WorkInProgressAction,
]
