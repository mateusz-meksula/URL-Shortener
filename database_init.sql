CREATE SCHEMA IF NOT EXISTS shortener;
USE shortener;

CREATE TABLE IF NOT EXISTS user (
    user_id SMALLINT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(20) UNIQUE NOT NULL,
    hash VARCHAR(60) NOT NULL,

    PRIMARY KEY (user_id),
    INDEX idx_name (name)
);

CREATE TABLE IF NOT EXISTS url (
    url_id SMALLINT UNSIGNED AUTO_INCREMENT,
    user_id SMALLINT UNSIGNED,
    short VARCHAR(6) UNIQUE NOT NULL,
    long_url VARCHAR(250) NOT NULL,
    count SMALLINT NOT NULL DEFAULT 0,
    created timestamp DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (url_id),
    FOREIGN KEY (user_id) REFERENCES user (user_id),
    INDEX idx_short (short)
);