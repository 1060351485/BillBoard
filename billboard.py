#!/usr/bin/python
# encoding: utf-8

# """
#
# 顶层文件
#
# """

import urwid


class BillBoardPlayer(object):
    def __init__(self):
        self.palette = None
        self.main_loop = None
        self.main = None
        self.choices = u'Chapman Cleese Gilliam Idle Jones Palin'.split()

        self._setup_ui()
        self._setup_signals()

    def _setup_ui(self):
        self.palette = [
            ('banner', '', '', '', '#ffa', '#60d'),
            ('streak', '', '', '', 'g50', '#60a'),
            ('inside', '', '', '', 'g38', '#808'),
            ('outside', '', '', '', 'g27', '#a06'),
            ('bg', '', '', '', 'g7', '#d06'), ]

        self.main = urwid.Padding(self.menu(u'Music List', self.choices), left=10, right=2)
        top = urwid.Overlay(self.main, urwid.SolidFill(),
                            align='left', width=('relative', 60),
                            valign='middle', height=('relative', 60),
                            min_width=20, min_height=9)
        self.main_loop = urwid.MainLoop(top)#, palette=self.palette)

    def _setup_signals(self):
        pass
        # urwid.register_signal()
        # urwid.connect_signal(exit, 'exit', self.on_exit)

    def on_exit(self):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def exit(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def menu(self, title, choices):
        body = [urwid.Text(title), urwid.Divider()]
        for c in choices:
            button = urwid.Button(c)
            urwid.connect_signal(button, 'click', self.item_chosen, c)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def exit_program(self, button):
        raise urwid.ExitMainLoop()

    def item_chosen(self, button, choice):
        response = urwid.Text([u'You chose ', choice, u'\n'])
        done = urwid.Button(u'Ok')
        urwid.connect_signal(done, 'click', self.exit_program)
        self.main.original_widget = urwid.Filler(urwid.Pile([response,
                                                        urwid.AttrMap(done, None, focus_map='reversed')]))

    def start(self):
        self.main_loop.run()


def main():
    player = BillBoardPlayer()
    player.start()


if __name__ == "__main__":
    main()
