#!/usr/bin/python
# encoding: utf-8

"""

网易云音乐获取音乐 http://music.163.com/#/discover/toplist?id=60198
BillBoard周榜获取榜单 http://www.billboard.com/charts/hot-100


"""
import os
import urllib2
import re
from bs4 import BeautifulSoup

# todo: need to detect net status when start up
net_ease_url = 'http://music.163.com/#/discover/toplist?id=60198'
billboard_url = 'http://www.billboard.com/charts/hot-100'
billboard_ip = '68.232.44.101'

return1 = os.system('ping '+billboard_ip)
if return1:
    print 'yes'
else:
    print 'np'

class BillBoardSpider(object):
    def __init__(self):
        self.url = billboard_url
        self.net_status = False
        self.is_latest = False
        self.date_time = ""

    def network_status(self):
        pass

    def is_latest(self):
        pass

    def get_lastest_list(self):
        pass

    def write_to_file(self, file_wt_name):
        pass

    def read_from_file(self, file_rd_name):
        pass


response = urllib2.urlopen(billboard_url)
page = response.read()

soup = BeautifulSoup(page, 'html.parser')

# todo: single quote were changed to &#039;
# song_list = re.findall(r'chart-row__song">([a-Z]*?)</h2', page)
# singer_list = re.findall(r'chart-row__artist.*?Artist\sName">([^0-9]*?)</a', page)

date_time = soup.find('time')
last_week = re.findall(r'Last\sWeek:\s([0-9 -]+)</', page)
song_list = soup.find_all('h2', class_='chart-row__song')
singer_list = soup.find_all('a', class_='chart-row__artist')

print len(song_list)
print len(singer_list)


def print_rank(this_rank, last_week):
    if not last_week.isalnum():
        return '--',
    last_rank = int(last_week)
    if last_rank == this_rank:
        return '--',
    elif last_rank > this_rank:
        return 'up:'+str(last_rank - this_rank),
    else:
        return 'down:'+str(this_rank - last_rank),


# todo: write result to a file

file_object = open('thefile.txt', 'w')
file_object.write(date_time.get_text()+'\n')

print date_time.get_text()
for i in range(len(song_list)):

    # print '%-8s' % print_rank(i + 1, last_week[i]),
    # print '%3d  ' % (i + 1),
    # print '%-40s' % song_list[i].get_text(),
    # print '%-20s' % singer_list[i].get_text().strip()
    file_object.write('%-8s' % print_rank(i + 1, last_week[i]))
    file_object.write('%3d  ' % (i + 1))
    file_object.write('%-40s' % song_list[i].get_text())
    file_object.write('%-20s\n' % singer_list[i].get_text().strip())

file_object.close()
