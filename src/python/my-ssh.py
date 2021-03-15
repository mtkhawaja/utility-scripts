from ast import parse
import sys, argparse
from subprocess import run
from decouple import config
from json import loads


def get_selected_host_ip(host_list, selection):
    return host_list[list(host_list.keys())[selection-1]]
     
def print_host_selection_menu(hosts):
    index = 1
    for host in hosts: 
        print(f'{index}. {host:<12} {hosts[host]:>12}')
        index += 1
    return

def ssh(pk_path, username, ip):
    run(['ssh', '-i', pk_path, f'{username}@{ip}'])
    

def main(args):
    hosts = run(['python.exe', 'get-ip-list.py', '-d'], capture_output=True, encoding='utf-8')
    host_list = loads(hosts.stdout)
    print_host_selection_menu(host_list)
    selection = int(input("Please Select by Index: "))
    selected_host_ip = get_selected_host_ip(host_list, selection)
    ssh(args.private_key, args.username, selected_host_ip)

KEY_PATH = config('MY_SSH_DEFAULT_KEY_PATH')
USERNAME = config('MY_SSH_DEFAULT_USERNAME')

parser = argparse.ArgumentParser()
parser.add_argument('-u','--username', help='Username for SSH session.', default=USERNAME)
parser.add_argument('-pk','--private_key', help='Path to private key.', default=KEY_PATH)
parser.set_defaults(func=main)
args = parser.parse_args()
args.func(args)

sys.exit(0)