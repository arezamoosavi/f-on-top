buildstart:
	docker-compose up --build -d

create-sample-topic:
	bash scripts/local_kafka_create_topics.sh 

run-tests:
	bash scripts/run_unit_tests.sh