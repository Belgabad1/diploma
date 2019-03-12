from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget

from models.util import Functions


class Widget(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.widget = QStackedWidget(self)
        self.begin = QWidget()
        self.widget.addWidget(self.begin)
        self.widget.setCurrentWidget(self.begin)
        self.setCentralWidget(self.widget)
        self.resize(800, 600)
        Functions.center(self)
        self.show()

    def add_widget(self, visualiser):
        new_widget = CentralWidget(visualiser)
        self.widget.addWidget(new_widget)
        self.widget.setCurrentWidget(new_widget)


class CentralWidget(QWidget):
    radius = 50
    depth = 7
    def __init__(self, visualiser):
        super().__init__()
        self.visualiser = visualiser
        self.show()

    def _draw_vertices(self, painter):
        vertices = self.visualiser.model.vertices
        i = 0
        for vertex in vertices:
            x_center, y_center = vertex.coordinates
            painter.drawEllipse(x_center - self.radius // 2, y_center - self.radius // 2, self.radius, self.radius)

    def _draw_edges(self, painter):
        ribs = self.visualiser.model.ribs
        for edge in ribs:
            x1, y1 = edge.first_vertex.coordinates
            x2, y2 = edge.second_vertex.coordinates
            painter.drawLine(x1, y1, x2, y2)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self._draw_edges(painter)
        self._draw_vertices(painter)
        pen = QPen(Qt.black, self.depth, Qt.SolidLine)
        painter.setPen(pen)
        painter.end()
