from argparse import ArgumentParser
from sys import exit
from os import path
import webbrowser 

def main(args):
    if not path.exists(args.file_path):
        print('File does not exist!')
        return -1

    with open(args.file_path) as url_file:
        for url in url_file.readlines():
            webbrowser.open(url)
    return 0


parser = ArgumentParser()
parser.add_argument('-f', '--file_path', required = True, help = 'Path to file with links', type=str)
parser.set_defaults(func=main)
args = parser.parse_args()
return_code = args.func(args) 

exit(return_code)