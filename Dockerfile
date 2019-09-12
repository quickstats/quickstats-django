FROM python:3.6-alpine
LABEL maintainer=kungfudiscomonkey@gmail.com

ENV APP_DIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Upgrade Pip
RUN pip install --no-cache-dir -U pip

# Install Postgres Support
RUN set -ex \
    && apk add --no-cache postgresql-dev \
    && apk add --no-cache --virtual build-deps build-base \
    && pip install --no-cache-dir psycopg2-binary \
    && apk del build-deps

# Install Pillow Support
RUN set -ex \
    && apk add --no-cache jpeg-dev zlib-dev \
    && apk add --no-cache --virtual build-deps build-base \
    && pip install --no-cache-dir Pillow==6.0.0 \
    && apk del build-deps

# Finish installing app
WORKDIR ${APP_DIR}
ADD quickstats ${APP_DIR}/quickstats
ADD docker ${APP_DIR}/docker
ADD setup.py ${APP_DIR}/setup.py
RUN set -ex && pip install --no-cache-dir -r ${APP_DIR}/docker/requirements.txt
USER nobody

ENTRYPOINT ["docker", "docker-entrypoint.sh"]
CMD ["web"]
