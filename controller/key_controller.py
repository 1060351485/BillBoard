#!/usr/bin/python
# encoding: utf-8

"""

处理命令输入

"""

import Queue


class KeyController(object):
    def __init__(self, player):
        self.player = player
        self.input_queue = Queue.Queue()

    # def start