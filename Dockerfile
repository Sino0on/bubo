FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system app && adduser --system --group --home /home/app app
ENV HOME=/home/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/media /app/staticfiles \
    && chown -R app:app /app \
    && chmod +x /app/entrypoint.sh

USER app

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "bubostore.wsgi:application", "--bind", "0.0.0.0:8032", "--workers", "3", "--timeout", "30", "--access-logfile", "-", "--error-logfile", "-"]