DELIMITER //
CREATE PROCEDURE `update_salary`(IN employee_number INT, IN new_total INT)
BEGIN
	UPDATE salaries
    SET salary = new_total
    WHERE emp_no = employee_number AND to_date = '9999-01-01';
END //
DELIMITER ;