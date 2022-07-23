INSERT INTO user_admin ( user_id, password ) VALUES
( ( SELECT id FROM user WHERE username = ? ), ? )