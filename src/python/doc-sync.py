import argparse, sys
import re
from os import path, getcwd
from decouple import config


# Initialize Paths.
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--source", help="Path to source config document.")
parser.add_argument(
    "-t",
    "--target",
    help="Path to target document. A new document will be created if the target document does not exist",
)
args = parser.parse_args()
src_path = args.source if args.source else config("DOC_SYNC_SRC")
tgt_path = args.target if args.target else config("DOC_SYNC_TGT")


try:
    if not path.exists(src_path):
        raise FileNotFoundError()
except FileNotFoundError:
    print(
        "FileNotFoundError: Path to specified source file invalid or source file does not exist!"
    )
    print(f"Current Working Directory: {getcwd()}")
    print(f"Source File Path provided: {src_path}")
    print(f"Target File Path provided: {tgt_path}")
    sys.exit(1)

src_file = open(src_path, "r")
tgt_file = open(tgt_path, "w")

# Regex Explanation: https://regex101.com/r/EL93E7/4
reg_ex = "=\s*.*(?=')'"

for line in src_file.readlines():
    stripped_contents = re.sub(reg_ex, "= ''", line)
    tgt_file.write(stripped_contents)


src_file.close()
tgt_file.close()

sys.exit(0)