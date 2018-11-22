#-*- coding: UTF-8 -*-
import mysql.connector

def create_table(my_host, user_name, my_password, db_name, new_table):
	conn = mysql.connector.connect(host = my_host, 
		user = user_name,
		password = my_password, 
		database = db_name,
		)

	#-*- coding: UTF-8 -*-
	cur = conn.cursor()
	cur.execute("USE " + db_name + ";")

	#Create a table
	cur.execute(new_table)