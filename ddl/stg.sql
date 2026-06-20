CREATE SCHEMA IF NOT EXISTS stg;

DROP TABLE IF EXISTS stg.posts;

CREATE TABLE stg.posts (
    load_dt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    record_source VARCHAR(100) NOT NULL DEFAULT 'jsonplaceholder.posts',
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    title TEXT,
    body TEXT
);

CREATE INDEX IF NOT EXISTS idx_stg_posts_user_id ON stg.posts(user_id);
CREATE INDEX IF NOT EXISTS idx_stg_posts_post_id ON stg.posts(post_id);
