#!/usr/bin/python
# encoding: utf-8

"""

网易云音乐API

"""

import os
import time
import re
import hashlib
import json
import urllib
import requests
import base64
from Crypto.Cipher import AES
from mutagen.id3 import ID3, TRCK, TIT2, TALB, TPE1, TDRC, COMM, TPOS

playlist_api = "http://music.163.com/api/playlist/detail?id=%s&ids=%s"
song_url = 'http://music.163.com/discover/toplist?id=60198'


class NetEaseApi(object):
    def __init__(self):
        header = {
            'Accept': '*/*',
            'Accept-Encoding': 'text/html',
            'Accept-Language': 'en-US,en;zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko)'
        }
        toplist_id = re.search(r'toplist.+?(\d+)', song_url)
        self.playlist_id = toplist_id.group(1)

        self.ss = requests.Session()
        self.ss.cookies.update(header)

        self.url_dict = {}

        self.database = None
        conf_dir = os.path.join(os.path.expanduser('~'), '.billboard-player')
        self.cookie_path = os.path.join(conf_dir, 'cookie')
        self.storage_path = os.path.join(conf_dir, 'database.json')
        self.default_timeout = 10

    def encrypted_id(self, id):
        byte1 = bytearray('3go8&$8*3*3h0k(2)2')
        byte2 = bytearray(id)
        byte1_len = len(byte1)
        for i in xrange(len(byte2)):
            byte2[i] = byte2[i] ^ byte1[i % byte1_len]
        m = hashlib.md5()
        m.update(byte2)
        result = m.digest().encode('base64')[:-1]
        result = result.replace('/', '_')
        result = result.replace('+', '-')
        return result

    def modificate_text(self, text):
        text = parser.unescape(text)
        text = re.sub(r'//*', '-', text)
        text = text.replace('/', '-')
        text = text.replace('\\', '-')
        text = re.sub(r'\s\s+', ' ', text)
        return text

    def get_url_list(self):
        j = self.ss.get(
            playlist_api % (
                self.playlist_id, urllib.quote('[%s]' % self.playlist_id)
            )
        ).json()

        for i in j['result']['tracks']:
            song_info = {}
            song_info['id'] = i['id']
            song_info['song_url'] = u'http://music.163.com/song/%s' % i['id']
            song_info['durl'], song_info['mp3_quality'] = self.get_durl(i)
            name = re.sub(r'\(.*\)', '', i['name']).strip().lower()

            self.url_dict[name] = song_info
        return self.url_dict

    # def download_music(self):
    #     pass
    #
    # def download_list(self):
    #     pass
    #
    # def set_download_directory(self):
    #     pass

    def get_durl(self, i):
        for q in ('hMusic', 'mMusic', 'lMusic'):
            if i[q]:
                dfsId = str(i[q]['dfsId'])
                edfsId = self.encrypted_id(dfsId)
                durl = u'http://m2.music.126.net/%s/%s.mp3' \
                       % (edfsId, dfsId)
                return durl, q[0]
        return None, None

    def modified_id3(self):
        pass

    def get_song_info(self):
        pass


# netease = NetEaseApi()
# l = netease.get_url_list()
# print json.dumps(l, indent=4)
# url = l['Panda']['durl']
# print url
# os.system('mplayer -really-quiet %s' % url)
