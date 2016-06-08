#!/usr/bin/python
# encoding: utf-8

# """
#
# 顶层文件
#
# """


import urwid
from views.playerListBox import PlayerListBox
from model.player.player import Player


class BillBoardPlayer(object):
    def __init__(self):
        self.palette = None
        self.main_loop = None
        self.main = None
        self.choices = u'you 2 3 Idle Jones Palin'.split()
        self.list_box = None

        self.music_player = Player()

        self._setup_ui()
        self._setup_signals()

    def _setup_ui(self):
        self.palette = [
            ('banner', '', '', '', '#ffa', '#60d'),
            ('streak', '', '', '', 'g50', '#60a'),
            ('inside', '', '', '', 'g38', '#808'),
            ('outside', '', '', '', 'g27', '#a06'),
            ('bg', '', '', '', 'g7', '#d06'), ]
        self.list_box = self.get_music_list(u'Music List', self.choices)

        self.main = urwid.Padding(self.list_box, left=10, right=2)
        top = urwid.Overlay(self.main, urwid.SolidFill(u'%'),
                            align='left', width=('relative', 60),
                            valign='middle', height=('relative', 60),
                            min_width=20, min_height=9)
        self.main_loop = urwid.MainLoop(top)  # , palette=self.palette)

    def _setup_signals(self):
        urwid.register_signal(PlayerListBox, ['quit', 'next', 'pause', 'stop', 'mute', 'volume_up', 'volume_down'])
        urwid.connect_signal(self.list_box, 'quit', self.on_quit)
        urwid.connect_signal(self.list_box, 'next', self.on_next)
        urwid.connect_signal(self.list_box, 'pause', self.on_pause)
        urwid.connect_signal(self.list_box, 'stop', self.on_stop)
        urwid.connect_signal(self.list_box, 'mute', self.on_mute)
        urwid.connect_signal(self.list_box, 'volume_up', self.on_volume_up)
        urwid.connect_signal(self.list_box, 'volume_down', self.on_volume_down)

    def on_quit(self):
        self.music_player.quit()
        raise urwid.ExitMainLoop()

    def on_next(self):
        self.music_player.next()

    def on_pause(self):
        self.music_player.pause()

    def on_stop(self):
        self.music_player.stop()

    def on_mute(self):
        self.music_player.mute()

    def on_volume_up(self):
        self.music_player.volume_up()

    def on_volume_down(self):
        self.music_player.volume_down()

    def get_music_list(self, title, choices):
        body = [urwid.Text(title), urwid.Divider()]
        for c in choices:
            button = urwid.Button(c)
            urwid.connect_signal(button, 'click', self.item_chosen, c)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return PlayerListBox(urwid.SimpleFocusListWalker(body))

    def item_chosen(self, button, choice):
        # print choice
        self.music_player.play(choice + '.mp3')
        # response = urwid.Text([u'You chose ', choice, u'\n'])
        # done = urwid.Button(u'Ok')
        # urwid.connect_signal(done, 'click', self.exit_program)
        # self.main.original_widget = urwid.Filler(urwid.Pile([response,
        #                                                 urwid.AttrMap(done, None, focus_map='reversed')]))

    def start(self):
        self.main_loop.run()


def main():
    BBplayer = BillBoardPlayer()
    BBplayer.start()


if __name__ == "__main__":
    main()
