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

    MINIO_SERVER = "localhost"
    MINIO_ACCESSKEY = "Q3AM3UQ867SPQQA43P2F"
    MINIO_SECRET = "zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG"
    MINIO_BUCKET = "menuratings_bucket"
    MINIO_SECURE = True
    DEFAULT_FILE_STORAGE = "django_minio.storage.MinioStorage"
