CREATE SCHEMA IF NOT EXISTS dds;

DROP TABLE IF EXISTS dds.sat_post;
DROP TABLE IF EXISTS dds.link_user_post;
DROP TABLE IF EXISTS dds.hub_post;
DROP TABLE IF EXISTS dds.hub_user;

CREATE TABLE dds.hub_user (
    user_hk CHAR(32) PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    load_dt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    record_source VARCHAR(100) NOT NULL
);

CREATE TABLE dds.hub_post (
    post_hk CHAR(32) PRIMARY KEY,
    post_id INT NOT NULL UNIQUE,
    load_dt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    record_source VARCHAR(100) NOT NULL
);

CREATE TABLE dds.link_user_post (
    link_user_post_hk CHAR(32) PRIMARY KEY,
    user_hk CHAR(32) NOT NULL REFERENCES dds.hub_user(user_hk),
    post_hk CHAR(32) NOT NULL REFERENCES dds.hub_post(post_hk),
    load_dt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    record_source VARCHAR(100) NOT NULL
);

CREATE TABLE dds.sat_post (
    post_hk CHAR(32) NOT NULL REFERENCES dds.hub_post(post_hk),
    title TEXT,
    body TEXT,
    hashdiff CHAR(32) NOT NULL,
    load_dt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    record_source VARCHAR(100) NOT NULL,
    PRIMARY KEY (post_hk, hashdiff)
);

CREATE INDEX IF NOT EXISTS idx_link_user_post_user_hk ON dds.link_user_post(user_hk);
CREATE INDEX IF NOT EXISTS idx_link_user_post_post_hk ON dds.link_user_post(post_hk);
CREATE INDEX IF NOT EXISTS idx_sat_post_post_hk ON dds.sat_post(post_hk);
