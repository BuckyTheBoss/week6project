DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS phone_call;

CREATE TABLE user (
	user_id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	password TEXT NOT NULL
);

CREATE TABLE customer (
	customer_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	first_name TEXT,
	last_name TEXT,
	phone NUMERIC,
	email TEXT,
	address1 TEXT,
	address2 TEXT,
	postal_code NUMERIC,
	city TEXT,
	country TEXT,
	added_by INTEGER,
	FOREIGN KEY (added_by) REFERENCES user(user_id)
);

CREATE TABLE phone_call (
	call_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	customer_id INTEGER,
	user_id INTEGER,
	call_time DATETIME DEFAULT CURRENT_TIMESTAMP,
	call_message TEXT,
	FOREIGN KEY (user_id) REFERENCES user(user_id),
	FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);





INSERT INTO user (username, password)
	VALUES ('admin', 'password');

insert into customer (first_name,last_name,phone,email,address1,address2,postal_code,city,country,added_by)
VALUES ('Test','Customer1','0500000000','test@test.com','test drive 1','apartment 23','12345','testcity','testcountry',1),('Test2','Customer2','0511111111','test2@test2.com','test drive 2','apartment 12','67890','testcity2','testcountry2',1);
