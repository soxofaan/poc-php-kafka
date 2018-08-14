PHP - Kafka - AVRO POC
======================

POC the usage of Kafka with AVRO messages and the schema registry to manage the schemas.

Usage
-----

- `docker-compose up -d` To start kafka and zookeeper
- `docker-compose exec kafka kafka-topics.sh --create --zookeeper zookeeper --replication-factor 1 --partitions 5 --topic page_visits`
- `docker-compose run --rm java java -jar producer/target/java-producer-1.0-SNAPSHOT-jar-with-dependencies.jar <nb messages> http://schemaregistry:8081` To produce one or more messages with java
- `docker-compose run --rm java java -jar consumer/target/java-consumer-1.0-SNAPSHOT-jar-with-dependencies.jar http://schemaregistry:8081` To launch a java consumer
- Before running the PHP scripts, use Composer to setup up the dependencies and autoloader: from within `php` folder run `docker-compose run --rm php composer install`
- `docker-compose run --rm php php src/produce.php <nb messages>` To produce one or more messages with PHP
- `docker-compose run --rm php php src/consume.php` To launch a PHP consumer
- `docker-compose run --rm python python src/consume.py` To launch a Python consumer
- `docker-compose run --rm python python src/consume_raw.py` To launch a Python consumer for raw Kafka messages (without Avro deserialization)
- `docker-compose down --remove-orphans -v` To stop everything

Note: All consumers are created in the same group and consume the same topic. It means that a message won't be consumed twice by these consumers.
Note: As the topic is created with 5 partitions, you can't handle more than 5 messages at the same time.

Note
----

- librdkafka and php-rdkafka seems both to be under active development and pretty up-to-date with current kafka features
- The AVRO library does not seems to be well maintained but the project does not evolve that much so it does not seems to an issue.
