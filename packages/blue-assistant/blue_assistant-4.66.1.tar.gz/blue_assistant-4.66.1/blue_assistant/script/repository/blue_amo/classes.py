from blue_objects import file, path


from blue_assistant.script.repository.generic.classes import GenericScript
from blue_assistant.logger import logger


class BlueAmoScript(GenericScript):
    name = path.name(file.path(__file__))
