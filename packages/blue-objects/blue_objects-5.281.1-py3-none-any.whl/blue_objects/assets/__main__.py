import argparse

from blueness import module
from blueness.argparse.generic import sys_exit

from blue_objects import NAME
from blue_objects.assets.functions import publish
from blue_objects.logger import logger

NAME = module.name(__file__, NAME)

parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    help="publish",
)
parser.add_argument(
    "--arg",
    type=bool,
    default=0,
    help="0|1",
)
parser.add_argument(
    "--object_name",
    type=str,
)
parser.add_argument(
    "--extensions",
    type=str,
    default="png+geojson",
    help="png+geojson",
)
args = parser.parse_args()

success = False
if args.task == "publish":
    success = publish(
        object_name=args.object_name,
        list_of_extensions=args.extensions.split("+"),
    )
else:
    success = None

sys_exit(logger, NAME, args.task, success)
