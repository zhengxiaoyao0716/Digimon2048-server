#!python

from flask import Flask
app = Flask(__name__)

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

import json
#@return ranking list after <days>ago with 
#	limit <count> and order by <order>(DESC/ASC).
@app.route('/get_ranks/<int:days>/<int:count>/<order>')
def get_ranks(days, count, order):
	values = []
	for m_level in range(8):
		level_values = sqlite_execute("SELECT * FROM rank\
			WHERE level == {0} AND \
			time > date('now','-{1} day')\
			ORDER BY score {2} \
			LIMIT {3}\
			".format(m_level + 1, days - 1, order, count))
		if order == 'DESC': values.insert(0, level_values)
		else: values.append(level_values)
	return json.dumps(values)

#@return player's online ranking
@app.route('/find_position/<int:level>/<int:score>')
def find_position(level, score):
	values = sqlite_execute("SELECT level, score FROM rank\
		WHERE time > date('now','0 day')\
		ORDER BY level DESC, score DESC")
	rank = 1
	for m_level, m_score in values:
		rank += 1
		if m_level > level or (m_level == level \
				and m_score > score):
			continue
		break
	return str(rank)

#Push player's grade, Use 'POST' type.
#@param level player's level
#@param score player's score
#@param name player's name
#@param time formated time such as '2015-10-10 15:00:00'
from flask import request
@app.route('/push_grade', methods = ['GET', 'POST'])
def push_grade():
        sqlite_execute('INSERT INTO rank VALUES({0}, {1}, "{2}", "{3}")\
                '.format(request.form['level'], request.form['score'],
                request.form['name'].encode('UTF-8'),
                request.form['time']))
        return 'succeed'


if __name__ == '__main__':
        #app.run(host="123.57.72.138",port=5000)
		app.run()