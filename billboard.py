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

        main = urwid.Padding(self.menu(u'Pythons', self.choices), left=2, right=2)
        top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                            align='center', width=('relative', 60),
                            valign='middle', height=('relative', 60),
                            min_width=20, min_height=9)
        self.main_loop = urwid.MainLoop(top, palette=self.palette)

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
        main.original_widget = urwid.Filler(urwid.Pile([response,
                                                        urwid.AttrMap(done, None, focus_map='reversed')]))

    def start(self):
        # def exit_on_q(key):
        #     if key in ('q', 'Q'):
        #         raise urwid.ExitMainLoop()
        #
        # placeholder = urwid.SolidFill()
        # loop = urwid.MainLoop(placeholder, self.palette, unhandled_input=exit_on_q)
        # loop.screen.set_terminal_properties(colors=256)
        # loop.widget = urwid.AttrMap(placeholder, 'bg')
        # loop.widget.original_widget = urwid.Filler(urwid.Pile([]))
        #
        # div = urwid.Divider()
        # outside = urwid.AttrMap(div, 'outside')
        # inside = urwid.AttrMap(div, 'inside')
        # txt1 = urwid.Text(('banner', u" song_first "), align='center')
        # txt2 = urwid.Text(('banner', u" song_second "), align='center')
        # streak = urwid.AttrMap(txt1, 'streak')
        # pile = loop.widget.base_widget  # .base_widget skips the decorations
        # for item in [outside, inside, streak, inside, outside]:
        #     pile.contents.append((item, pile.options()))
        #
        # loop.run()

        self.main_loop.run()


def main():
    player = BillBoardPlayer()
    player.start()


# pass


if __name__ == "__main__":
    main()
