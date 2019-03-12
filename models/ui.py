import copy

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor
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
        new_widget = GraphWidget(visualiser)
        self.widget.addWidget(new_widget)
        self.widget.setCurrentWidget(new_widget)

    def keyPressEvent(self, event):
        current_index = self.widget.currentIndex()
        if event.key() == Qt.Key_Left and current_index > 1:
            current_index -= 1
        elif event.key() == Qt.Key_Right and current_index < self.widget.count() - 1:
            current_index += 1
        self.widget.setCurrentIndex(current_index)


class GraphWidget(QWidget):
    radius = 50
    depth = 4
    def __init__(self, visualiser):
        super().__init__()
        self.visualiser = copy.deepcopy(visualiser)
        self.show()

    def _draw_vertices(self, painter):
        vertices = self.visualiser.model.vertices
        for vertex in vertices:
            x_center, y_center = vertex.coordinates
            painter.setPen(QPen(QColor(vertex.color), self.depth))
            painter.setBrush(QColor(vertex.area_color))
            painter.drawEllipse(x_center - self.radius // 2, y_center - self.radius // 2, self.radius, self.radius)
            painter.setPen(QPen(Qt.black, self.depth))
            painter.drawText(
                x_center - self.radius // 2, y_center - self.radius // 2, self.radius, self.radius,
                Qt.AlignCenter, str(vertex.label)
            )

    def _draw_edges(self, painter):
        ribs = self.visualiser.model.ribs
        for edge in ribs:
            x1, y1 = edge.first_vertex.coordinates
            x2, y2 = edge.second_vertex.coordinates
            painter.setPen(QPen(QColor(edge.color), self.depth))
            painter.drawLine(x1, y1, x2, y2)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self._draw_edges(painter)
        self._draw_vertices(painter)
        pen = QPen(Qt.black, self.depth, Qt.SolidLine)
        painter.setPen(pen)
        painter.end()
