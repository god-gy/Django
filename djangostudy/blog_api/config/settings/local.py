import os

from .base import *  # noqa: F403

DEBUG = os.getenv("DEBUG", True)

# CORS
# ALLOWED_HOSTS = ['mydomain.com'] # 실제로 배포할 때,
ALLOWED_HOSTS = ["*"]  # 로컬 개발용

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # 로컬 프론트 개발
    "https://app.example.com",  # 운영 프론트
]

# 또는 모든 출처 허용
# CORS_ALLOW_ALL_ORIGINS = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}
