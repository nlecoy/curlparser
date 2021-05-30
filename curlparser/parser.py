import argparse
import json
import shlex

from collections import OrderedDict, namedtuple
from urllib.parse import urlparse


ParsedCommand = namedtuple(
    "ParsedCommand",
    [
        "method",
        "url",
        "auth",
        "cookies",
        "data",
        "json",
        "header",
        "verify",
    ],
)

parser = argparse.ArgumentParser()

parser.add_argument("command")
parser.add_argument("url")
parser.add_argument("-A", "--user-agent")
parser.add_argument("-I", "--head")
parser.add_argument("-H", "--header", action="append", default=[])
parser.add_argument("-b", "--cookie", action="append", default=[])
parser.add_argument("-d", "--data", "--data-ascii", "--data-binary", "--data-raw", default=None)
parser.add_argument("-k", "--insecure", action="store_false")
parser.add_argument("-u", "--user", default=())
parser.add_argument("-X", "--request", default="")


def is_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def parse(curl_command: str) -> ParsedCommand:
    cookies = OrderedDict()
    header = OrderedDict()
    body = None
    method = "GET"

    curl_command = curl_command.replace("\\\n", " ")

    tokens = shlex.split(curl_command)
    parsed_args = parser.parse_args(tokens)

    if parsed_args.command != "curl":
        raise ValueError("Not a valid cURL command")

    if not is_url(parsed_args.url):
        raise ValueError("Not a valid URL for cURL command")

    data = parsed_args.data
    if data:
        method = "POST"

    if data:
        try:
            body = json.loads(data)
        except json.JSONDecodeError:
            header["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            header["Content-Type"] = "application/json"

    if parsed_args.request:
        method = parsed_args.request

    for arg in parsed_args.cookie:
        try:
            key, value = arg.split("=", 1)
        except ValueError:
            pass
        else:
            cookies[key] = value

    for arg in parsed_args.header:
        try:
            key, value = arg.split(":", 1)
        except ValueError:
            pass
        else:
            header[key] = value

    user = parsed_args.user
    if user:
        user = tuple(user.split(":"))

    return ParsedCommand(
        method=method,
        url=parsed_args.url,
        auth=user,
        cookies=cookies,
        data=data,
        json=body,
        header=header,
        verify=parsed_args.insecure,
    )
