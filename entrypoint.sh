#!/bin/sh
set -e

# Volumes mounted at runtime (media/staticfiles) may carry stale ownership
# from previous container versions — fix it before dropping to the
# unprivileged 'app' user for everything else.
chown -R app:app /app/media /app/staticfiles

gosu app python manage.py migrate --noinput
gosu app python manage.py collectstatic --noinput

exec gosu app "$@"
