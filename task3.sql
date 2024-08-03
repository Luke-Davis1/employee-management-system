use employees;

-- Add the two neccessary columns
ALTER TABLE employees
ADD work_email VARCHAR(75);

ALTER TABLE employees
ADD personal_email VARCHAR(75);

ALTER TABLE employees
ADD work_phone CHAR(12);

-- Create stored Procedure for work_emails
DELIMITER //
CREATE PROCEDURE `update_employee_work_email`(IN employee_number INT, IN email VARCHAR(75))
	BEGIN
	UPDATE sub_employees
	SET work_email = email
	WHERE emp_no = employee_number;
	END //
DELIMITER ;

-- Create stored Procedure for personal_emails
DELIMITER //
CREATE PROCEDURE `update_employee_personal_email`(IN employee_number INT, IN email VARCHAR(75))
	BEGIN
	UPDATE sub_employees
	SET personal_email = email
	WHERE emp_no = employee_number;
	END //
DELIMITER ;

-- Create Procedure for phone number
DELIMITER //
CREATE PROCEDURE `update_employee_phone_number`(IN employee_number INT, IN phone CHAR(12))
	BEGIN
	UPDATE sub_employees
	SET work_phone = phone
	WHERE emp_no = employee_number;
	END //
DELIMITER ;

-- Create a table containing a subset of the employees table
CREATE TABLE sub_employees LIKE employees;

-- Insert 10,000 records into the subset table (birthdate helps randomize the numbers)
INSERT INTO sub_employees
select * from employees order by birth_date LIMIT 10000;


