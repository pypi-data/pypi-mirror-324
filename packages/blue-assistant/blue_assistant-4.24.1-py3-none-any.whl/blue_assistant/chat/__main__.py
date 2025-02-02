import argparse

from blueness import module
from blueness.argparse.generic import sys_exit

from blue_assistant import NAME
from blue_assistant.chat.functions import chat
from blue_assistant.logger import logger

NAME = module.name(__file__, NAME)

parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    help="chat",
)
parser.add_argument(
    "--object_name",
    type=str,
)
parser.add_argument(
    "--interactive",
    type=int,
    default=0,
    help="0 | 1",
)
parser.add_argument(
    "--verbose",
    type=int,
    default=0,
    help="0 | 1",
)
args = parser.parse_args()

success = False
if args.task == "chat":
    success = chat(
        object_name=args.object_name,
        interactive=args.interactive == 1,
        verbose=args.verbose == 1,
    )
else:
    success = None

sys_exit(logger, NAME, args.task, success)
