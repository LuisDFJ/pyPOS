SELECT u.id, u.username, u.position, uu.password
FROM user u JOIN user_user uu ON u.id = uu.user_id