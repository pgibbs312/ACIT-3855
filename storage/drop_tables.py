import mysql.connector

db_conn = mysql.connector.connect(host="ec2-52-27-199-232.us-west-2.compute.amazonaws.com", user="root",
password="Pg000001", database="website")

db_cursor = db_conn.cursor()
db_cursor.execute('''
        DROP TABLE blog
    ''')
db_conn.commit()
db_conn.close()
