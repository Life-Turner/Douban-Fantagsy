#-*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
import json
import mysql.connector

conn = mysql.connector.connect(host = '127.0.0.1',
                              user = 'root',
                              password = 'D0more&t4lkless',
                              database = 'douban',
                              )

cur = conn.cursor()
cur.execute('USE douban')

# tag_name = "商业"
id_list = []

#To get books' id
id_pattern = re.compile(r'\d+')

def store_info(dbid, title, raters, average, subtitle, chi_title, my_index):
    cur.execute('INSERT INTO books (dbid, title, raters, average, subtitle, chi_title, my_index) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                (int(dbid), title, int(raters), average, subtitle, chi_title, my_index))
    conn.commit()

def get_info(dbid):
    #Some User Agents
    session = requests.Session()
    headers = {'User-Agent':
               'Mozilla/5.0 (Windows; U; Windows NT 6.1;'\
               ' en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

    info_index = 0

    for single_id in dbid:
        # html = r'https://api.douban.com/v2/'\
        # 'book/{single_id}'.format(single_id = single_id)
        html = r'https://douban.uieee.com/v2/'\
        'book/{single_id}'.format(single_id = single_id)
        req = session.get(html, headers = headers)
        time.sleep(3)
        object_info = json.loads(req.text)

        #Process Informer
        info_index += 1
        print(info_index)
        #Get Douban ID
        the_dbid = single_id
        #Get Original Title
        if "origin_title" in object_info:
            title = object_info["origin_title"]
        else:
            title = ''
        #Get Rating's info
        if 'rating' in object_info:
            average = float(object_info["rating"]["average"])
            raters = object_info["rating"]["numRaters"]
        else:
            average = 0
            raters = 0
        #Get Subtitle
        if 'subtitle' in object_info:
            subtitle = object_info["subtitle"]
        else:
            subtitle = ''
        #Get chinese title
        if 'title' in object_info:
            chi_title = object_info["title"]
        else:
            chi_title = ''

        store_info(the_dbid, title, raters, average, subtitle, chi_title, info_index)


def get_book_ID(tag_name):

    #Some User Agents
    session = requests.Session()
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

    for page_num in range(50):
        number = page_num * 20   
        html = r"https://book.douban.com/tag/{tag_name}"\
                        "?start={number}&type=T".format(tag_name = tag_name, number = number)
        print(html)
        req = session.get(html, headers = headers)
        time.sleep(3)

        bs = BeautifulSoup(req.text, "html.parser")

        link_list = bs.select('h2 a')

        for link in link_list:
            link_href = link.get('href')
            link_id = id_pattern.search(link_href).group()
            id_list.append(link_id)

    final_id_list = set(id_list)
    get_info(final_id_list)

    print("Hooray! My program succeeded!")

if __name__ == "__main__":
    tag_name = input("Please enter the tag of books: ")
    get_book_ID(tag_name)