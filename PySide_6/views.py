# pylint: disable=C0103
# pylint: disable=W0612
# pylint: disable=C0116
# pylint: disable=C0115
from typing import TYPE_CHECKING

import qdarktheme
from conveter import Converter, ConverterThread
from messages import MsgBox
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)
from utils import CODECS  # QSS - Estilos do QT for Python
from variables_ import *

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
        # self.convert = Converter(window)
        self.msg = MsgBox(window)
        self.convert_thread: ConverterThread | None = None

        self._make_layout()
        self.selected_format = self.combo.currentText()

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

        # Campo de entrada de texto
        self.input_file_field = QLineEdit(self.window)
        self.output_file_field = QLineEdit(self.window)

        # Botão
        self.button = Button("Converter", self.window)
        self.select_input_folder_button = Button("Selecione seu vídeo", self.window)
        self.select_output_folder_button = Button(
            "Selecione onde quer salvar seu vídeo", self.window
        )

        # Criando Slots
        slot_convert = self._make_slot(self._start_convert)
        slot_select_input_folder = self._make_slot(self._select_input_folder)
        slot_select_output_folder = self._make_slot(self._select_output_folder)

        # Conectando os eventos
        self._connect_button_clicked(self.button, slot_convert)
        self._connect_button_clicked(
            self.select_input_folder_button, slot_select_input_folder
        )
        self._connect_button_clicked(
            self.select_output_folder_button, slot_select_output_folder
        )

        # Label
        self.label_format = QLabel("Selecione o formato de saída:")
        self.label_video_dir = QLabel("Selecione o diretório:")
        self.label_output_file = QLabel("Selecione o diretório:")

        # Adicionando Widgets
        self.addWidget(self.label_video_dir)
        self.addWidget(self.select_input_folder_button)
        self.addWidget(self.input_file_field)
        self.addWidget(self.label_format)
        self.addWidget(self.combo)
        self.addWidget(self.label_output_file)
        self.addWidget(self.select_output_folder_button)
        self.addWidget(self.output_file_field)
        self.addWidget(self.button)

    def _connect_button_clicked(self, button: Button, slot):
        button.clicked.connect(slot)

    @Slot()
    def _make_slot(self, func, *args, **kwargs):
        @Slot(bool)
        def real_slot(_):
            func(*args, **kwargs)

        return real_slot

    @Slot()
    def _start_convert(self):
        input_path = self.input_file_field.text()
        output_path = self.output_file_field.text()
        if not input_path:
            return
        if not output_path:
            return

        # self.convert.start_conversion(self.selected_format, input_path, output_path)
        if self.convert_thread is not None and self.convert_thread.isRunning():
            self.msg.show_error("Conversão em andamento")
            return
        self.convert_thread = ConverterThread(
            self.window, self.selected_format, input_path, output_path
        )
        self.convert_thread.finished.connect(self.handle_conversion_finished)
        self.convert_thread.error.connect(self.handle_conversion_error)
        self.convert_thread.start()
        self.window.status_bar.showMessage("Conversão em andamento...")

    @Slot()
    def _select_input_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filters = "Vídeos (*.webm *.mp4 *.avi *.mkv *.mov *.mpeg1 *.mpeg2 *.mpeg4\
            *.mpg *.wmv *.mpegps *.flv *.3gpp);;Webm Files (*.webm);;MP4 Files (*.mp4);\
            ;AVI Files (*.avi);;MKV Files (*.mkv);;MOV Files (*.mov);;MPEG-1 Files (*.mpeg1);\
            ;MPEG-2 Files (*.mpeg2);;MPEG-4 Files (*.mpeg4);;MPG Files (*.mpg);;WMV Files (*.wmv);\
            ;MPEGPS Files (*.mpegps);;FLV Files (*.flv);;3GPP Files (*.3gpp);;All Files (*);;"
        selected_folder, _ = QFileDialog.getOpenFileName(
            self.window,
            "Selecione seu vídeo para conversão",
            filter=filters,
            options=options,
        )
        if not selected_folder:
            return
        self.input_file_field.setText(selected_folder)

    @Slot()
    def _select_output_folder(self):
        output_extension = self.combo.currentText()
        filters = f"*.{output_extension.lower()}"
        selected_folder, _ = QFileDialog.getSaveFileName(
            self.window,
            "Selecione o local e nome do arquivo de saída",
            filter=filters,
        )
        if not selected_folder:
            return
        self.output_file_field.setText(selected_folder)

    def handle_conversion_finished(self, output_path):
        self.window.status_bar.showMessage("Conversão concluída")
        self.msg.show_info(f"Conversão concluída.\nSalvo em: {output_path}")

    def handle_conversion_error(self, error_message):
        self.window.status_bar.showMessage("Conversão cancelada")
        self.msg.show_error(f"Conversão cancelada: {error_message}")


# class Converter:
#     def __init__(self, window: "MainWindow"):
#         self.window = window

#     def start_conversion(self, selected_format, input_path, output_path):
#         msg = MsgBox(self.window)
#         print(input_path)
#         if not input_path:
#             return
#         try:
#             temp_output = tempfile.NamedTemporaryFile(
#                 suffix=f".{selected_format.lower()}", delete=False
#             )

#             codec = self.convert(selected_format)
#             video_clip = VideoFileClip(input_path)
#             video_clip.write_videofile(temp_output.name, codec=codec)

#             if not output_path:
#                 msg.show_error("Conversão cancelada")
#                 return
#             shutil.copy(temp_output.name, output_path)

#             msg.show_success(f"Conversão concluída.\nSalvo em: {output_path}")

#         except Exception as e:
#             msg.show_error(f"Ocorreu um erro durante a conversão: {str(e)}")

#     def convert(self, selected_format):
#         for extension in CODECS:
#             if selected_format == extension[0]:
#                 return extension[1]


# class MsgBox:
#     def __init__(self, window: "MainWindow") -> None:
#         self.window = window

#     def make_dialog(self, text):
#         msg_box = self.window.make_msg_box()
#         msg_box.setText(text)
#         return msg_box

# def show_error(self, text):
#     msg_box = self.make_dialog(text)
#     msg_box.setIcon(msg_box.Icon.Critical)
#     msg_box.exec()

# def show_success(self, text):
#     msg_box = self.make_dialog(text)
#     msg_box.setIcon(msg_box.Icon.Information)
#     msg_box.exec()
