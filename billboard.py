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
import re
from views.playerListBox import PlayerListBox
from views.playerListBox import PlayerButton
from views.playerListBox import MainWindow
from model.player.player import Player
from model.spider.billboard_spider import BillBoardSpider
from model.API.netease_api import NetEaseApi

class BillBoardPlayer(object):
    def __init__(self):
        self.main_loop = None
        self.main = None
        self.choices = []  # song list
        self.list_box = None

        # ui color
        self.palette = None
        self.song_color = None
        self.artist_color = None
        self.current_rank_color = None
        self.last_rank_color = None

        # todo: Spider is too slow, block the view! Initialize main window, need to change to logic when start up
        self.spider = BillBoardSpider()
        self.json_list = self.spider.get_latest_list()
        self.json_list = self.spider.read_from_file()

        for i in range(1, 101):
            self.choices.append('%2s. %-10s %10s\n' % (
                self.json_list[i]['this_rank'], self.json_list[i]['song'] + ' / ' + self.json_list[i]['artist'],
                self.json_list[i]['last_rank']))

        # netease music
        nem = NetEaseApi()
        self.song_dict = nem.get_url_list()

        self.music_player = Player()

        self._setup_ui()
        self._setup_signals()

    """
        UI
    """
    def _setup_ui(self):
        # todo: add time, week, playtime, network, PlayListButton
        palette = [
            ('header', 'dark red', ''),
            ('list_btn', '', ''),
            ('list_box', '', ''),
            ('time', '', ''),
            ('week', '', ''),
            ('progress', '', ''),
            ('net_status', '', ''),
            ('footer', 'dark red', ''),
            ('bg', '', '')]

        main_window = MainWindow(self.json_list, self.choices, self.item_chosen)
        self.list_box = main_window.list_box
        self.main_loop = urwid.MainLoop(main_window.main_frame, palette=palette)
        self.main_loop.screen.set_terminal_properties(colors=256)

    def _setup_signals(self):
        urwid.register_signal(PlayerListBox,
                              ['quit', 'next', 'pause', 'stop', 'mute', 'volume_up', 'volume_down'])
        urwid.connect_signal(self.list_box, 'quit', self.on_quit)
        urwid.connect_signal(self.list_box, 'next', self.on_next)
        urwid.connect_signal(self.list_box, 'pause', self.on_pause)
        urwid.connect_signal(self.list_box, 'stop', self.on_stop)
        urwid.connect_signal(self.list_box, 'mute', self.on_mute)
        urwid.connect_signal(self.list_box, 'volume_up', self.on_volume_up)
        urwid.connect_signal(self.list_box, 'volume_down', self.on_volume_down)

    """
         player
    """
    def on_quit(self):
        self.music_player.quit()
        raise urwid.ExitMainLoop()

    def on_next(self):
        self.music_player.next()

    # todo: check validness
    def on_pause(self):
        # if not self.music_player.is_playing:
        # self.music_player.play()
        self.music_player.pause()

    def on_stop(self):
        self.music_player.stop()

    def on_mute(self):
        self.music_player.mute()

    def on_volume_up(self):
        self.music_player.volume_up()

    def on_volume_down(self):
        self.music_player.volume_down()

    def item_chosen(self, button, choice):

        # print choice
        name = re.findall(r'.\s(.*?)\s/\s', choice)[0]
        name = name.lower()
        if name in self.song_dict and 'durl' in self.song_dict[name]:
            self.music_player.play(self.song_dict[name]['durl'])
            print '------------------'
        else:
            pass
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
