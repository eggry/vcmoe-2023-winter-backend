import os

DATA_DIR = os.getenv("DATA_DIR", "../data")

HOST_UID = os.getenv("HOST_UID", "495775367")

HOST_AVID = os.getenv("HOST_AVID", "85002656")

CORS_ALLOW_ORIGINS = [
    "https://localhost:8080",
    "http://localhost:8081",
    "https://xiaohengshu.com"
]
