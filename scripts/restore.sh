#!/bin/sh
# Восстановление из бэкапа, созданного scripts/backup.sh.
# Использование: ./scripts/restore.sh backups/db_20260101_030000.sql.gz backups/media_20260101_030000.tar.gz
# ВНИМАНИЕ: перезаписывает текущую БД и медиафайлы.
set -eu

DB_DUMP="${1:?usage: restore.sh <db_dump.sql.gz> [media_archive.tar.gz]}"
MEDIA_ARCHIVE="${2:-}"

set -a
. "$(dirname "$0")/../.env"
set +a

echo "Restoring database from $DB_DUMP ..."
gunzip -c "$DB_DUMP" | docker compose exec -T db psql -U "$POSTGRES_USER" "$POSTGRES_DB"

if [ -n "$MEDIA_ARCHIVE" ]; then
  echo "Restoring media from $MEDIA_ARCHIVE ..."
  docker compose exec -T web sh -c "rm -rf /app/media/* && tar -xzf - -C /app" < "$MEDIA_ARCHIVE"
fi

echo "Restore complete."
