SELECT u.id, u.username, u.position, ua.password
FROM user u JOIN user_admin ua ON u.id = ua.user_id
WHERE u.username = ?