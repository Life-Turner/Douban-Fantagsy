#-*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re

def get_ID(number, tag_name, pattern_text, headers, id_url):
    #Some User Agents
    session = requests.Session()
    id_pattern = re.compile(pattern_text)
    id_list = []
  
    html = id_url.format(tag_name = tag_name, number = number)

    req = session.get(html, headers = headers)

    bs = BeautifulSoup(req.text, "html.parser")
    # print(bs)

    link_list = bs.select('td div a')
    # print(link_list)

    for link in link_list:
        link_href = link.get('href')
        link_id = id_pattern.search(link_href).group()
        id_list.append(link_id)

    print("Process: Get ID Finished.")
    return id_list