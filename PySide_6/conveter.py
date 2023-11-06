# pylint: disable=C0103
# pylint: disable=W0612
# pylint: disable=C0116
# pylint: disable=C0115
import shutil
import tempfile
from typing import TYPE_CHECKING, Optional

from messages import MsgBox
from moviepy.editor import VideoFileClip
from PySide6.QtCore import QObject, QThread, Signal
from utils import CODECS

if TYPE_CHECKING:
    from main_window import MainWindow


class Converter:
    def __init__(self, window: "MainWindow"):
        self.window = window

    def start_conversion(self, selected_format, input_path, output_path):
        msg = MsgBox(self.window)
        print(input_path)
        if not input_path:
            return
        try:
            temp_output = tempfile.NamedTemporaryFile(
                suffix=f".{selected_format.lower()}", delete=False
            )

            codec = self.convert(selected_format)
            video_clip = VideoFileClip(input_path)
            video_clip.write_videofile(temp_output.name, codec=codec)

            if not output_path:
                msg.show_error("Conversão cancelada")
                return
            shutil.copy(temp_output.name, output_path)

            msg.show_info(f"Conversão concluída.\nSalvo em: {output_path}")

        except Exception as e:
            msg.show_error(f"Ocorreu um erro durante a conversão: {str(e)}")

    def convert(self, selected_format):
        """
        Convert the selected format to the corresponding codec.

        Parameters:
            selected_format (str): The format to be converted.

        Returns:
            str: The corresponding codec for the selected format.
        """
        for extension in CODECS:
            if selected_format == extension[0]:
                return extension[1]


class ConverterThread(QThread):
    finished = Signal(str)
    error = Signal(str)

    def __init__(
        self, window: "MainWindow", selected_format, input_path, output_path
    ) -> None:
        """
        Initializes the class instance with the provided parameters.

        Args:
            window (MainWindow): The main window instance.
            selected_format: The selected format.
            input_path: The input path.
            output_path: The output path.

        Returns:
            None
        """
        super().__init__()
        self.window = window
        self.selected_format = selected_format
        self.input_path = input_path
        self.output_path = output_path
        self.msg = MsgBox(self.window)

    def run(self):
        """
        Runs the conversion process.

        This function performs the following steps:
        1. Creates a temporary output file with a suffix based on the selected format.
        2. Retrieves the codec for the selected format.
        3. Loads the video clip from the input path.
        4. Writes the video clip to the temporary output file using the specified codec.
        5. If an output path is not provided, displays an error message and emits a signal indicating the conversion cancellation.
        6. Copies the temporary output file to the specified output path.
        7. Displays a success message indicating the conversion completion and the output path.
        8. Emits a signal indicating the completion of the conversion process.
        9. If an exception occurs during the conversion process, displays an error message with the exception details and emits a signal indicating the error.

        Parameters:
            None

        Returns:
            None
        """
        try:
            temp_output = tempfile.NamedTemporaryFile(
                suffix=f".{self.selected_format.lower()}", delete=False
            )

            codec = self.convert(self.selected_format)
            video_clip = VideoFileClip(self.input_path)
            video_clip.write_videofile(temp_output.name, codec=codec)
            if not self.output_path:
                self.msg.show_error("Conversão cancelada")
                self.error.emit("Conversão cancelada")
                return
            shutil.copy(temp_output.name, self.output_path)
            # self.msg.show_success(f"Conversão concluída.\nSalvo em: {self.output_path}")
            self.finished.emit(self.output_path)
        except Exception as e:
            # self.msg.show_error(f"Ocorreu um erro durante a conversão: {str(e)}")
            self.error.emit(str(e))

    def convert(self, selected_format: str):
        """
        Converts the selected format to its corresponding codec.

        Parameters:
            selected_format (str): The format to be converted.

        Returns:
            str: The corresponding codec for the selected format.
        """
        for extension in CODECS:
            if selected_format == extension[0]:
                return extension[1]
