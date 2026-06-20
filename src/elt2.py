import hashlib
import psycopg2

from config import DB_CONFIG, RECORD_SOURCE


def md5_hash(value: str) -> str:
    return hashlib.md5(value.encode("utf-8")).hexdigest()


def load_to_dds() -> None:
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT user_id, post_id, title, body FROM stg.posts;")
            rows = cur.fetchall()

            for user_id, post_id, title, body in rows:
                user_hk = md5_hash(str(user_id))
                post_hk = md5_hash(str(post_id))
                link_user_post_hk = md5_hash(f"{user_id}|{post_id}")
                hashdiff = md5_hash(f"{title or ''}|{body or ''}")

                cur.execute(
                    """
                    INSERT INTO dds.hub_user (user_hk, user_id, record_source)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (user_hk) DO NOTHING;
                    """,
                    (user_hk, user_id, RECORD_SOURCE),
                )

                cur.execute(
                    """
                    INSERT INTO dds.hub_post (post_hk, post_id, record_source)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (post_hk) DO NOTHING;
                    """,
                    (post_hk, post_id, RECORD_SOURCE),
                )

                cur.execute(
                    """
                    INSERT INTO dds.link_user_post
                        (link_user_post_hk, user_hk, post_hk, record_source)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (link_user_post_hk) DO NOTHING;
                    """,
                    (link_user_post_hk, user_hk, post_hk, RECORD_SOURCE),
                )

                cur.execute(
                    """
                    INSERT INTO dds.sat_post
                        (post_hk, title, body, hashdiff, record_source)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (post_hk, hashdiff) DO NOTHING;
                    """,
                    (post_hk, title, body, hashdiff, RECORD_SOURCE),
                )

            print(f"ELT 2 completed. Processed {len(rows)} rows from stg.posts")


def main() -> None:
    load_to_dds()


if __name__ == "__main__":
    main()
