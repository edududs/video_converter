# pylint: disable=C0103
# pylint: disable=W0612
from typing import TYPE_CHECKING

import qdarktheme
from moviepy.editor import VideoFileClip
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QComboBox, QFileDialog, QLabel, QPushButton, QVBoxLayout
from utils import CODECS
from variables_ import BIG_FONT_SIZE  # QSS - Estilos do QT for Python
from variables_ import (
    MEDIUM_FONT_SIZE,
    MINIMUM_WIDTH,
    PRIMARY_COLOR,
    QSS,
    SMALL_FONT_SIZE,
    TEXT_MARGIN,
)

if TYPE_CHECKING:
    from main_window import MainWindow


def _setup_theme():
    qdarktheme.setup_theme(
        theme="dark",
        corner_shape="rounded",
        custom_colors={
            "[dark]": {
                "primary": f"{PRIMARY_COLOR}",
            },
            "[light]": {
                "primary": f"{PRIMARY_COLOR}",
            },
        },
        additional_qss=QSS,
    )


class Button(QPushButton):
    def __init__(self, text: str, parent: "MainWindow", *args, **kwargs):
        super().__init__(text, parent, *args, **kwargs)
        self.config_style()

    def config_style(self):
        font = self.font()
        font.setPixelSize(SMALL_FONT_SIZE)
        self.setFont(font)


class ButtonLayout(QVBoxLayout):
    def __init__(self, window: "MainWindow", *args, **kwargs):
        """
        Initializes an instance of the class with a `window` object of type `MainWindow`. 
        `window` is used to set the `window` attribute of the instance. 
        `*args` and `**kwargs` are used to pass any additional arguments to the parent class.
        """
        super().__init__(*args, **kwargs)
        self.window = window
        self.convert = Converter(window)

        self._make_layout()

    def _make_layout(self):
        """
        Creates and initializes the layout of the window.

        Returns:
            None
        """
        # Caixa de seleção
        self.combo = QComboBox(self.window)
        items = [i for i, codec in CODECS]
        self.combo.addItems(items)

        # Botão
        self.button = Button("Selecione seu vídeo", self.window)

        slot = self._make_slot(self._start_convert)

        self._connect_button_clicked(self.button, slot)

        # Label
        self.label = QLabel("Selecione o formato de saída:")
        self.addWidget(self.label)
        self.addWidget(self.combo)
        self.addWidget(self.button)

    def _connect_button_clicked(self, button: Button, slot):
        button.clicked.connect(slot)

    @Slot()
    def _make_slot(self, func, *args, **kwargs):
        @Slot(bool)
        def real_slot(_):
            func(*args, **kwargs)

        return real_slot

    def _start_convert(self):
        self.selected_format = self.combo.currentText()
        self.convert.start_conversion(self.selected_format)


class Converter:
    def __init__(self, window: "MainWindow"):
        self.window = window

    def start_conversion(self, selected_format):
        msg = MsgBox(self.window)
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        input_path, _ = QFileDialog.getOpenFileName(
            self.window,
            "Selecione seu vídeo para conversão",
            filter="Webm Files (*.webm);;MP4 Files (*.mp4);;All Files (*)",
            options=options,
        )
        print(input_path)
        if not input_path:
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self.window,
            "Selecione o local e nome do arquivo de saída",
            filter=f"*.{selected_format.lower()}",
        )
        video_clip = VideoFileClip(input_path)
        if not output_path:
            return
        try:
            codec = self.convert(selected_format)
            video_clip.write_videofile(output_path, codec=codec)
            msg.show_success(f"Conversão concluída.\nSalvo em: {output_path}")
        except Exception as e:
            msg.show_error(f"Ocorreu um erro durante a conversão: {str(e)}")

    def convert(self, selected_format):
        for extension in CODECS:
            if selected_format == extension[0]:
                return extension[1]


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

    def show_success(self, text):
        msg_box = self.make_dialog(text)
        msg_box.setIcon(msg_box.Icon.Information)
        msg_box.exec()
