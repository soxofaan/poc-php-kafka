PHP - Kafka - AVRO POC
======================

POC the usage of Kafka with AVRO messages and the schema registry to manage the schemas.

Usage
-----

Kafka cluster set up

- `docker-compose up -d` To start kafka and zookeeper
- `docker-compose exec kafka kafka-topics.sh --create --zookeeper zookeeper --replication-factor 1 --partitions 5 --topic page_visits`

Java producing and consuming 

- `docker-compose run --rm java java -jar producer/target/java-producer-1.0-SNAPSHOT-jar-with-dependencies.jar <nb messages>` To produce one or more messages with java
- `docker-compose run --rm java java -jar consumer/target/java-consumer-1.0-SNAPSHOT-jar-with-dependencies.jar` To launch a java consumer

This POC comes with pre-built jars for Java. To build them through docker containers:
- `docker-compose run --rm java bash -c "cd producer && mvn package"`
- `docker-compose run --rm java bash -c "cd consumer && mvn package"`


PHP producing and consuming

- Before running the PHP scripts, use Composer to setup up the dependencies and autoloader: from within `php` folder run `docker-compose run --rm php composer install`
- `docker-compose run --rm php php src/produce.php <nb messages>` To produce one or more messages with PHP
- `docker-compose run --rm php php src/consume.php` To launch a PHP consumer

Python producing and consuming
- `docker-compose run --rm python python src/produce.py <nb messages>` To produce a couple of messages with Python
- `docker-compose run --rm python python src/consume.py` To launch a Python consumer
- `docker-compose run --rm python python src/consume_raw.py` To launch a Python consumer for raw Kafka messages (without Avro deserialization)
- `docker-compose run --rm python python src/schemaregistry.py` To dump the used schemas and versions from the schema registry

Tear down

- `docker-compose down --remove-orphans -v` To stop everything

Note: All consumers are created in the same group and consume the same topic. It means that a message won't be consumed twice by these consumers.
Note: As the topic is created with 5 partitions, you can't handle more than 5 messages at the same time.

Note
----

- librdkafka and php-rdkafka seems both to be under active development and pretty up-to-date with current kafka features
- The AVRO library does not seems to be well maintained but the project does not evolve that much so it does not seems to an issue.
