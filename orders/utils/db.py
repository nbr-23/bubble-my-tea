import mysql.connector

def connect_to_database():
    try:
       
        host = 'sql11.freesqldatabase.com'
        database = 'sql11699181'
        user = 'sql11699181'
        password = 'ZfjSzeVCt2'
        port = 3306

        
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )

        if connection.is_connected():
            print('Database connection successful.')
            return connection
        else:
            print('Database connection failed.')
            return None
    except mysql.connector.Error as error:
        print('Error connecting to the database:', error)
        return None


if __name__ == "__main__":
    db_connection = connect_to_database()

