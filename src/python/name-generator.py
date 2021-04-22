from __future__ import annotations
import argparse
from sys import exit
from datetime import datetime
from hashlib import sha512


class NameGenerator:
    @classmethod
    def generate_name(
        cls: NameGenerator,
        custom_name: str = "",
        rand_str_len: int = 10,
        custom_extension: str = "txt",
        no_date: bool = False,
        no_hex: bool = False,
        no_ext: bool = False,
    ):
        generated_name = []
        current_dt = datetime.now()
        if not no_date:
            generated_name.append(cls._time_stamp(current_dt))
        if custom_name:
            generated_name.append(custom_name)
        if not no_hex:
            generated_name.append(cls._hash_symbols(rand_str_len, current_dt))
        extension = "" if no_ext else f".{custom_extension}"
        return f"{'-'.join(generated_name)}{extension}"

    @staticmethod
    def _hash_symbols(rand_str_len: int, current_dt: datetime) -> str:
        return sha512(current_dt.ctime().encode("utf-8")).hexdigest()[:rand_str_len]

    @staticmethod
    def _time_stamp(current_dt: datetime) -> str:
        return current_dt.strftime("%Y_%m_%d-%H%M%S")


def configure_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-n",
        "--name",
        help="Add name after date in generated name.",
        type=str,
    )
    parser.add_argument(
        "-e",
        "--extension",
        help="File extension. The default extension is '.txt'",
        type=str,
        default="txt",
    )
    parser.add_argument(
        "-d",
        "--digit_count",
        help="""The number of random digits to include.
                The digit count can be between 1 and 128.
                By default, 10 digits are used.""",
        type=int,
        default=10,
    )
    parser.add_argument(
        "-nd",
        "--no_date",
        help="Omit timestamp.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-nh",
        "--no_hex",
        help="Omit hex digits.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-ne",
        "--no_extension",
        help="Omit extension.",
        action="store_true",
        default=False,
    )


def process_args(args: argparse.Namespace) -> str:
    if args.digit_count > 128 or args.digit_count <= 0:
        raise ValueError("Digit Count must be a positive integer less than 128")
    return NameGenerator.generate_name(
        custom_name=args.name,
        rand_str_len=args.digit_count,
        custom_extension=args.extension,
        no_date=args.no_date,
        no_hex=args.no_hex,
        no_ext=args.no_extension,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    configure_parser(parser)
    args = parser.parse_args()
    print(process_args(args))
    exit(0)