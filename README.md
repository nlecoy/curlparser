# cURL Parser

Parse cURL commands returning object representing the request.

## How to install?

`curlparser` is available on PyPi:

### Using pip

```shell
$ pip install curlparser
```
### Using poetry

```shell
$ poetry add curlparser
```

### Using pipenv

```shell
$ pipenv install curlparser
```

## How to use?

```python
>>> import curlparser

>>> result = curlparser.parse(
    """
    curl \
      --header 'Content-Type: application/json' \
      --request PUT \
      --user nlecoy:my_password \
      --data '{"username":"xyz", "password":"xyz"}' \
      https://api.github.com/repos/nlecoy/curlparser
    """
)

>>> result.url
'https://api.github.com/repos/nlecoy/curlparser'

>>> result.auth
('nlecoy', 'my_password')

>>> result.json
{'username': 'xyz', 'password': 'xyz'}
```

## Available parameters

`curlparser`'s parse method will return a `ParsedCommand` object containing the following fields:

- method
- url
- auth
- cookies
- data
- json
- header
- verify

## License

cURL Parser is distributed under the Apache 2.0. See [LICENSE](LICENSE) for more information.
