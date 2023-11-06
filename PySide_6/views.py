# pylint: disable=C0103
# pylint: disable=W0612
# pylint: disable=C0116
# pylint: disable=C0115
from typing import TYPE_CHECKING

import qdarktheme
from conveter import ConverterThread
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
    """
    Sets up the theme for the application.

    This function configures the theme for the application using the qdarktheme library.
    It sets the theme to "dark", with rounded corners, and customizes the primary color based on 
    the `PRIMARY_COLOR` variable. The `additional_qss` parameter is used to apply additional custom
    styles to the application.

    Parameters:
        None

    Returns:
        None
    """
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
        """
        Initializes the object with the given text, parent, and any additional arguments and keyword 
        arguments.

        :param text: A string representing the text to be displayed.
        :type text: str
        :param parent: The parent object of the current object.
        :type parent: MainWindow
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(text, parent, *args, **kwargs)
        self.config_style()

    def config_style(self):
        """
        Configures the style of the object.

        This function sets the font size of the object to a small value.

        Parameters:
            self (object): The object itself.

        Returns:
            None
        """
        font = self.font()
        font.setPixelSize(SMALL_FONT_SIZE)
        self.setFont(font)


class InfoStatusBar:
    def __init__(self, parent: "MainWindow"):
        """
        Initializes the class instance.

        :param parent: The parent MainWindow instance.
        """
        self.window = parent
        self.config_style()

    def config_style(self):
        """
        Sets the font size of the status bar to 10 pixels.

        Parameters:
            self (object): The current instance of the class.

        Returns:
            None
        """
        font = self.window.status_bar.font()
        font.setPixelSize(10)
        self.window.status_bar.setFont(font)


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
        self.status_bar = InfoStatusBar(window)

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
        """
        Connects a button click event to a given slot.

        Args:
            button (Button): The button to connect.
            slot (callable): The slot to connect to.

        Returns:
            None
        """
        button.clicked.connect(slot)

    @Slot()
    def _make_slot(self, func, *args, **kwargs):
        """
        Creates a slot function that wraps the provided function.

        Parameters:
            func (function): The function to be wrapped.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            function: The wrapped function.
        """
        @Slot(bool)
        def real_slot(_):
            func(*args, **kwargs)

        return real_slot

    @Slot()
    def _start_convert(self):
        """
        Starts the conversion process.

        This function is triggered when the user clicks on the start button. It retrieves the input
        path and output path from the respective input fields. If either of the paths is empty, the
        function returns without performing any further actions.

        The function then checks if a conversion thread is already running. If it is, an error
        message is displayed and the function returns. Otherwise, a new conversion thread is 
        created with the selected format, input path, and output path. The finished signal of the
        conversion thread is connected to the handle_conversion_finished slot, and the error signal
        is connected to the handle_conversion_error slot. The conversion thread is then started.

        Finally, a status message is displayed on the status bar indicating that the conversion is
        in progress.

        Parameters:
        - None

        Return:
        - None
        """
        input_path = self.input_file_field.text()
        output_path = self.output_file_field.text()
        if not input_path:
            return
        if not output_path:
            return

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
        """
        Slot function to select an input folder.

        This function opens a file dialog to allow the user to select a video file for conversion.
        The dialog options are set to read-only and the file filters are set to include various video formats.
        The selected folder path is then set as the text of the input file field.

        Parameters:
            None

        Returns:
            None
        """
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
        """
        Slot function that selects an output folder for the user to choose from.
        This function takes no parameters.
        Returns nothing.
        """
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
        """
        Handles the event when a conversion finishes.

        Parameters:
            output_path (str): The path where the conversion output is saved.

        Returns:
            None
        """
        self.window.status_bar.showMessage("Conversão concluída")
        self.msg.show_info(f"Conversão concluída.\nSalvo em: {output_path}")

    def handle_conversion_error(self, error_message):
        """
        Handles a conversion error by displaying an error message in the status bar and showing
        a message box with the error details.

        :param error_message: The error message to display.
        :type error_message: str
        """
        self.window.status_bar.showMessage("Conversão cancelada")
        self.msg.show_error(f"Conversão cancelada: {error_message}")
