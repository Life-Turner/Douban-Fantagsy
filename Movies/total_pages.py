#-*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup

def total_pages(tag_name, headers, id_url):
	session = requests.Session()
	html = id_url.format(tag_name = tag_name, number = 0)

	req = session.get(html, headers = headers)

	bs = BeautifulSoup(req.text, "html.parser")
	result_list = bs.find_all('span', {'class': 'thispage'})
	if result_list == []:
		total_num = 1
	else:
		total_num = int(result_list[0].get('data-total-page'))
	print("Total Pages: " + str(total_num))
	return total_num
