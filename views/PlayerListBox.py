#!/usr/bin/python
# encoding: utf-8

# """
#
# 歌曲选单
#
# """

import urwid


# todo: need to add more attributes
class PlayerButton(urwid.Button):
    def __init__(self, text_list, color_list):
        super(PlayerButton, self).__init__("")
        self._text = urwid.SelectableIcon([u'\N{BULLET} ', text_list], 0)
        self._w = urwid.AttrMap(self._text, None, focus_map='selected')

    @property
    def text(self):
        return self._text.text

    def set_text(self, text):
        self._text.set_text(text)


class PlayerListBox(urwid.ListBox):
    def __init__(self, body):
        super(PlayerListBox, self).__init__(body)
        # self._command_map['q'] = 'quit'
        # self._command_map['Q'] = 'quit'
        self._command_map['right'] = 'cursor page down'
        self._command_map['left'] = 'cursor page up'
        # self._command_map['>'] = 'cursor page down'
        # self._command_map['.'] = 'cursor page down'
        # self._command_map['n'] = 'next'
        # self._command_map['N'] = 'next'

    def keypress(self, size, key):
        if key in ('up', 'down', 'right', 'left', 'enter'):
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
        elif key in ('{', '['):
            urwid.emit_signal(self, 'volume_down')
        elif key in ('}', ']'):
            urwid.emit_signal(self, 'volume_up')

