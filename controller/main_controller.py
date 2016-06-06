#!/usr/bin/python
# encoding: utf-8

"""

控制器

"""

import definitions
import threading


class MainController(object):
    def __init__(self, player, data, queue):
        self.music_player = player
        self.data = data
        self.queue = queue
        self.quit = False

        threading.Thread(target=self._key_input).start()

    def send_message(self):
        pass

    def _key_input(self):
        while not self.quit:
            key = self.queue.get()
            if key == definitions.KEYS['Quit']:
                # self.music_player.quit()
                pass
