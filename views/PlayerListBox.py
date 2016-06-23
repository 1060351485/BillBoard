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


class MainWindow(object):
    def __init__(self, json_list, choices, func):
        # data init
        self.json_list = json_list
        self.item_chosen = func
        self.choices = choices

        # main body
        self.list_box = self._get_music_list(choices)
        list_box_padding = urwid.Padding(self.list_box, left=10, right=10)
        top = urwid.Overlay(list_box_padding, self._get_status_bar(None, None, None),
                            align='center', width=('relative', 90),
                            valign='bottom', height=('relative', 90),
                            min_width=20, min_height=20)

        main_frame = urwid.Frame(top, header=self._get_header('header'), footer=self._get_footer('footer'))
        self.main_frame = urwid.AttrMap(main_frame, 'bg')

    # get

    # Initialization
    def _get_header(self, attribute):
        header = '\n\n┬┐ ┬ ┬  ┬   ┬┐ ┌─┐┌─┐┬─┐┬─┐  ┌┬┐┌─┐┬─┐  ┬ ┌─┐┌─┐\n├┴┐│ │  │   ├┴┐│ │├─┤├┬┘│ │   │ │ │├─┘  │ │ ││ │\n┴─┘┴ ┴─┘┴─┘ ┴─┘└─┘┴ ┴┴└─┴─┘   ┴ └─┘┴    ┴ └─┘└─┘\n '
        header_wrap = urwid.Text((attribute, header), align='center')
        return header_wrap

    def _get_status_bar(self, week_col, prog_txt, prog_col):
        current_week = urwid.Text(('header', self.json_list[0]), align='center')
        progress = urwid.Text(('header', 'progress'), align='center')
        net_status = urwid.Text(('header', 'status'), align='center')

        lb = [
            urwid.AttrMap(urwid.Columns([
                urwid.Pile([
                    current_week]),
                urwid.Pile([
                    progress]),
                urwid.Pile([
                    net_status]),
            ]), 'header'),
        ]
        # grid = urwid.GridFlow([current_time, current_week, progress, net_status], 20, 2, 0, 'center')

        list_box = urwid.ListBox(urwid.SimpleListWalker(lb))
        list_box = urwid.Padding(list_box, left=10, right=60)
        return list_box

    def _get_music_list(self, choices):
        body = [urwid.Divider()]
        for c in choices:
            button = PlayerButton(c, None)
            urwid.connect_signal(button, 'click', self.item_chosen, c)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return PlayerListBox(urwid.SimpleFocusListWalker(body))

    def _get_footer(self, attribute):
        footer = (u"Welcome to the Billboard Player! \n "
                  u"   Up ⬆︎ / Down ⬇︎ / Page Up ⬅︎️ / Page Down ︎➡︎\n"
                  u" Play(p) Pause(p) Next(n) Stop(s) Mute(m) Quit(q)")
        footer_wrap = urwid.Text((attribute, footer), align='center')
        return footer_wrap
