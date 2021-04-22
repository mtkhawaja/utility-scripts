from argparse import ArgumentParser
from sys import exit
from string import Template
from os import error, path
from decouple import config


def read_source(source_path):
    source_text = ""
    if not path.exists(source_path):
        raise FileNotFoundError("Source File Not found")
    with open(source_path, "r") as source_file:
        source_text = Template(source_file.read())
    return source_text


def write_to_target(target_path, target_text):
    DEFAULT_FILE_NAME = "README.md"
    if path.isdir(target_path):
        target_path = "".join([target_path, DEFAULT_FILE_NAME])
    with open(target_path, "w") as target_file:
        target_file.write(target_text)


def main(args):
    tag_dict = {
        "project_title": args.project_title,
    }
    try:
        source_text = read_source(args.source_path)
        target_text = source_text.substitute(tag_dict)
        write_to_target(args.target_path, target_text)
    except FileNotFoundError as err:
        print(f"Runtime Error: {err}")
        return -1
    return 0


source_template_path = config("README_TEMPLATE_PATH")
parser = ArgumentParser()
parser.add_argument(
    "-t",
    "--target_path",
    default="./README.md",
    help="The path where the README.md will be saved.",
)
parser.add_argument(
    "-s", "--source_path", default=source_template_path, help="Path to template file."
)
parser.add_argument(
    "-p", "--project_title", default="Your Project Name", help="Name of the Project."
)
parser.add_argument(
    "-nd",
    "--no_display",
    help="Set flag to hide all messages in command line.",
    action="store_true",
)

parser.set_defaults(func=main)
parser.parse_args()
args = parser.parse_args()

return_code = args.func(args)

if not args.no_display:
    msg = ""
    if return_code == 0:
        msg = f"README.md successfully created:\t{args.target_path}"
    else:
        msg = f"Unable to create README.md\nSource Path:\t{args.source_path}\nTarget Path:\t{args.target_path}"
    print(msg)

exit(return_code)