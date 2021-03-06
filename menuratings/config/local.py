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

    MINIO_SERVER = "localhost:8002"
    MINIO_ACCESSKEY = "minio_admin"
    MINIO_SECRET = "minio_password"
    MINIO_BUCKET = "menuratingsbucket"
    MINIO_SECURE = False
    DEFAULT_FILE_STORAGE = "django_minio.storage.MinioStorage"

    GRAYLOG_ENDPOINT = "udp://localhost:12201"
