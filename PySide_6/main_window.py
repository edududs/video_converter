from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        """
        Initializes the class instance.

        :param parent: The parent widget.
        :type parent: QWidget | None
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        :return: None
        """
        super().__init__(parent, *args, **kwargs)

        # Central Widget
        self.central_widget = QWidget()

        # Layout
        self.v_layout = QVBoxLayout()

        # Setando o Layout dentro do Central Widget
        self.central_widget.setLayout(self.v_layout)

        # Setando o Central Widget
        self.setCentralWidget(self.central_widget)

        # Adicionando título à janela
        self.setWindowTitle("Video Manager")

        # Adicionando status bar
        self.status_bar = self.statusBar()
        current_font = self.statusBar().font()
        new_font = QFont(current_font)
        new_font.setPointSize(10)
        self.status_bar.setFont(new_font)

    def adjust_fixed_size(self) -> None:
        # Tenta ajustar o tamanho da janela ao conteúdo

        self.adjustSize()

        # Tirando o redimensionamento da janela

        # self.setFixedSize(self.size())

    def addwidget_to_vlayout(self, widget: QWidget) -> None:
        """
        Adds a widget to the vertical layout.

        Args:
            widget (QWidget): The widget to be added.

        Returns:
            None
        """
        self.v_layout.addWidget(widget)

    def make_msg_box(self):
        """
        Creates and returns a QMessageBox object.

        :return: A QMessageBox object.
        """
        return QMessageBox(self)

    def make_menu_items(self, menu_item: list | str | tuple):
        menu = self.menuBar()
        if isinstance(menu_item, (list, tuple)):
            for item in menu_item:
                menu.addMenu(item)
            return
        menu.addMenu(menu_item)
