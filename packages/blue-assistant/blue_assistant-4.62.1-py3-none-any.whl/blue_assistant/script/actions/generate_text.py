from typing import Dict, Tuple
from openai import OpenAI

from blueness import module
from blue_objects import file
from openai_commands.env import OPENAI_API_KEY

from blue_assistant import NAME
from blue_assistant.env import BLUE_ASSISTANT_DEFAULT_MODEL, BLUE_ASSISTANT_MAX_TOKEN
from blue_assistant.script.actions.generic import GenericAction
from blue_assistant.logger import logger

NAME = module.name(__file__, NAME)


class GenerateTextAction(GenericAction):
    name = file.name(__file__)

    def perform(
        self,
        node_name: str,
    ) -> Tuple[bool, Dict]:
        metadata = {}

        if not OPENAI_API_KEY:
            logger.error("OPENAI_API_KEY is not set.")
            return False, {}

        success, generic_metadata = super().perform(node_name=node_name)
        if not success:
            return success, generic_metadata

        client = OpenAI(api_key=OPENAI_API_KEY)

        try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": self.script.nodes[node_name]["prompt"],
                            }
                        ],
                    }
                ],
                model=BLUE_ASSISTANT_DEFAULT_MODEL,
                max_tokens=BLUE_ASSISTANT_MAX_TOKEN,
            )
        except Exception as e:
            logger.error(str(e))
            return False, {"error": str(e)}

        if self.script.verbose:
            logger.info("response: {}".format(response))

        if not response.choices:
            logger.error("no choice.")
            return False, {}

        metadata["reply"] = response.choices[0].message.content
        logger.info("🗣️ reply: {}".format(metadata["reply"]))

        metadata.update(generic_metadata)
        return True, metadata
