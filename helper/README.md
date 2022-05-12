# helper

[`python:3-alpine`](https://hub.docker.com/_/python/)-based utility container for generating documentation for this repo

## usage

```
usage: main.py [-h] [--debug] workflows [workflows ...]

utility for generating documentation of this repo

positional arguments:
  workflows   path(s) to the workflow files to report on

optional arguments:
  -h, --help  show this help message and exit
  --debug     enable debug output (default: False)
```