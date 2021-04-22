import argparse, sys
from math import floor, ceil
from pyperclip import copy

# Default Config
LINE_LENGTH = 100
GROWTH_CONSTRAINT = lambda x: floor(x - 0.30 * x)
GROWTH_FACTOR = 1.05


def generate_opening_line(opening_token, style_char, line_length):
    return f"{opening_token}{style_char * (line_length - len(opening_token))}"


def generate_body_line(body, style_char, line_length):
    SPACE = " "
    body = f"{SPACE}{body}{SPACE}"
    line = style_char * line_length
    replacement_point = floor((line_length / 2)) - floor(len(body) / 2)
    return f"{SPACE}{line[1:replacement_point]}{body}{line[(replacement_point+len(body)):]}"


def generate_closing_line(closing_token, style_char, line_length):
    SPACE = " "
    return f"{SPACE}{style_char * (line_length - len(closing_token))}{closing_token}"


def generate_comment(body, style_char, opening_token, closing_token, line_length):
    opening_line = generate_opening_line(opening_token, style_char, line_length)
    body_line = generate_body_line(body, style_char, line_length)
    closing_line = generate_closing_line(closing_token, style_char, line_length)
    return f"{opening_line}\n{body_line}\n{closing_line}"


# Prase arguments and set defaults if applicable.
parser = argparse.ArgumentParser()
parser.add_argument("body", help="Comment Body", type=str)
parser.add_argument(
    "-o",
    "--opening",
    help="Opening Comment Token. For example: /* , #, ''' etc.",
    type=str,
)
parser.add_argument(
    "-c",
    "--closing",
    help="Closing Comment Token. For example: */, #, ''' etc.",
    type=str,
)
parser.add_argument(
    "-s",
    "--style",
    help="Comment Style Character. For example: *, |, #, = etc.",
    type=str,
)
parser.add_argument(
    "-d",
    "--display",
    help="Set flag to see comment copied to clipboard in command line.",
    action="store_true",
)
parser.add_argument(
    "-nd",
    "--no_display",
    help="Set flag to hide all messages in command line.",
    action="store_true",
)

args = parser.parse_args()


# Initialize Comment Parameters
body = args.body
style_char = args.style if args.style else "*"
opening_token = args.opening if args.opening else "/*"
closing_token = args.closing if args.closing else "*/"

# Adjust defaults based on body length
if len(body) > GROWTH_CONSTRAINT(LINE_LENGTH):
    while len(body) > GROWTH_CONSTRAINT(LINE_LENGTH):
        LINE_LENGTH = floor(GROWTH_FACTOR * LINE_LENGTH)

# Generate Comment
comment = generate_comment(body, style_char, opening_token, closing_token, LINE_LENGTH)

# Copy Comment to Clipboard

copy(comment)

if not args.no_display:
    print("Comment Copied to Clipboard!")

if args.display:
    print(comment)


sys.exit(0)