import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='bubbles',
            user='root',
            password='Janvier9.@',
            port='3306'
        )
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None
