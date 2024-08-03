import csv
from mysql.connector import connect, Error
from secrets import secrets
import datetime

employee_numbers = []
# open the csv file
with open('employees_cuts.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        employee_numbers.append(row[0])

secret_key = secrets.get('SECRET_KEY')
db_user = secrets.get('DATABASE_USER', 'root')
db_pass = secrets.get('DATABASE_PASSWORD', 'pass')
db_port = secrets.get('DATABASE_PORT', 3306)

try:
    cnx = connect(
        host="localhost",
        user=db_user,
        password=db_pass,
        database='employees'
    )
except Error as e:
    print(e)
    
cursor = cnx.cursor()

# Check to see if the employee is getting fired
cursor.execute("""
               SELECT emp_no
               FROM sub_employees
               """)

result_set = cursor.fetchall()
# set termination date
termination_date = datetime.date(2023, 9,6)

for row in result_set:
    employee_number = row[0]
    if str(employee_number) in employee_numbers:
        cursor.callproc('update_employment_status', (employee_number, 'T', termination_date))


cnx.commit()