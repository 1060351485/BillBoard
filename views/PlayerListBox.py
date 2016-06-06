#!/usr/bin/python
# encoding: utf-8

# """
#
# 歌曲选单
#
# """

import urwid


class PlayerListBox(urwid.ListBox):
    def __init__(self, body):
        super(PlayerListBox, self).__init__(body)

    def keypress(self, size, key):
        if key in ('up', 'down', 'page up', 'page down', 'enter'):
            super(PlayerListBox, self).keypress(size, key)
        elif key in ('n', 'N'):
            urwid.emit_signal(self, 'next')
        elif key in ('P', 'p'):
            urwid.emit_signal(self, 'pause')
        elif key in ('q', 'Q'):
            urwid.emit_signal(self, 'quit')
        elif key in ('s', 'S'):
            urwid.emit_signal(self, 'stop')
        elif key in ('m', 'M'):
            urwid.emit_signal(self, 'mute')
        elif key == '9':
            urwid.emit_signal(self, 'volume_down')
        elif key == '0':
            urwid.emit_signal(self, 'volume_up')
