#!/bin/sh

set -e

if [ "${1:0:1}" = '-' ]; then
	set -- quickstats "$@"
fi

# wait() 
# {
#     until quickstats check 2>/dev/null
#     do
#         echo "Waiting for database to startup"
#         sleep 3
#     done
# }

case "$1" in
worker)
  # Shortcut to start a celery worker for Promgen
  set -- celery "-A" quickstats "$@"
  ;;
web)
  # Shortcut for launching a Promgen web worker under gunicorn
  shift
  set -- gunicorn "quickstats.standalone.wsgi:application" "$@"
  ;;
esac

# Finally exec our command
exec "$@"
