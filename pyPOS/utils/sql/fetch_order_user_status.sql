SELECT
    datetime( o.unix_time, 'unixepoch', 'localtime' ) AS timestamp,
    o.id        AS id,
    o.name      AS name,
    os.name     AS status,
    os.color    AS color,
    u.username  AS username,
    o.status_id AS status_id,
    o.user_id   AS user_id
FROM orders AS o
INNER JOIN order_status AS os
    ON o.status_id = os.id
INNER JOIN user AS u
    ON o.user_id = u.id
WHERE o.user_id = ?
AND os.name = ?