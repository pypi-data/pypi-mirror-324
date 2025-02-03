import os
from blue_options.env import load_config, load_env

load_env(__name__)
load_config(__name__)


BLUE_ASSISTANT_DEFAULT_MODEL = os.getenv(
    "BLUE_ASSISTANT_DEFAULT_MODEL",
    "",
)

BLUE_ASSISTANT_MAX_TOKEN_str = os.getenv("BLUE_ASSISTANT_MAX_TOKEN", "")
try:
    BLUE_ASSISTANT_MAX_TOKEN = int(BLUE_ASSISTANT_MAX_TOKEN_str)
except Exception:
    BLUE_ASSISTANT_MAX_TOKEN = 2000
