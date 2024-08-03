from tabulate import tabulate
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
               SELECT 
               title,
               ROUND(AVG(salary)) * COUNT(*) AS 'calculated total'
               FROM
               titles t
               JOIN
               sub_employees se ON se.emp_no = t.emp_no
               JOIN
               salaries s ON t.emp_no = s.emp_no
               WHERE
               se.employment_status IS NULL
               AND t.to_date = '9999-01-01'
               AND s.to_date = '9999-01-01'
               GROUP BY title
               ORDER BY ROUND(AVG(salary)) * COUNT(*);
               """)

result_set = cursor.fetchall()
total = 0
# Get the total amount
for row in result_set:
    total += row[1]

final = [[f"{total}"]]
table_head = ['Title', 'Projected Total Pay']
print()
print("S A L A R Y   A N D   P R O J E C T I O N   R E P O R T")
print(tabulate(result_set, headers=table_head, tablefmt="grid", disable_numparse=True))
print()
print('A S S U M P T I O N S   /   C O N S I D E R A T I O N S')
print("""
      This report takes into account salaries as they currently stand in the database. While collecting this data, I noticed that some employees
      have had the same salary for 10-20 years which wouldn't occur in the real world. Instead there would be a greater range and possibly much higher
      expenses for the company to pay all of there workers. On top of that, this report only looks into roughly 3/100ths of all employees in the database
      due to runtimes on various algorithms to compute emails, phone numbers, etc. This report also assumed that no bonuses or additional expenses such
      as healthcare or 401k contributions should be taken into account when producing this report.
      """)
print()
print('S U M M A R Y   S E C T I O N')
final_head = ['Total Projected Expenses']
print(tabulate(final, headers=final_head, tablefmt="grid", disable_numparse=True))