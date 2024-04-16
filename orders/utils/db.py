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

try:
    DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'bubbles', 
                'USER': 'root', 
                'PASSWORD': 'Janvier9.@',  
                'HOST': 'localhost',  
                'PORT': '3306', 
                'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
    print("<<< CONNECTED TO THE DATABASE >>>")
except Exception as e:
    print("An error occurred while importing database settings:", e)
