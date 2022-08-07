DROP VIEW IF EXISTS entry_view;

CREATE VIEW entry_view AS
SELECT
    oe.id       AS id,
    datetime( os.unix_time, 'unixepoch', 'localtime' ) AS order_timestamp,
    datetime( oe.unix_time, 'unixepoch', 'localtime' ) AS entry_timestamp,
    oe.order_id AS order_id,
    os.name     AS order_name,
    os.username AS user,
    pr.name     AS product,
    pr.category AS category,
    pr.price    AS price,
    oe.comment  AS comment,
    oes.name    AS status,
    oes.color   AS color,
    thumbnail
FROM
    order_entry AS oe
INNER JOIN
    (
        SELECT
            orders.id AS id,
            name,
            username,
            unix_time
        FROM orders
        INNER JOIN user ON orders.user_id = user.id
    )                           AS os   ON oe.order_id    = os.id
INNER JOIN product              AS pr   ON oe.product_id  = pr.id
INNER JOIN order_entry_status   AS oes  ON oe.status_id   = oes.id;