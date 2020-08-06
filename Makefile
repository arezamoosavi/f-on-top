init:
	sudo sysctl -w vm.max_map_count=262144
	sudo rm -rf esdata/
	mkdir esdata
	sudo chmod 777 -R esdata/

build_start:
	docker-compose up --build -d

get-indexes:
	curl http://localhost:9200/_cat/indices

raw_sensor-topic:
	docker-compose exec kafka kafka-topics --create \
	--topic raw-sensor --if-not-exists \
	kafka:9092 --replication-factor 1 --partitions 1 \
	--zookeeper zookeeper:2181 sleep infinity

processed_sensor-topic:
	docker-compose exec kafka kafka-topics --create \
	--topic processed-sensor --if-not-exists \
	kafka:9092 --replication-factor 1 --partitions 1 \
	--zookeeper zookeeper:2181 sleep infinity
