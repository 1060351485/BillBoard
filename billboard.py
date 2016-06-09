#!/usr/bin/python
# encoding: utf-8

# """
#
#   ┬┐ ┬ ┬  ┬   ┬┐ ┌─┐┌─┐┬─┐┬─┐  ┌┬┐┌─┐┬─┐   ┬ ┌─┐┌─┐
#   ├┴┐│ │  │   ├┴┐│ │├─┤├┬┘│ │   │ │ │├─┘   │ │ ││ │
#   ┴─┘┴ ┴─┘┴─┘ ┴─┘└─┘┴ ┴┴└─┴─┘   ┴ └─┘┴     ┴ └─┘└─┘
#
# """


import urwid
from views.playerListBox import PlayerListBox
from model.player.player import Player
from model.spider.billboard_spider import BillBoardSpider


class BillBoardPlayer(object):
    def __init__(self):
        self.palette = None
        self.main_loop = None
        self.main = None
        self.choices = []  # song list
        self.list_box = None

        # todo: Spider is too slow, block the view! Initialize main window
        self.spider = BillBoardSpider()
        self.json_list = self.spider.read_from_file()

        for i in range(1, 101):
            self.choices.append('%2s. %-10s %10s' % (
                self.json_list[i]['this_rank'], self.json_list[i]['song'] + ' / ' + self.json_list[i]['artist'],
                self.json_list[i]['last_rank']))

        self.music_player = Player()

        self._setup_ui()
        self._setup_signals()

    def _setup_ui(self):

        self.palette = [
            ('header', 'yellow', ''),
            ('list_btn', '', ''),
            ('list_box', '', ''),
            ('net_status', '', ''),
            ('footer', 'yellow', ''), ]

        header = '\n\n┬┐ ┬ ┬  ┬   ┬┐ ┌─┐┌─┐┬─┐┬─┐  ┌┬┐┌─┐┬─┐  ┬ ┌─┐┌─┐\n├┴┐│ │  │   ├┴┐│ │├─┤├┬┘│ │   │ │ │├─┘  │ │ ││ │\n┴─┘┴ ┴─┘┴─┘ ┴─┘└─┘┴ ┴┴└─┴─┘   ┴ └─┘┴    ┴ └─┘└─┘\n '

        header_wrap = urwid.Text(('header', header), align='center')

        footer = (u"Welcome to the Billboard Player!  "
                  u"UP / DOWN / PAGE UP / PAGE DOWN scroll.  'q' exits.")
        footer_wrap = urwid.Text(('footer', footer), align='center')

        self.list_box = self.get_music_list(self.choices)
        list_box_padding = urwid.Padding(self.list_box, left=10, right=10)

        top = urwid.Overlay(list_box_padding, urwid.SolidFill(),
                            align='left', width=('relative', 90),
                            valign='middle', height=('relative', 80),
                            min_width=20, min_height=9)

        main_frame = urwid.Frame(top, header=header_wrap, footer=footer_wrap)

        self.main_loop = urwid.MainLoop(main_frame, palette=self.palette)

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

    def get_music_list(self, choices):
        body = [urwid.Divider()]
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
