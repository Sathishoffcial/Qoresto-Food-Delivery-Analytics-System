import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="nithish@004",
        database="zomato_db"
    )

if __name__ == "__main__":
    conn = get_db_connection()
    print("Database Connected Successfully!")
    conn.close()