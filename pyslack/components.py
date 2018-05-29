import urwid

options = {
    'icons': {
        'channel': '\uF198',
        'divider': '\uE0B1',
        'full_divider': '\uE0B0',
        'full_star': '\uF005',
        'keyboard': '\uF11C',
        'line_star': '\uF006',
        'person': '\uF415',
        'private_channel': '\uF023'
    }
}

class BreadCrumbs(urwid.Text):
    def intersperse(self, iterable, delimiter):
        it = iter(iterable)
        yield next(it)
        for elem in it:
            yield delimiter
            yield elem

    def __init__(self, elements=[]):
        separator = ('separator', ' {} '.format(options['icons']['divider']))
        body = list(self.intersperse(elements, separator))
        super(BreadCrumbs, self).__init__([' '] + body)

class Channel(urwid.AttrMap):
    def __init__(self, name, is_private=False):
        icon = ' · ' if is_private else '\uF023'
        body = urwid.SelectableIcon(' {} {}'.format(
            options['icons']['private_channel' if is_private else 'channel'],
            name
        ))
        super(Channel, self).__init__(body, None, 'active_channel')

class ChannelHeader(urwid.Pile):
    def __init__(self, date, topic, num_members, name, is_private=False, starred=False):
        star_icon = options['icons']['full_star' if starred else 'line_star']
        body = [
            TextDivider(' {} {}'.format(
                options['icons']['private_channel' if is_private else 'channel'],
                name
            )),
            BreadCrumbs([
                star_icon,
                '{} {}'.format(options['icons']['person'], num_members),
                topic
            ]),
            TextDivider(('history_date', date), align='center')
        ]
        super(ChannelHeader, self).__init__(body)

class ChatBox(urwid.Frame):
    def __init__(self, messages, header, message_box):
        body = urwid.ListBox(urwid.SimpleFocusListWalker(messages))
        super(ChatBox, self).__init__(body, header=header, footer=message_box)

class Message(urwid.Columns):
    def __init__(self, time, user, edited=False):
        time_column = urwid.Text(('datetime', ' {} │'.format(time)))
        edited_column = urwid.Text(('edited', ' (edited) ' if edited else ''))
        super(Message, self).__init__([
            ('fixed', 8, time_column),
            urwid.Text(user),
            ('fixed', 10, edited_column)
        ])

class MessageBox(urwid.Pile):
    def __init__(self, user, typing=None):
        if typing != None:
            top_separator = TextDivider(('is_typing', '{} {} is typing...'.format(
                options['icons']['keyboard'],
                typing
            )))
        else:
            top_separator = urwid.Divider('─')
        prompt = urwid.Edit(('prompt', [
            ' ', user, ('prompt_arrow', options['icons']['full_divider'] + ' ')
        ]))
        body = [
            top_separator,
            prompt,
            urwid.Divider('─')
        ]
        super(MessageBox, self).__init__(body)

class SideBar(urwid.Frame):
    def __init__(self, channels=[], title=''):
        header = TextDivider(title)
        footer = urwid.Divider('─')
        empty_line = urwid.Divider(' ')
        self.listbox = urwid.ListBox(urwid.SimpleFocusListWalker([
            empty_line,
            TextDivider('Channels')
        ] + channels))
        super(SideBar, self).__init__(self.listbox, header=header, footer=footer)

class TextDivider(urwid.Columns):
    def __init__(self, text='', align='left', char='─'):
        text_size = len(text if isinstance(text, str) else text[1]) + 2
        text_widget = ('fixed', text_size, urwid.Text(text, align='center'))
        if align == 'right':
            body = [
                urwid.Divider(char),
                text_widget,
                ('fixed', 1, urwid.Divider(char))
            ]
        elif align == 'center':
            body = [
                urwid.Divider(char),
                text_widget,
                urwid.Divider(char)
            ]
        else:
            body = [
                ('fixed', 1, urwid.Divider(char)),
                text_widget,
                urwid.Divider(char)
            ]
        super(TextDivider, self).__init__(body)
