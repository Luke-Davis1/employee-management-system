from pymongo import MongoClient
from mysql.connector import connect, Error
from secrets import secrets
from tabulate import tabulate

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
    
MONGODB_URI = 'mongodb+srv://[username]:[password]@cluster0.owg0dbs.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(MONGODB_URI)

# Create/retrieve a database called 'Employee appreciation'
employee_appreciation = client['employee_appreciation']

# Create/retreive the bonuses collection
bonuses_collection = employee_appreciation['bonuses']

# Insert the bonuses data into the collection
# bonus_data = [
#     { 'yearsOfService': 1, 'bonusAmount': 50 },
#    { 'yearsOfService': 5, 'bonusAmount': 500 },
#    { 'yearsOfService': 10, 'bonusAmount': 1000 },
#    { 'yearsOfService': 15, 'bonusAmount': 1500 },
#    { 'yearsOfService': 20, 'bonusAmount': 3000 },
#    { 'yearsOfService': 25, 'bonusAmount': 4000 },
#    { 'yearsOfService': 30, 'bonusAmount': 5000 }
# ]

# # Insert bonus data into collection
# bonuses_collection.insert_many(bonus_data)

# Pull in the data from the MYSQL database with appropriate years of service
cursor = cnx.cursor()

cursor.execute("""
               SELECT 
                se.emp_no,
                first_name,
                last_name,
                FLOOR(DATEDIFF('2023-09-06', from_date) / 365.25) AS 'Years of service'
                FROM
                    dept_emp de
                        JOIN
                    sub_employees se ON se.emp_no = de.emp_no
                WHERE
                    se.employment_status IS NULL
                        AND to_date = '9999-01-01'
                        AND (FLOOR(DATEDIFF('2023-09-06', from_date) / 365.25) = 25
                        OR FLOOR(DATEDIFF('2023-09-06', from_date) / 365.25) = 30);
               """)

result_set = cursor.fetchall()

filter = {'_id': 0 }

bonus_30_years = bonuses_collection.find_one({'yearsOfService': 30}, filter)['bonusAmount']
bonus_25_years = bonuses_collection.find_one({'yearsOfService': 25}, filter)['bonusAmount']
bonus_20_years = bonuses_collection.find_one({'yearsOfService': 20}, filter)['bonusAmount']
bonus_15_years = bonuses_collection.find_one({'yearsOfService': 15}, filter)['bonusAmount']
bonus_10_years = bonuses_collection.find_one({'yearsOfService': 10}, filter)['bonusAmount']
bonus_5_years = bonuses_collection.find_one({'yearsOfService': 5}, filter)['bonusAmount']
bonus_1_year = bonuses_collection.find_one({'yearsOfService': 1}, filter)['bonusAmount']

new_set = []

# Go through each tuple in the result_set, updating the row with bonus data
for row in result_set:
    if row[3] >= 30:
        new_set.append(row + (bonus_30_years,))
    elif row[3] >= 25:
        new_set.append(row + (bonus_25_years,))
    elif row[3] >= 20:
        new_set.append(row + (bonus_20_years,))
    elif row[3] >= 15:
        new_set.append(row + (bonus_15_years,))
    elif row[3] >= 10:
        new_set.append(row + (bonus_10_years,))
    elif row[3] >= 5:
        new_set.append(row + (bonus_5_years,))
    elif row[3] >= 1:
        new_set.append(row + (bonus_1_year,))
    else:
        new_set.append(row + (0,))   
     
# Create the headers for the table
head = ['Employee Number', 'First Name', 'Last Name', 'Years of Service', 'Bonus Amount']

# Print the results
print(tabulate(new_set, headers=head, tablefmt="grid", disable_numparse=True))