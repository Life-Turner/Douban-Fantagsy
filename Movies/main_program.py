#-*- coding: UTF-8 -*-
import sys
sys.path.append(r'C:\Users\tyrel\Desktop\Fantagsy V3')

from get_id import get_ID
from get_info import get_info
from store_info import store_info
from create_table import create_table
from drop_table import drop_table
from total_pages import total_pages
import time

headers = {'User-Agent':
'Mozilla/5.0 (Windows; U; Windows NT 6.1;'\
' en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

id_url = r'https://movie.douban.com/tag/{tag_name}?start={number}&type=T'
info_url = r'https://douban.uieee.com/v2/movie/{single_id}'

#Get a tag
tag_name = input("Please enter a tag: ")
#Other variables
pattern_text = r'\d+'

#Get the total pages
pages = total_pages(tag_name, headers, id_url)
num_each_page = 20
total_num = pages * num_each_page
my_index = 0

my_host = "127.0.0.1"
user_name = 'root'
my_password = 'D0more&t4lkless'
db_name = 'douban'

table_name = input("Table's Name: ")
delete_table = """DROP TABLE IF EXISTS {tb_name};""".format(tb_name = table_name)
new_table = """
CREATE TABLE IF NOT EXISTS {tb_name} (
my_index INT(5) NOT NULL, 
id INT(10), 
title VARCHAR(200), 
chi_title VARCHAR(200), 
raters INT(10), 
average_rate FLOAT(4, 1),
PRIMARY KEY(my_index)
);""".format(tb_name = table_name)

#Drop a table
drop_table(my_host, user_name, my_password, db_name, delete_table)

#Create a new table
create_table(my_host, user_name, my_password, db_name, new_table)

#Main Program
for page in range(pages):

	#Get ID
	number = page * num_each_page
	ID_list = get_ID(number, tag_name, pattern_text, headers, id_url)
	time.sleep(3)
	print('Pages Cruising Procedure: '\
		'{:.2%}'.format(page/pages))

	for single_id in ID_list:
		my_index += 1
		#Get information of id
		try:
			ID_info = get_info(single_id, headers, info_url)
			
			#Store information
			insert_data = '''INSERT INTO {tb_name} \
			(my_index, id, title, chi_title, average_rate, raters) \
			VALUES ({my_index}, {dbid}, "{title}", "{chi_title}", {average_rate}, {raters})\
			;'''.format(tb_name = table_name,
				my_index = my_index,
				dbid = ID_info['dbid'],
				title = ID_info['title'],
				chi_title = ID_info['chi_title'],
				average_rate = ID_info['average'],
				raters = ID_info['raters']
				)
			# print(insert_data)

			store_info(insert_data, my_host, user_name, my_password, db_name)
			print('ID Procedure: {:.2%}'.format(my_index/total_num))

		except KeyError:
			print("An KeyError just happened. ID: ")
			print(str(single_id))
			continue

		#Make it sleep for a few seconds to avoid connection refused.
		time.sleep(4)

print("Hooray! Mission Finally Done.")
