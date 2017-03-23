#!/usr/bin/python
# encoding: utf-8

# """
#
#  music player
#
# """

import subprocess
import Queue
import platform
import os
import logging

class Player(object):
    def __init__(self):
        # todo: add a playlist to support next song, and show playing status
        # maybe in the condition that player is playing but it is paused
        self.is_playing = False
        self.is_pause = False
        self.is_quit = True
        self.volume = -5
        self.current_playing = None
        self.loop_one_song = True
        self.loop_all = False
        self.subprocess = None
        self.music_url = os.getcwd()
        self.queue = Queue.Queue()
        self.platfrom = platform.system()
        self.error_handle = open(self.music_url + '/model/player/' + 'player.log', 'wt')
        # print self.platfrom
        # print platform.release()

    def play(self, name, song_url):
        logging.debug("play")
        if self.is_playing:
            self.subprocess.kill()
        if self.platfrom == 'Darwin':
            self.subprocess = subprocess.Popen(['mplayer', '-really-quiet', song_url, '-af', 'volume=%d' % self.volume],
                                               stdin=subprocess.PIPE,
                                               stderr=self.error_handle)
        self.is_playing = True
        self.is_pause = False
        self.current_playing = name

    def stop(self):
        if self.subprocess:
            self.subprocess.kill()
        self.is_playing = False

    def pause(self):
        if self.is_playing:
            self.subprocess.stdin.write(u'p')
            self.is_pause = not self.is_pause

    def mute(self):
        if self.is_playing:
            self.subprocess.stdin.write(u'm')

    def volume_up(self):
        if self.is_playing:
            self.subprocess.stdin.write(u'0')
            self.volume += 0.5

    def volume_down(self):
        if self.is_playing:
            self.subprocess.stdin.write(u'9')
            self.volume += -0.5

    def next_song(self):
        pass

    def quit(self):
        self.stop()
        self.is_quit = True
        subprocess.call('echo -e "\033[?25h";clear', shell=True)
