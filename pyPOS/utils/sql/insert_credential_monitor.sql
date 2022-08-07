INSERT INTO user_monitor ( user_id, password ) VALUES
( ( SELECT id FROM user WHERE username = ? ), ? )