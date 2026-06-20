import os

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "dv_db"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}

SOURCE_URL = "https://jsonplaceholder.typicode.com/posts"
RECORD_SOURCE = "jsonplaceholder.posts"
