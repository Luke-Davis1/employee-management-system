# from getpass import getpass
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

print(cnx)