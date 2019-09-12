FROM python:3.6-alpine
LABEL maintainer=kungfudiscomonkey@gmail.com

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV APP_DIR /usr/src/app
ENV STATIC_ROOT /var/cache/app
ENV MEDIA_ROOT /var/lib/app

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
RUN SECRET_KEY=1 quickstats collectstatic --noinput
USER nobody
EXPOSE 8000

ENTRYPOINT ["docker/docker-entrypoint.sh"]
CMD ["web"]
