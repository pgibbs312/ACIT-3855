import mysql.connector

mydb = mysql.connector.connect(
    host="ec2-52-27-199-232.us-west-2.compute.amazonaws.com",
    user="root",
    password="Pg000001"
)

c = mydb.cursor()
c.execute("use website")
c.execute('''
    CREATE TABLE blog (
        id INTEGER AUTO_INCREMENT,
        trans_id VARCHAR(250) NOT NULL,
        blog_id INTEGER NOT NULL,
        title VARCHAR(100) NOT NULL,
        snippet VARCHAR(100) NOT NULL,
        blogBody VARCHAR(250) NOT NULL,
        userName VARCHAR(100) NOT NULL,
        postNumbers INTEGER NOT NULL,
        date VARCHAR(250) NOT NULL,
        PRIMARY KEY (id))
    ''')

c.execute('''
    CREATE TABLE users(
        id INTEGER AUTO_INCREMENT,
        trans_id VARCHAR(250) NOT NULL,
        user_id INTEGER NOT NULL,
        email VARCHAR(100) NOT NULL,
        name VARCHAR(100) NOT NULL,
        password Varchar(100) NOT NULL,
        phoneNumber Varchar(250) NOT NULL,
        timeStamp VARCHAR(100) NOT NULL,
        age INTEGER NOT NULL,
        friends INTEGER NOT NULL,
        PRIMARY KEY (id))
''')
mydb.commit()
mydb.close()