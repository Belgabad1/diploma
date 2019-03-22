from PyQt5.QtWidgets import QDesktopWidget


class Functions:

    @staticmethod
    def center(widget):
        screen = QDesktopWidget().screenGeometry()
        size = widget.geometry()
        widget.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    @staticmethod
    def shift(rect, val):
        rect.setLeft(rect.left() + val)
        rect.setRight(rect.right() + val)
        return rect
