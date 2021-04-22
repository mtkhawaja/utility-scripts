from argparse import ArgumentParser
import argparse
from os import mkdir, makedirs
from os.path import join

parser = ArgumentParser()


def create_static_dir(args):
    parent_dir_path = args.target_path
    dir = f"static/{args.app_name}"
    dir_path = join(parent_dir_path, dir)
    makedirs(dir_path)
    subfolder_level_one = ["scripts/js/", "styles/css/"]
    for subfolders in subfolder_level_one:
        path = join(dir_path, subfolders)
        makedirs(path)
    return 0


parser.add_argument(
    "-t", "--target_path", default="./", help="Target Destination for Static Directory"
)
parser.add_argument(
    "-a",
    "--app_name",
    required=True,
    help="Name of the application for the static directory.",
)
parser.set_defaults(func=create_static_dir)
args = parser.parse_args()
args.func(args)
