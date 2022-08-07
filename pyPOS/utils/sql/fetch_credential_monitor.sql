SELECT u.id, u.username, u.position, um.password
FROM user u JOIN user_monitor um ON u.id = um.user_id
WHERE u.username = ?