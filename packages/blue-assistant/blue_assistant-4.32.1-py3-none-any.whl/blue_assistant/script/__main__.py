import argparse

from blueness import module
from blueness.argparse.generic import sys_exit

from blue_assistant import NAME
from blue_assistant.script.functions import load_script
from blue_assistant.logger import logger

NAME = module.name(__file__, NAME)

parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    help="run",
)
parser.add_argument(
    "--object_name",
    type=str,
)
parser.add_argument(
    "--verbose",
    type=int,
    default=0,
    help="0 | 1",
)
args = parser.parse_args()

success = False
if args.task == "run":
    success, script = load_script(
        object_name=args.object_name,
        verbose=args.verbose == 1,
    )

    if success:
        success = script.run()
else:
    success = None

sys_exit(logger, NAME, args.task, success)
