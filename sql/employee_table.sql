CREATE TABLE employee (
	employee_ID	numeric(5,0),
	name		varchar(100) NOT NULL,
	SSN		numeric(9,0),
	gender		char(2),
	email		varchar(20),
	phone		numeric(10,0) NOT NULL,
	address		varchar(255) NOT NULL,
	hiring_date	date NOT Null,
	primary key (employee_ID),
	unique(email)
	);
