FROM php:7.2-cli-alpine


# Install composer (based on https://hub.docker.com/r/library/composer/)
ENV COMPOSER_ALLOW_SUPERUSER 1
ENV COMPOSER_HOME /tmp
ENV COMPOSER_VERSION 1.6.5

RUN curl -s -f -L -o /tmp/installer.php https://raw.githubusercontent.com/composer/getcomposer.org/b107d959a5924af895807021fcef4ffec5a76aa9/web/installer \
 && php -r " \
    \$signature = '544e09ee996cdf60ece3804abc52599c22b1f40f4323403c44d44fdfdd586475ca9813a858088ffbc1f233e9b180f061'; \
    \$hash = hash('SHA384', file_get_contents('/tmp/installer.php')); \
    if (!hash_equals(\$signature, \$hash)) { \
        unlink('/tmp/installer.php'); \
        echo 'Integrity check failed, installer is either corrupt or worse.' . PHP_EOL; \
        exit(1); \
    }" \
 && php /tmp/installer.php --no-ansi --install-dir=/usr/bin --filename=composer --version=${COMPOSER_VERSION} \
 && composer --ansi --version --no-interaction \
 && rm -rf /tmp/* /tmp/.htaccess



# Build dependencies for librdkafka (https://github.com/edenhill/librdkafka)
# Based on https://github.com/elek/docker-librdkafka/blob/master/Dockerfile
RUN apk add --update --no-cache build-base git bash autoconf python
# Build and install librdkafka
WORKDIR /root/src/librdkafka
RUN git clone https://github.com/edenhill/librdkafka.git . \
    && git checkout v0.11.5 \
    && ./configure \
    && make \
    && make install


# Install and enable php-rdkafka client (https://github.com/arnaud-lb/php-rdkafka)
RUN pecl install rdkafka-3.0.5 \
    && docker-php-ext-enable rdkafka
