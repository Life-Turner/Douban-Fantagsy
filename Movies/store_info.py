#-*- coding: UTF-8 -*-
import mysql.connector

def store_info(insert_data, my_host, user_name, my_password, db_name):
	conn = mysql.connector.connect(host = my_host, 
		user = user_name,
		password = my_password, 
		database = db_name,
		)

	cur = conn.cursor()
	cur.execute('USE ' + db_name)
	cur.execute(insert_data)

	conn.commit()
