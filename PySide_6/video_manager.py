# pylint: disable=C0103
# pylint: disable=W0612
import sys

from main_window import MainWindow
from PySide6.QtWidgets import QApplication
from views import ButtonLayout, _setup_theme

if __name__ == "__main__":
    # Iniciando aplicação
    app = QApplication(sys.argv)
    _setup_theme()
    window = MainWindow()

    # Adicionando labels
    convert_button = ButtonLayout(window)
    window.v_layout.addLayout(convert_button)

    # Ajustando o tamanho da janela
    window.adjust_fixed_size()

    window.show()
    app.exec()
