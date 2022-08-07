DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_admin;
DROP TABLE IF EXISTS user_monitor;
DROP TABLE IF EXISTS user_user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    position TEXT NOT NULL
);

CREATE TABLE user_admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password TEXT NOT NULL,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user( id )
);

CREATE TABLE user_monitor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password TEXT NOT NULL,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user( id )
);

CREATE TABLE user_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password TEXT NOT NULL,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user( id )
);