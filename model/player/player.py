#!/usr/bin/python
# encoding: utf-8

# """
#
# 音乐播放
#
# """

import subprocess
import Queue
import platform
import os


class Player(object):
    def __init__(self):
        self.is_playing = False
        self.is_quit = True
        self.current_playing = None
        self.loop_one_song = False
        self.loop_all = False
        self.subprocess = None
        self.music_url = os.getcwd()
        self.queue = Queue.Queue()
        self.platfrom = platform.system()
        self.error_handle = open(self.music_url + '/model/player/' + 'tmp.log', 'wt')
        # print self.platfrom
        # print platform.release()

    def play(self, name):
        if self.is_playing:
            self.subprocess.kill()
        if self.platfrom == 'Darwin':
            self.subprocess = subprocess.Popen(['mplayer', '-really-quiet', self.music_url + name],
                                               stdin=subprocess.PIPE,
                                               stderr=self.error_handle)
        self.is_playing = True
        self.current_playing = name

    def stop(self):
        if self.subprocess:
            self.subprocess.kill()
        self.is_playing = False

    def pause(self):
        if self.is_playing:
            self.subprocess.stdin.write(u'p')
        self.is_playing = not self.is_playing

    def mute(self):
        if self.is_playing:
            self.subprocess.stdin.write(u'm')

    def volume_up(self):
        if self.is_playing:
            self.subprocess.stdin.write(u'0')

    def volume_down(self):
        if self.is_playing:
            self.subprocess.stdin.write(u'9')

    def close(self):
        pass

    def next(self):
        pass

    def quit(self):
        self.stop()
        self.is_quit = True
        subprocess.call('echo -e "\033[?25h";clear', shell=True)
