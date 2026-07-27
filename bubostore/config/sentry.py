import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration


def init_sentry(debug: bool = False) -> None:
    dsn = os.getenv("SENTRY_DSN")

    # Не инициализируем Sentry, если DSN отсутствует
    if not dsn:
        return

    sentry_logging = LoggingIntegration(
        level=None,      # Breadcrumbs не собираем из логов
        event_level=None # Не отправляем logging как события
    )

    sentry_sdk.init(
        dsn=dsn,

        integrations=[
            DjangoIntegration(),
            sentry_logging,
        ],

        environment=os.getenv(
            "ENVIRONMENT",
            "development",
        ),

        release=os.getenv(
            "RELEASE",
            "unknown",
        ),

        # Производительность
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.2")),

        # Профилирование
        profile_session_sample_rate=float(os.getenv("SENTRY_PROFILE_SAMPLE_RATE", "0.2")),
        profile_lifecycle="trace",

        # Отправлять PII (пользователь, IP и т.п.) — заказы содержат имена/телефоны покупателей,
        # по умолчанию выключено, чтобы не светить их в Sentry
        send_default_pii=os.getenv("SENTRY_SEND_PII", "False") == "True",

        debug=debug,
    )