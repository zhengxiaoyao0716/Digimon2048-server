import sqlite3
def sqlite_execute(exec_str):
        conn = sqlite3.connect('rank_list.db')
        cursor = conn.cursor()
        cursor.execute(exec_str)
        values = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return values
#Create
sqlite_execute('CREATE TABLE rank\
        (level INTEGER, score INTEGER, \
		name nvarchar(20), time TimeStamp)')

#Insert test dates
import random, time
conn = sqlite3.connect('rank_list.db')
cursor = conn.cursor()
for i in range(100):
        level = random.randint(1, 5)
        score = random.randint(0, 5000)
        time = '2015-10-%02d %02d:%02d:%02d'%(
			random.randint(1, 12),
			random.randint(0, 23),
			random.randint(0, 59),
			random.randint(0, 59))
        cursor.execute('INSERT INTO rank \
			VALUES(%d,%d,"asdf","%s")'
			%(level,score,time))

cursor.close()
conn.commit()
conn.close()