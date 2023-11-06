# pylint: disable=C0103
# pylint: disable=W0612
# pylint: disable=C0116
# pylint: disable=C0115
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window import MainWindow


class MsgBox:
    def __init__(self, window: "MainWindow") -> None:
        self.window = window

    def make_dialog(self, text):
        msg_box = self.window.make_msg_box()
        msg_box.setText(text)
        return msg_box

    def show_error(self, text):
        msg_box = self.make_dialog(text)
        msg_box.setIcon(msg_box.Icon.Critical)
        msg_box.exec()

    def show_info(self, text):
        msg_box = self.make_dialog(text)
        msg_box.setIcon(msg_box.Icon.Information)
        msg_box.exec()
