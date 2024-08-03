Use employees;
-- Add new column to sub_employees table
ALTER TABLE sub_employees
ADD employment_status CHAR(1);

-- Add a termination_date field to dept_emp table
ALTER TABLE dept_emp
ADD termination_date DATE;

-- Add stored procedure to update employment status and termination date
DELIMITER //
CREATE PROCEDURE `update_employment_status`(IN employee_number INT, IN emp_status CHAR(1), IN in_date DATE)
BEGIN
	-- Update employment status
    UPDATE sub_employees
    SET employment_status = emp_status
    WHERE emp_no = employee_number;

    -- Update termination date
    UPDATE dept_emp
    SET termination_date = in_date
    WHERE emp_no = employee_number AND to_date = '9999-01-01';
    
    -- Update to_date
    UPDATE dept_emp
    SET to_date = in_date
    WHERE emp_no = employee_number AND termination_date = in_date;
    
    -- Update titles table
    UPDATE titles
    SET to_date = in_date
    WHERE emp_no = employee_number;
    
END //
DELIMITER ;




