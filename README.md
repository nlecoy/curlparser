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
      -H 'Accept: application/vnd.github.v3+json' \
      https://api.github.com/repos/nlecoy/curlparser
    """
)

>>> result.url
'https://api.github.com/repos/nlecoy/curlparser'
```

## Available parameters

`curlparser`'s parse method will return a `ParsedCommand` object containing the following fields:

- method
- url
- auth
- data
- header

## License

cURL Parser is distributed under the Apache 2.0. See [LICENSE](LICENSE) for more information.
