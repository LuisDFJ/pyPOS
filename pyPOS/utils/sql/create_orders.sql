DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_status;
DROP TABLE IF EXISTS order_entry;
DROP TABLE IF EXISTS order_entry_status;

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    unix_time INTEGER NOT NULL,
    status_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (status_id) REFERENCES order_status(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE order_status (
    id      INTEGER PRIMARY KEY,
    name    TEXT UNIQUE NOT NULL,
    color   TEXT UNIQUE NOT NULL
);

INSERT INTO order_status ( id, name, color ) VALUES ( 1, 'Open', 'orange' );
INSERT INTO order_status ( id, name, color ) VALUES ( 2, 'Complete', 'green' );
INSERT INTO order_status ( id, name, color ) VALUES ( 3, 'Canceled', 'red' );


CREATE TABLE order_entry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    status_id INTEGER,
    product_id INTEGER,
    unix_time INTEGER NOT NULL,
    comment TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (status_id) REFERENCES order_entry_status(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE order_entry_status (
    id      INTEGER PRIMARY KEY,
    name    TEXT UNIQUE NOT NULL,
    color   TEXT UNIQUE NOT NULL
);

INSERT INTO order_entry_status ( id, name, color ) VALUES ( 1, 'Created',       'white' );
INSERT INTO order_entry_status ( id, name, color ) VALUES ( 2, 'In progress',   'yellow' );
INSERT INTO order_entry_status ( id, name, color ) VALUES ( 3, 'Ready',         'orange' );
INSERT INTO order_entry_status ( id, name, color ) VALUES ( 4, 'Delivered',     'green' );
INSERT INTO order_entry_status ( id, name, color ) VALUES ( 5, 'Payed',         'black' );
INSERT INTO order_entry_status ( id, name, color ) VALUES ( 6, 'Canceled',      'red' );
