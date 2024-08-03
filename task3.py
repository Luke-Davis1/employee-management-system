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

# Get the cursor
cursor = cnx.cursor()

# Get the CURRENT senior employees
senior_employees = []
cursor.execute("""
               SELECT t.emp_no
               FROM titles t
               JOIN sub_employees se
               ON t.emp_no = se.emp_no
               WHERE title LIKE 'Senior%'
               AND to_date = '9999-01-01'
               """)

for row in cursor.fetchall():
    senior_employees.append(row[0])

# Collect all the records from the employees table
cursor.execute("SELECT * FROM sub_employees")

# Store the result of all the tuples
result_set = cursor.fetchall()

# set up array to keep track of work_emails
work_email_list = []
total =1
# Go through each record in the table
for row in result_set:
    employee_number = row[0]
    string_employee_number = str(employee_number)
    if employee_number < 100000:
        phone_number = '801-60' + string_employee_number[0:1] + '-' + string_employee_number[1:]
    else:
        phone_number = '801-6' + string_employee_number[0:2] + '-' + string_employee_number[2:]
        
    first_name= row[2]
    first_letter = first_name[0:1].lower()
    last_name = row[3].lower()
    username = first_letter + last_name
    domain = '@company.net'
    work_email = username + domain
    counter = 1
    isPresent = work_email_list.count(work_email)
    
    while isPresent == 1:
        work_email = username + str(counter) + domain
        counter += 1
        isPresent = work_email_list.count(work_email)
        
    # append email to list
    work_email_list.append(work_email)
    print('Records processed:', total)
    total += 1
    cursor.callproc('update_employee_phone_number', (employee_number, phone_number))
    cursor.callproc('update_employee_work_email', (employee_number, work_email))
    
# Set up array to keep track of personal_emails
personal_email_list = []

for row in result_set:
    employee_number = row[0]
    first_name= row[2]
    first_letter = first_name[0:1].lower()
    last_name = row[3].lower()
    username = first_letter + last_name
    domain = '@personal.com'
    personal_email = username + domain
    counter = 1
    # Check if they are senior employee
    if senior_employees.count(employee_number) == 1:
        isPresent = personal_email_list.count(personal_email)
        
        while isPresent == 1:
            personal_email = username + str(counter) + domain
            counter += 1
            isPresent = personal_email_list.count(personal_email)
            
        # append email to list
        personal_email_list.append(personal_email)
    
        cursor.callproc('update_employee_personal_email', (employee_number, personal_email))
        
        
# Commit the changes to the database
cnx.commit()

# Close the connection
cnx.close()