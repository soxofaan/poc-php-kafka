import contextlib
import logging
import os

from confluent_kafka import Consumer

log = logging.getLogger(os.path.basename(__file__))


def main():
    topic = 'page_visits'

    c = Consumer({
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'raw.py',
    })
    c.subscribe([topic])

    log.info("Starting to consume kafka topic {t!r}".format(t=topic))
    with contextlib.closing(c):
        while True:
            try:
                msg = c.poll(1)
                if msg:
                    print((
                        msg.key(),
                        msg.value(),
                        msg.error()
                    ))
            except KeyboardInterrupt:
                log.info("kthxby!")
                break
            except Exception as e:
                log.error("Consume failure: %r.", e, exc_info=True)
                continue


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
