#!/bin/sh

set -o errexit
set -o nounset

sleep 70
echo ". . . . . Faust App Is RUNNING! . . . . ."

faust -A faust_app.app:app worker -l info -p 6066


exec "$@"