CREATE TABLE products
(
	product_id INT PRIMARY KEY,
	product VARCHAR NOT NULL,
	price FLOAT,
	description VARCHAR,
	stock INT,
	last_refill TIMESTAMP,
	next_refill TIMESTAMP
);
