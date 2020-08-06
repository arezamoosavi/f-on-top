#!/bin/sh

set -o errexit
set -o nounset

while python database/db_check.py; do echo 'connecting to database...'; sleep 2; done;

n=15

while [ $n -gt 0 ]
do
	echo "Wait for kafka  $n more times."
	n=$(( n-1 ))
    sleep 2
done


echo ". . . . . Faust App Is RUNNING! . . . . ."

faust -A faust_app.app:app worker -l info -p 6066

exec "$@"