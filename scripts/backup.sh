#!/bin/sh
# Дамп Postgres + архив медиафайлов. Запускать из корня проекта (там где docker-compose.yml).
# Пример cron (ежедневно в 03:00): 0 3 * * * cd /path/to/bubo && ./scripts/backup.sh >> backups/backup.log 2>&1
set -eu

RETENTION_DAYS=14
BACKUP_DIR="$(cd "$(dirname "$0")/.." && pwd)/backups"
STAMP="$(date +%Y%m%d_%H%M%S)"

mkdir -p "$BACKUP_DIR"

set -a
. "$(dirname "$0")/../.env"
set +a

echo "[$STAMP] Dumping database..."
docker compose exec -T db pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" | gzip > "$BACKUP_DIR/db_$STAMP.sql.gz"

echo "[$STAMP] Archiving media..."
docker compose exec -T web tar -czf - -C /app media > "$BACKUP_DIR/media_$STAMP.tar.gz"

echo "[$STAMP] Pruning backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name '*.sql.gz' -mtime +"$RETENTION_DAYS" -delete
find "$BACKUP_DIR" -name '*.tar.gz' -mtime +"$RETENTION_DAYS" -delete

echo "[$STAMP] Done: db_$STAMP.sql.gz, media_$STAMP.tar.gz"
