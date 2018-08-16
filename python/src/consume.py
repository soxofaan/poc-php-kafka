import contextlib
import logging
import os

from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer

log = logging.getLogger(os.path.basename(__file__))


def main():
    topic = 'page_visits'

    c = AvroConsumer({
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'SimpleConsumerExample',
        'schema.registry.url': 'http://schemaregistry:8081',
    })
    c.subscribe([topic])

    log.info("Starting to consume kafka topic {t!r}".format(t=topic))
    with contextlib.closing(c):
        while True:
            try:
                msg = c.poll(1)
                if msg:
                    if not msg.error():
                        print(msg.value())
                    elif msg.error().code() != KafkaError._PARTITION_EOF:
                        log.error("Kafka error: %r", msg.error())
                        continue
            except KeyboardInterrupt:
                log.info("kthxby!")
                break
            except Exception as e:
                log.error("Consume failure: %r.", e, exc_info=True)
                continue


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
