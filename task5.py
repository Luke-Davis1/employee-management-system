from mysql.connector import connect, Error
from secrets import secrets

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

cursor.execute("""
               SELECT se.emp_no, title, salary
               FROM sub_employees se
               JOIN titles t
               ON t.emp_no = se.emp_no
               JOIN salaries s
               ON s.emp_no = se.emp_no
               WHERE se.employment_status IS NULL AND t.to_date = '9999-01-01' AND s.to_date = '9999-01-01'
               """)

result_set = cursor.fetchall()

for row in result_set:
    # See what titles are
    match row[1]:
        case 'Manager':
            cursor.callproc('update_salary', (row[0], int(row[2] * 1.1)))
        case 'Technique Leader':
            cursor.callproc('update_salary', (row[0], int(row[2] * 1.08)))
        case 'Engineer':
            cursor.callproc('update_salary', (row[0], int(row[2] * 1.075)))
        case 'Senior Engineer':
            cursor.callproc('update_salary', (row[0], int(row[2] * 1.07)))
        case 'Senior Staff':
            cursor.callproc('update_salary', (row[0], int(row[2] * 1.065)))
        case _:
            cursor.callproc('update_salary', (row[0], int(row[2] * 1.05)))
            
cnx.commit()