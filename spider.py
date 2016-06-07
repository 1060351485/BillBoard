#!/usr/bin/python
# encoding: utf-8

"""

网易云音乐获取音乐 http://music.163.com/#/discover/toplist?id=60198
BillBoard周榜获取榜单 http://www.billboard.com/charts/hot-100


"""

import urllib2
import re
from bs4 import BeautifulSoup

net_ease_url = 'http://music.163.com/#/discover/toplist?id=60198'
billboard_url = 'http://www.billboard.com/charts/hot-100'

# request = urllib2.Request(billboard_url)
response = urllib2.urlopen(billboard_url)
page = response.read()

soup = BeautifulSoup(page, 'html.parser')


last_week = re.findall(r'Last\sWeek:\s([0-9 -]+)</', page)
song_list = re.findall(r'chart-row__song">(.*?)</h2', page.encode('utf-8'))
singer_list = re.findall(r'chart-row__artist.*?Artist\sName">([^0-9]*?)</a', page)

#  song_list = soup.find_all('h2', class_='chart-row__song')
# singer_list = soup.find_all('a', class_='chart-row__artist')
# last_week = soup.find_all('span', class_='chart-row__last-week')

# song_list = re.findall(r'chart-row__song">(.*?)</h2.*?Artist\sName">([^0-9]*?)</a', page)

# print len(last_week)
print len(song_list)
print len(singer_list)


def print_rank(this_rank, last_week):
    if not last_week.isalnum():
        return '--',
    last_rank = int(last_week)
    if last_rank == this_rank:
        return '--',
    elif last_rank > this_rank:
        return 'down:' + str(last_rank - this_rank),
    else:
        return 'up:' + str(this_rank - last_rank),


# for i in range(len(song_list)):
#     # print '%-4d' % (i + 1),
#     # print '%-10s' % print_rank(i + 1, last_week[i]),
#     print '%-30s' % song_list[i].get_text()
#     # print '%-30s' % singer_list[i].strip()
