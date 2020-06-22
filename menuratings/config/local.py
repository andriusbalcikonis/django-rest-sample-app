import os
import dj_database_url
from .common import Common

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):
    DEBUG = True

    # Postgres
    DATABASES = {
        "default": dj_database_url.config(
            default="postgres://postgres:@localhost:5432/postgres",
            conn_max_age=int(os.getenv("POSTGRES_CONN_MAX_AGE", 600)),
        )
    }
