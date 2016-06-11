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
from views.playerListBox import PlayerButton
from model.player.player import Player
from model.spider.billboard_spider import BillBoardSpider


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

        # todo: Spider is too slow, block the view! Initialize main window
        self.spider = BillBoardSpider()
        self.json_list = self.spider.read_from_file()

        for i in range(1, 101):
            self.choices.append('%2s. %-10s %10s\n' % (
                self.json_list[i]['this_rank'], self.json_list[i]['song'] + ' / ' + self.json_list[i]['artist'],
                self.json_list[i]['last_rank']))

        self.music_player = Player()

        self._setup_ui()
        self._setup_signals()

    def _setup_ui(self):
        # todo: add time, week, playtime, network, PlayListButton

        def get_music_list(choices):
            body = [urwid.Divider()]
            for c in choices:
                button = PlayerButton(c, None)
                urwid.connect_signal(button, 'click', self.item_chosen, c)
                body.append(urwid.AttrMap(button, None, focus_map='reversed'))
            return PlayerListBox(urwid.SimpleFocusListWalker(body))

        def get_header(attribute):
            header = '\n\n┬┐ ┬ ┬  ┬   ┬┐ ┌─┐┌─┐┬─┐┬─┐  ┌┬┐┌─┐┬─┐  ┬ ┌─┐┌─┐\n├┴┐│ │  │   ├┴┐│ │├─┤├┬┘│ │   │ │ │├─┘  │ │ ││ │\n┴─┘┴ ┴─┘┴─┘ ┴─┘└─┘┴ ┴┴└─┴─┘   ┴ └─┘┴    ┴ └─┘└─┘\n '
            header_wrap = urwid.Text((attribute, header), align='center')
            return header_wrap

        def get_footer(attribute):
            footer = (u"Welcome to the Billboard Player! \n "
                      u"   Up ⬆︎ / Down ⬇︎ / Page Up ⬅︎️ / Page Down ︎➡︎\n"
                      u" Play(p) Pause(p) Next(n) Stop(s) Mute(m) Quit(q)")
            footer_wrap = urwid.Text((attribute, footer), align='center')
            return footer_wrap

        # tim_col, wek_col, prog_col, net_col, time_txt, week_txt
        def get_status_bar():
            current_time = urwid.Text(('header', 'current_time'), align='center')
            current_week = urwid.Text(('header', 'current_week'), align='center')
            progress = urwid.Text(('header', 'progress'), align='center')
            net_status = urwid.Text(('header', 'status'), align='center')

            lb = [
                urwid.AttrMap(urwid.Columns([
                    urwid.Pile([
                        current_time]),
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
            return list_box

        self.palette = [
            ('header', 'dark red', ''),
            ('list_btn', '', ''),
            ('list_box', '', ''),
            ('time', '', ''),
            ('week', '', ''),
            ('progress', '', ''),
            ('net_status', '', ''),
            ('footer', 'dark red', ''),
            ('bg1', '', '', '', '', 'g23'),
            ('bg2', '', '')]

        self.list_box = get_music_list(self.choices)

        list_box_padding = urwid.Padding(self.list_box, left=10, right=10)

        top = urwid.Overlay(list_box_padding, get_status_bar(),
                            align='center', width=('relative', 90),
                            valign='bottom', height=('relative', 90),
                            min_width=20, min_height=20)

        main_frame = urwid.Frame(top, header=get_header('header'), footer=get_footer('footer'))

        main_frame_attribute = urwid.AttrMap(main_frame, 'bg2')
        self.main_loop = urwid.MainLoop(main_frame_attribute, palette=self.palette)
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
