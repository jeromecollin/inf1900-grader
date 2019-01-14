from re import sub

from urwid import Edit, LineBox, Pile, RadioButton, Text, WidgetWrap, emit_signal

from src.util.dlist import Dlist
from src.views.base.signal import Signal


class RadioGroup(WidgetWrap):
    def __init__(self, enum_type, starting_value):
        self.selected_value = starting_value
        self.enum_type = enum_type

        self.radio_group = []
        for choice in enum_type:
            RadioButton(self.radio_group,
                        label=choice.name.capitalize(),
                        state=choice is starting_value)

        radio_title = sub(r"(\w)([A-Z])", r"\1 \2", enum_type.__name__).capitalize()

        super().__init__(LineBox(Pile([Text(("header", radio_title)), *self.radio_group])))

    def get_data(self):
        for radio in self.radio_group:
            if radio.state:
                return self.enum_type[radio.label.upper()]


@Signal("on_flush")
class MiniBuffer(Edit):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.history = Dlist("")
        self.current = self.history

        self.keybind = {
            "enter" : self.flush,
            "ctrl p": self.previous_history,
            "ctrl n": self.next_history,
            "ctrl r": self.reverse_i_search
        }

    def flush(self):

        txt = self.get_edit_text()

        if txt != self.current.prev.data:
            self.current.data = txt
            self.current.add(Dlist(""))
            self.current = self.current.next
        else:
            self.current.data = ""

        self.history = self.current

        self.set_edit_text("")

        emit_signal(self, "on_flush", self.get_last_text())

    def previous_history(self):
        self.history.data = self.get_edit_text()
        self.history = self.history.prev
        self.update_text(self.history.data)

    def next_history(self):
        self.history.data = self.get_edit_text()
        self.history = self.history.next
        self.update_text(self.history.data)

    def reverse_i_search(self):
        # TODO: https://docs.python.org/3.7/library/readline.html
        pass

    def update_text(self, text):
        self.set_edit_text(text)
        self.set_edit_pos(len(text))

    def get_last_text(self):
        return self.current.prev.data
