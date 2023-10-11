import sys
from io import StringIO

from moviepy.editor import VideoFileClip
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class WebMToMP4Converter:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.window.setWindowTitle("WebM to MP4 Converter")
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.label = QLabel("Selecione o arquivo WebM de entrada:")
        self.layout.addWidget(self.label)

        self.select_input_button = QPushButton("Selecionar WebM")
        self.select_input_button.clicked.connect(self.get_input_file)
        self.layout.addWidget(self.select_input_button)

        self.label_output = QLabel("Selecione o local e nome do arquivo MP4 de saída:")
        self.layout.addWidget(self.label_output)

        self.select_output_button = QPushButton("Selecionar MP4 de Saída")
        self.select_output_button.clicked.connect(self.get_output_file)
        self.layout.addWidget(self.select_output_button)

        self.convert_button = QPushButton("Converter para MP4")
        self.convert_button.clicked.connect(self.convert_webm_to_mp4)
        self.layout.addWidget(self.convert_button)

        self.text_output = QPlainTextEdit()
        self.text_output.setReadOnly(True)
        self.layout.addWidget(self.text_output)

        self.central_widget.setLayout(self.layout)
        self.window.setCentralWidget(self.central_widget)

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())

    def get_input_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.input_file, _ = QFileDialog.getOpenFileName(
            self.window,
            "Selecionar arquivo WebM",
            "",
            "WebM Files (*.webm);;All Files (*)",
            options=options,
        )

    def get_output_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.output_file, _ = QFileDialog.getSaveFileName(
            self.window,
            "Selecionar arquivo MP4 de Saída",
            "",
            "MP4 Files (*.mp4);;All Files (*)",
            options=options,
        )

    def convert_webm_to_mp4(self):
        try:
            video_clip = VideoFileClip(self.input_file)
            video_clip.write_videofile(self.output_file, codec="libx264")
            sys.stdout = StringIO()  # Redireciona a saída padrão para um buffer
            self.label_output.setText(f"Conversão concluída: {self.output_file}")
            self.text_output.setPlainText(sys.stdout.getvalue())
            sys.stdout = sys.__stdout__  # Restaura a saída padrão
            self.label_output.setText(f"Conversão concluída: {self.output_file}")
        except Exception as e:
            self.label_output.setText(f"Ocorreu um erro durante a conversão: {str(e)}")


if __name__ == "__main__":
    converter = WebMToMP4Converter()
    converter.run()
