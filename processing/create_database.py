import sqlite3

conn = sqlite3.connect('stats.sqlite')

c = conn.cursor()
c.execute('''
    CREATE TABLE stats
    (
        id INTEGER PRIMARY KEY ASC,
        num_users INTEGER NOT NULL, 
        number_posts INTEGER NOT NULL,
        most_posts INTEGER NOT NULL,
        least_posts Varchar(100) NOT NULL,
        average_posts INTEGER NOT NULL,
        last_updated Varchar(100) NOT NULL
    )
''')
c.execute('''
    INSERT INTO stats (num_users, number_posts, most_posts, least_posts, average_posts, last_updated)
    VALUES ("0", "0", "0", "0", "0", "2021-11-27T18:01:36.112Z");
''')
conn.commit()
conn.close()