from typing import List, Dict, Tuple, Type

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


def get_action_class(
    action_name: str,
) -> Tuple[bool, Type[GenericAction]]:
    for action_class in list_of_actions:
        if action_class.name == action_name:
            return True, action_class

    logger.error(f"{action_name}: action not found.")
    return False, GenericAction


def perform_action(
    action_name: str,
    node: Dict,
) -> Tuple[bool, Dict]:
    success, action_class = get_action_class(action_name=action_name)
    if not success:
        return False, {
            "error": f"{action_name}: action not found.",
        }

    action_object = action_class(node=node)

    return action_object.perform()
