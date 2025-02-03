import os
from blue_options.env import load_config, load_env

load_env(__name__)
load_config(__name__)


BLUE_ASSISTANT_TEST_OBJECT = os.getenv(
    "BLUE_ASSISTANT_TEST_OBJECT",
    "",
)
