from PyQt5.QtWidgets import QDesktopWidget


class Functions:

    @staticmethod
    def center(widget):
        screen = QDesktopWidget().screenGeometry()
        size = widget.geometry()
        widget.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
