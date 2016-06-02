#!/usr/bin/python
# encoding: utf-8

"""

网易云音乐BillBoard周榜

"""

import urllib2

url = 'http://music.163.com/#/discover/toplist?id=60198'

request = urllib2.Request(url)
response = urllib2.urlopen(request)
page = response.read()

print page
