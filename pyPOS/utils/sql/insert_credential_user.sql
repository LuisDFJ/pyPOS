INSERT INTO user_user ( user_id, password ) VALUES
( ( SELECT id FROM user WHERE username = ? ), ? )