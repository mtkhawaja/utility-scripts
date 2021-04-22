import sys, argparse
from decouple import config
from requests import post, get


def create_paste(args):
    params = {
        "api_dev_key": args.dev_key,
        "api_user_key": args.user_key,
        "api_option": "paste",
        "api_paste_private": 2,
        "api_paste_name": args.name,
        "api_paste_code": args.paste_content,
    }
    response = post(args.dev_endpoint, params)
    if "Bad API request" in response.text:
        return response.text
    return f"Paste URL:\t{response.text}"


def list_pastes(args):
    params = {
        "api_dev_key": args.dev_key,
        "api_user_key": args.user_key,
        "api_option": "list",
        "api_results_limit": args.limit,
    }
    response = post(args.dev_endpoint, params)
    return f"User Pastes:\n{response.text}"


def delete_paste(args):
    params = {
        "api_dev_key": args.dev_key,
        "api_user_key": args.user_key,
        "api_paste_key": args.paste_key,
        "api_option": "delete",
    }
    response = post(args.dev_endpoint, params)
    return response.text


def get_paste_contents(args):
    params = {
        "api_dev_key": args.dev_key,
        "api_user_key": args.user_key,
        "api_paste_key": args.paste_key,
        "api_option": "show_paste",
    }
    response = post(args.raw_endpoint, params)
    return response.text


def update_config(api_user_key, path):
    # TODO: cache api_user_key
    pass


def request_api_user_key(API_DEV_KEY):
    LOGIN_ENDPOINT = config("PASTEBIN_LOGIN_ENDPOINT")
    post_params = {
        "api_dev_key": API_DEV_KEY,
        "api_user_name": config("PASTEBIN_USERNAME"),
        "api_user_password": config("PASTEBIN_PASSWORD"),
    }
    response = post(LOGIN_ENDPOINT, post_params)
    return response.text


# Config
API_DEV_KEY = config("PASTEBIN_API_DEV_KEY")
API_USER_KEY = request_api_user_key(API_DEV_KEY)
DEV_ENDPOINT = config("PASTEBIN_DEV_ENDPOINT")
RAW_ENDPOINT = config("PASTEBIN_RAW_PASTE_ENDPOINT")

# top-level parser
parser = argparse.ArgumentParser(prog="pastebin")
parser.add_argument(
    "-dk", "--dev_key", help="API Dev Key for Pastebin", default=API_DEV_KEY
)
parser.add_argument(
    "-uk", "--user_key", help="User Key for Pastebin", default=API_USER_KEY
)
parser.add_argument(
    "-de", "--dev_endpoint", help="Request endpoint.", default=DEV_ENDPOINT
)
parser.add_argument(
    "-re", "--raw_endpoint", help="Raw paste endpoint.", default=RAW_ENDPOINT
)
subparsers = parser.add_subparsers(help="sub-command help.")

# parser for create command.
create_paste_parser = subparsers.add_parser("create", help="create paste help")
create_paste_parser.add_argument("-n", "--name", help="Paste name.", type=str)
create_paste_parser.add_argument(
    "-pc", "--paste_content", help="Paste contents", type=str
)
create_paste_parser.set_defaults(func=create_paste)

# parser for list command.
list_paste_parser = subparsers.add_parser("list", help="list paste help")
list_paste_parser.add_argument(
    "-l", "--limit", help="Define the count of pastes to view.", default=50
)
list_paste_parser.set_defaults(func=list_pastes)

# parser for delete command
delete_paste_parser = subparsers.add_parser("delete", help="delete paste help")
delete_paste_parser.add_argument(
    "-pk", "--paste_key", help="Paste key for paste to be deleted."
)
delete_paste_parser.set_defaults(func=delete_paste)

# parser for get command
get_paste_parser = subparsers.add_parser("get", help="get paste help")
get_paste_parser.add_argument(
    "-pk", "--paste_key", help="Paste key for paste to be viewed."
)
get_paste_parser.set_defaults(func=get_paste_contents)

# parse args and call appropriate function
args = parser.parse_args()
result = args.func(args)

print(result)

sys.exit(0)