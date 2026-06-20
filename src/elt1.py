import requests
import psycopg2

from config import DB_CONFIG, SOURCE_URL, RECORD_SOURCE


def extract_posts() -> list[dict]:
    response = requests.get(SOURCE_URL, timeout=30)
    response.raise_for_status()
    return response.json()


def load_to_stg(posts: list[dict]) -> None:
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE stg.posts;")

            for post in posts:
                cur.execute(
                    """
                    INSERT INTO stg.posts (record_source, user_id, post_id, title, body)
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (
                        RECORD_SOURCE,
                        post["userId"],
                        post["id"],
                        post["title"],
                        post["body"],
                    ),
                )


def main() -> None:
    posts = extract_posts()
    load_to_stg(posts)
    print(f"ELT 1 completed. Loaded {len(posts)} rows to stg.posts")


if __name__ == "__main__":
    main()
