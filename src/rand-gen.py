import argparse, sys
from decouple import config
from requests import get
from jsonrpcclient import request

API_KEY = config('RANDOM_API_KEY')
API_ENDPOINT = config('BASIC_RANDOM_API_ENDPOINT')
method = 'generateIntegers'


def flip():
    response = request(API_ENDPOINT, method,  apiKey=API_KEY, n=1, min=1, max=100 , request_id='')
    rand_num = response.data.result['random']['data'][0]
    outcome = 'heads' if rand_num <= 50 else 'tails' 
    return outcome

def multi_flip(flip_count):
    response = request(API_ENDPOINT, method,  apiKey=API_KEY, n=flip_count, min=1, max=100 , request_id='')
    rand_set = response.data.result['random']['data']
    outcomes = {'heads':0, 'tails': 0}
    for rand_num in rand_set:
        flip_result = 'heads' if rand_num <= 50 else 'tails'
        outcomes[flip_result] += 1
    return f'Flips: {flip_count:}\tHeads: {outcomes["heads"]}\tTails: {outcomes["tails"]}'

def get_rand(minimum,maximum):    
    response = request(API_ENDPOINT, method,  apiKey=API_KEY, n=1, min=minimum, max=maximum , request_id='')
    return response.data.result['random']['data'][0]

def get_rand_set(cardinality, minimum,maximum):
    response = request(API_ENDPOINT, method,  apiKey=API_KEY, n=cardinality, min=1, max=100 , request_id='', replacement=False)
    return response.data.result['random']['data']

parser = argparse.ArgumentParser()
parser.add_argument('-gt', '--greater_than', help='Lower bound for random number.', type=int)
parser.add_argument('-lt', '--less_than', help='Upper bound for random number', type=int)
parser.add_argument('-mf', '--multi_flip', help='Number of times to flip', type=int)
parser.add_argument('-rs', '--random_set', help='Generate a set of random numbers.', type=int)
parser.add_argument('-f', '--flip', help='Flip a coin', action='store_true')
args = parser.parse_args()

minimum = args.greater_than if args.greater_than else 1
maximum = args.less_than if args.less_than else 10000
result = ''

if args.flip:
    result = flip()
elif args.multi_flip:
    result = multi_flip(args.multi_flip)
elif args.random_set:
    result = get_rand_set(args.random_set,minimum,maximum)
else:
    result = get_rand(minimum,maximum)

print(result)

sys.exit(0)