import mysql.connector

def get_connection():
    # Update these values to match your XAMPP MySQL setup

    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user='root',
            password='',
            database='kl_aanwezig'
        )
        
        return conn

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

