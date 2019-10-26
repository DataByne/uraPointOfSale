CREATE TABLE subproducts
(
	product_id INT NOT NULL,
	subproduct_id INT NOT NULL REFERENCES products(product_id),
	price FLOAT,
	PRIMARY KEY(product_id, subproduct_id)
);
