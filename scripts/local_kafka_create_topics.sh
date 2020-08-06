#!/bin/sh

set -o errexit
set -o nounset

docker-compose exec kafka kafka-topics --create \
--topic sample_topic --if-not-exists \
kafka:9092 --replication-factor 1 --partitions 1 \
--zookeeper zookeeper:2181 sleep infinity
