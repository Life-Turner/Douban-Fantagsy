#-*- coding: UTF-8 -*-
import sys
sys.path.append(r'C:\Users\tyrel\Desktop\Fantagsy V3')

import requests
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
import json

"""Dealing with connection error"""
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def get_info(single_id, headers, info_url):
	#Some User Agents
	session = requests.Session()
	retry = Retry(connect=3, backoff_factor=0.5)
	adapter = HTTPAdapter(max_retries = retry)
	session.mount = ('http://', adapter)
	session.mount = ('https://', adapter)

	html = info_url.format(single_id = single_id)

	#Douban Movie ID
	dbid = single_id

	try:
		req = session.get(html, headers = headers)
		object_info = json.loads(req.text)		
	except requests.exceptions.ConnectionError:
		print("OMG! Connection Refused.")
		print("ID: " + single_id)
		time.sleep(8)
		info_dict = get_info(single_id, headers, info_url)
	else:
		#Original Movie Title
		if "title" in object_info:
			title = object_info["title"]
		else:
			title = ""
		
		#Movie's chinese title
		if "alt_title" in object_info:
			chi_title = object_info["alt_title"]
		else:
			chi_title = ""
		
		#Rater's amount and average rate
		if "rating" in object_info:
			raters = object_info["rating"]["numRaters"]
		else:
			raters = 0

		if "rating" in object_info:
			if object_info["rating"]["average"] != "":
				average = object_info["rating"]["average"]
			else:
				average = 0
		else:
			average = 0
			
		#Print out the information
		info_dict = {}
		info_dict['dbid'] = single_id
		info_dict['title'] = title
		info_dict['chi_title'] = chi_title
		info_dict['average'] = average
		info_dict['raters'] = raters
		# print(info_dict)

	return info_dict
