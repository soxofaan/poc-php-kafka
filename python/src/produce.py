import logging
import os
import random
import time
import argparse
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

log = logging.getLogger(os.path.basename(__file__))


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        'messages', metavar='N', type=int,
        help='Number of messages to send'
    )
    arguments = arg_parser.parse_args()

    topic = 'page_visits'
    nb = arguments.messages

    key_schema_json = '{"type": "string"}'
    value_schema_json = '''
    {
        "namespace": "example.avro",
        "name": "page_visit",
        "type": "record",
        "fields":
        [
            {"name": "time", "type": "long"},
            {"name": "site", "type": "string"},
            {"name": "ip", "type": "string"}
        ]
    }
    '''

    key_schema = avro.loads(key_schema_json)
    value_schema = avro.loads(value_schema_json)

    producer = AvroProducer({
        'bootstrap.servers': 'kafka:9092',
        'schema.registry.url': 'http://schemaregistry:8081',
    }, default_key_schema=key_schema, default_value_schema=value_schema)

    log.info("Producing {n} messages to kafka topic {t!r}".format(n=nb, t=topic))
    for i in range(nb):
        ip = '192.168.2.{x}'.format(x=random.randint(0, 255))
        value = {
            'time': int(time.time()),
            'site': 'www.example.com',
            'ip': ip
        }
        producer.produce(topic=topic, key=ip, value=value)

    producer.flush()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
