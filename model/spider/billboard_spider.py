#!/usr/bin/python
# encoding: utf-8

"""

get the latest billboard chart from www.billboard.com

NetEase Music           http://music.163.com/#/discover/toplist?id=60198
BillBoard The Hot 100   http://www.billboard.com/charts/hot-100


"""
import os
import urllib2
import re
import json
from bs4 import BeautifulSoup

net_ease_url = 'http://music.163.com/#/discover/toplist?id=60198'
billboard_url = 'http://www.billboard.com/charts/hot-100'


class BillBoardSpider(object):
    def __init__(self):

        # declare
        self.url = billboard_url
        self.net_status = False

        self.net_response = None
        # put information into json and write it to a file
        self.json_list = None
        self.file_name = 'billboard_list.json'

        # do all the actions in this function
        self.get_latest_list()

    def _check_internet_on(self):
        try:
            self.net_response = urllib2.urlopen(self.url, timeout=1)
            return True
        except urllib2.URLError as err:
            pass
        return False

    # Must call _check_internet_on first(to get the response)
    def _check_is_latest(self, date_time):

        # if file exists, load it, else load from the internet
        if not os.path.exists(self.file_name):
            return False
        # get old time from file

        json_file = file(self.file_name)
        billboard_list = json.load(json_file)

        if billboard_list[0] == date_time:
            self.json_list = billboard_list
            return True
        else:
            return False

    """

    if your list is the latest , do nothing
    otherwise get the latest list

    """

    def get_latest_list(self):

        # check network connection first
        self.net_status = self._check_internet_on()
        if not self.net_status:
            print "Can't access to www.billboard.com. Please check you network connection."
            return

        # Get datetime from the internet
        page = self._get_response_page()
        soup_page = BeautifulSoup(page, 'html.parser')

        date_time = soup_page.find('time').get_text()

        # check if there is a new list
        if self._check_is_latest(date_time):
            return

        # todo: single quote were changed to &#039;
        # song_list = re.findall(r'chart-row__song">([a-Z]*?)</h2', page)
        # singer_list = re.findall(r'chart-row__artist.*?Artist\sName">([^0-9]*?)</a', page)

        last_week = re.findall(r'Last\sWeek:\s([0-9 -]+)</', page)
        song_list = soup_page.find_all('h2', class_='chart-row__song')
        singer_list = soup_page.find_all('a', class_='chart-row__artist')

        # Write the list to file
        self._save_to_json(date_time, last_week, song_list, singer_list)
        self._write_to_file()

    def _save_to_json(self, date_time, last_week, song_list, singer_list):
        json_list = [date_time]
        for i in range(len(song_list)):
            dic = dict()
            dic['last_rank'] = self._print_rank(i + 1, last_week[i])
            dic['this_rank'] = str(i + 1)
            dic['artist'] = singer_list[i].get_text().strip()
            dic['song'] = song_list[i].get_text()
            json_list.append(dic)
        self.json_list = json_list

    def _write_to_file(self):
        file_object = open(self.file_name, 'w')
        file_object.write(str(json.dumps(self.json_list)))
        file_object.close()

    def read_from_file(self):
        json_file = file(self.file_name)
        self.json_list = json.load(json_file)

    def _get_response_page(self):
        return self.net_response.read()

    def print_list(self):
        print self.json_list[0]
        for i in range(1, 101):
            print '%-8s' % self.json_list[i]['last_rank'],
            print '%3s  ' % self.json_list[i]['this_rank'],
            print '%-40s' % self.json_list[i]['song'],
            print '%-20s' % self.json_list[i]['artist']

    def _print_rank(self, this_rank, last_week):
        if not last_week.isalnum():
            return '--'
        last_rank = int(last_week)
        if last_rank == this_rank:
            return '--'
        elif last_rank > this_rank:
            return 'up:' + str(last_rank - this_rank)
        else:
            return 'down:' + str(this_rank - last_rank)

    def get_billboard_list(self):
        return self.json_list


# spider = BillBoardSpider()
# spider.print_list()
# billboard_list = spider.get_billboard_list()
# print billboard_list
