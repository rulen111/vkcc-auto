import os


class DefaultConfig(object):
    # App's secret key
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "very secret key")

    # VK API access token, can be of any type (user, service, community)
    TOKEN = os.getenv("FLASK_TOKEN", "None")
    # The amount of time to wait before sending next request to VK API
    API_RPS_RATE = os.getenv("FLASK_API_RPS_RATE", 3)

    # Index of an excel workbook row to be considered first
    # to have relevant data (starts from 1, not 0)
    PAYLOAD_FIRST_ROW = os.getenv("FLASK_PAYLOAD_FIRST_ROW", 2)
    # Index of an excel workbook column to be considered
    # as an input column (starts from 1, not 0)
    PAYLOAD_INPUT_COL = os.getenv("FLASK_PAYLOAD_INPUT_COL", 1)
    # Index of an excel workbook column to be considered
    # as an output column (starts from 1, not 0)
    PAYLOAD_TARGET_COL = os.getenv("FLASK_PAYLOAD_TARGET_COL", 2)

    # Redis broker url for celery
    REDIS_URL = os.getenv("FLASK_REDIS_URL", "redis://localhost:6379/0")

    CELERY = dict(
        broker_url=REDIS_URL,
        result_backend=REDIS_URL,
    )
