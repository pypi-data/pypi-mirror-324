from blue_objects import file

from blue_assistant.script.actions.generic import GenericAction


class WorkInProgressAction(GenericAction):
    name = file.name(__file__)
