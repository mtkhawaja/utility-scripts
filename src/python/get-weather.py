import argparse, sys
from decouple import config
from requests import get
from datetime import datetime

API_KEY = config("WEATHER_API_KEY")
API_ENDPOINT = config("WEATHER_API_ENDPOINT")


def validate_args(args):
    if args.country_code:
        code_len = len(args.country_code)
        if code_len > 2 or code_len == 0:
            raise ValueError(
                "Country code must be two chracters long! e.g. US, UK etc."
            )
    return True


parser = argparse.ArgumentParser()
parser.add_argument("-z", "--zip", help="Zip Code eg. 20041", type=str)
parser.add_argument("-c", "--city", help="City. e.g. London", type=str)
parser.add_argument("-cc", "--country_code", help="Two digit country code.", type=str)
parser.add_argument(
    "-i",
    "--imperial",
    help="Imperial System of measurement. Metric is default",
    action="store_true",
)
args = parser.parse_args()

validate_args(args)
units = "imperial" if args.imperial else config("WEATHER_UNITS")
country_code = (
    args.country_code if args.country_code else config("WEATHER_COUNTRY_CODE")
)

request_type = ""
req_param = ""

if args.city:
    request_type = "q"
    req_param = args.city if args.city else config("WEATHER_CITY")
else:
    request_type = "zip"
    req_param = args.zip if args.zip else config("WEATHER_ZIP")


request_url = f"{API_ENDPOINT}/data/2.5/weather?{request_type}={req_param},{country_code}&appid={API_KEY}&units={units}"
print(request_url)
response = get(request_url).json()


date = datetime.now().strftime("%H:%M:%S %Y-%m-%d (System)")
temp = f"{response['main']['temp']}{'f' if args.imperial else 'c'}"
region = response["name"]

print(f"{date} {region:>10} {temp:>12}")

sys.exit(0)