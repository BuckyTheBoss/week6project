DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS phone_call;

CREATE TABLE user (
	user_id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	password TEXT NOT NULL
);

-- CREATE TABLE customer (
-- 	...
-- );

-- CREATE TABLE phone_call (
-- ...
-- );





INSERT INTO user (username, password)
	VALUES ('admin', 'password');
