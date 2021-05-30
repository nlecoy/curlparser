from collections import OrderedDict
from unittest import mock

import pytest

from curlparser.parser import ParsedCommand, is_url, parse


@pytest.mark.parametrize(
    "address, result",
    [
        ("http://", False),
        ("https://api.github.com", True),
        ("https://api.github.com/repos/nlecoy/curlparser", True),
        ("http://localhost:8000", True),
        ("http://.www.foo.bar./", True),
        ("api.github.com", False),
    ],
)
def test_is_url(address, result):
    assert is_url(address) is result


def test_is_url_returns_false_on_exception():
    with mock.patch("curlparser.parser.urlparse", side_effect=ValueError):
        assert is_url("https://api.github.com") is False


def test_parse_raises_on_invalid_command():
    with pytest.raises(ValueError):
        parse("ping https://api.github.com/repos/nlecoy/curlparser")


def test_parse_raises_on_invalid_url():
    with pytest.raises(ValueError):
        parse("curl http://")


@pytest.mark.parametrize(
    "curl_command, result",
    [
        (
            "curl https://api.github.com/repos/nlecoy/curlparser",
            ParsedCommand(
                method="GET",
                url="https://api.github.com/repos/nlecoy/curlparser",
                auth=(),
                cookies=OrderedDict(),
                data=None,
                json=None,
                header=OrderedDict(),
                verify=True,
            ),
        ),
        (
            "curl --insecure https://api.github.com/repos/nlecoy/curlparser",
            ParsedCommand(
                method="GET",
                url="https://api.github.com/repos/nlecoy/curlparser",
                auth=(),
                cookies=OrderedDict(),
                data=None,
                json=None,
                header=OrderedDict(),
                verify=False,
            ),
        ),
        (
            "curl -X DELETE https://api.github.com/repos/nlecoy/curlparser",
            ParsedCommand(
                method="DELETE",
                url="https://api.github.com/repos/nlecoy/curlparser",
                auth=(),
                cookies=OrderedDict(),
                data=None,
                json=None,
                header=OrderedDict(),
                verify=True,
            ),
        ),
        (
            "curl -b 'foo=bar' -b 'hello' https://api.github.com/repos/nlecoy/curlparser",
            ParsedCommand(
                method="GET",
                url="https://api.github.com/repos/nlecoy/curlparser",
                auth=(),
                cookies=OrderedDict([("foo", "bar")]),
                data=None,
                json=None,
                header=OrderedDict(),
                verify=True,
            ),
        ),
        (
            "curl -u nlecoy:my_password https://api.github.com/repos/nlecoy/curlparser",
            ParsedCommand(
                method="GET",
                url="https://api.github.com/repos/nlecoy/curlparser",
                auth=("nlecoy", "my_password"),
                cookies=OrderedDict(),
                data=None,
                json=None,
                header=OrderedDict(),
                verify=True,
            ),
        ),
        (
            "curl -d 'foo=bar' https://api.github.com/repos/nlecoy/curlparser",
            ParsedCommand(
                method="POST",
                url="https://api.github.com/repos/nlecoy/curlparser",
                auth=(),
                cookies=OrderedDict(),
                data="foo=bar",
                json=None,
                header=OrderedDict([("Content-Type", "application/x-www-form-urlencoded")]),
                verify=True,
            ),
        ),
        (
            """
            curl \
              --header 'Content-Type: application/json' \
              --header 'Hello World' \
              --request PUT \
              --user nlecoy:my_password \
              --data '{"username":"xyz", "password":"xyz"}' \
              https://api.github.com/repos/nlecoy/curlparser
            """,
            ParsedCommand(
                method="PUT",
                url="https://api.github.com/repos/nlecoy/curlparser",
                auth=("nlecoy", "my_password"),
                cookies=OrderedDict(),
                data='{"username":"xyz", "password":"xyz"}',
                json={
                    "username": "xyz",
                    "password": "xyz",
                },
                header=OrderedDict([("Content-Type", " application/json")]),
                verify=True,
            ),
        ),
    ],
)
def test_parse(curl_command, result):
    assert parse(curl_command) == result
