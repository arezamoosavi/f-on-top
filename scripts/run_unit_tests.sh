#!/bin/sh

set -o errexit
set -o nounset

docker-compose exec faust python3 -m pytest -s -v --show-capture=no tests/
