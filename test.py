import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="nithish@004"
    )

    print("Connected Successfully!")

except Exception as e:
    print(e)