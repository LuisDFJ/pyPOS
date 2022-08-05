INSERT INTO order_entry ( status_id, order_id, product_id, comment )
VALUES (
    ( SELECT id FROM order_entry_status WHERE name = 'Created' ),
    ?, ?, ?
)