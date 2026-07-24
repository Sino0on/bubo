# Развёртывание в продакшн (VPS + Docker Compose)

## 1. Подготовка сервера

- Ubuntu/Debian VPS с установленным Docker и Docker Compose plugin.
- Домен, указывающий A-записью на IP сервера.
- Открытые порты 80 и 443.

```bash
git clone <repo> bubo && cd bubo
cp .env.example .env
```

## 2. Заполнить `.env`

Обязательно для прода:

- `DEBUG=False`
- `SECRET_KEY` — сгенерировать: `python -c "import secrets; print(secrets.token_urlsafe(50))"`
- `ALLOWED_HOSTS=example.com,www.example.com`
- `CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com`
- `SITE_URL=https://example.com`
- `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` — свои значения
- `DATABASE_URL=postgresql://<POSTGRES_USER>:<POSTGRES_PASSWORD>@db:5432/<POSTGRES_DB>`
- `ADMIN_URL` — смените с `admin/` на что-то непредсказуемое, напр. `mgmt-8f2a/`
- `DJANGO_SUPERUSER_USERNAME` / `_EMAIL` / `_PASSWORD` — для создания админа
- `SENTRY_DSN` — если используете мониторинг ошибок (опционально)
- `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` — для уведомлений о заказах

## 3. Первый запуск (без TLS)

`nginx/conf.d/app.conf` по умолчанию слушает только порт 80 и отдаёт ACME challenge — этого
достаточно, чтобы получить сертификат.

Замените `example.com` на свой домен в `nginx/conf.d/app.conf`, затем:

```bash
docker compose up -d --build
docker compose logs -f web   # убедиться, что migrate/collectstatic прошли успешно
```

Создать суперпользователя:

```bash
docker compose exec web python manage.py shell < create_superuser.py
```

## 4. Получить TLS-сертификат

```bash
docker compose run --rm certbot certonly --webroot -w /var/www/certbot \
  -d example.com -d www.example.com \
  --email you@example.com --agree-tos --no-eff-email
```

Затем включить HTTPS:

```bash
cp nginx/app-ssl.conf.example nginx/conf.d/app.conf
sed -i 's/example\.com/ваш-домен.com/g' nginx/conf.d/app.conf   # если ещё не заменили
docker compose restart nginx
```

Сервис `certbot` в `docker-compose.yml` уже настроен на автопродление сертификата каждые 12 часов.

## 5. Бэкапы

```bash
crontab -e
# добавить строку (ежедневно в 03:00):
0 3 * * * cd /path/to/bubo && ./scripts/backup.sh >> backups/backup.log 2>&1
```

Бэкапы (дамп БД + архив медиа) складываются в `./backups`, хранятся 14 дней (настраивается
в `scripts/backup.sh`). **Рекомендуется** дополнительно копировать `./backups` за пределы
сервера (rsync/облачное хранилище) — локальный бэкап не спасает при потере самого сервера.

Восстановление:

```bash
./scripts/restore.sh backups/db_20260101_030000.sql.gz backups/media_20260101_030000.tar.gz
```

## 6. Проверка здоровья

`GET /healthz/` — проверяет соединение с БД, используется для docker/аптайм-мониторинга.

## 7. Обновление кода

```bash
git pull
docker compose up -d --build
```

`entrypoint.sh` при каждом старте контейнера `web` автоматически прогоняет `migrate` и
`collectstatic`.

## 8. Что дальше (не автоматизировано, но стоит рассмотреть)

- 2FA для админки (`django-otp`) — сейчас доступ защищён только паролем + непредсказуемым URL.
- Внешняя копия бэкапов (offsite).
- Учётные записи для персонала магазина в админке с ограниченными правами (`is_staff` + группы),
  если заказы будет обрабатывать не один человек.
