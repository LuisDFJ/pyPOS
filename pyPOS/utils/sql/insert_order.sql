INSERT INTO orders ( status_id, name, unix_time, user_id ) VALUES
(
    (SELECT id FROM order_status WHERE name = 'Open'),
    ?, STRFTIME( '%s', 'now' ), ?
)