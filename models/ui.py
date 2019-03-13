import copy

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget, QGridLayout

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

    def add_graph_widget(self, visualiser):
        new_widget = MainWidget(GraphWidget, visualiser, self.size())
        self.widget.addWidget(new_widget)
        self.widget.setCurrentWidget(new_widget)

    def keyPressEvent(self, event):
        current_index = self.widget.currentIndex()
        if event.key() == Qt.Key_Left and current_index > 1:
            current_index -= 1
        elif event.key() == Qt.Key_Right and current_index < self.widget.count() - 1:
            current_index += 1
        self.widget.setCurrentIndex(current_index)


class MainWidget(QWidget):
    def __init__(self, central_widget, visualiser, size):
        super().__init__()
        width, height = size.width(), size.height()
        grid = QGridLayout()
        l = 1
        r = 6
        if visualiser.variables:
            grid.addWidget(VariablesWidget(visualiser.variables, width, height // 6), l, 0)
            l += 1
        if visualiser.description:
            grid.addWidget(DescriptionWidget(visualiser.description, width, height // 6), r, 0)
            r -= 1
        grid.addWidget(central_widget(visualiser, width, height * (r - l + 1) // 6), l, 0, r, 0)
        self.setLayout(grid)
        self.show()


class VariablesWidget(QWidget):
    def __init__(self, variables, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.show()

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QPen(Qt.black, 7))
        painter.drawLine(0, self.height - 5, self.width, self.height - 5)
        painter.end()

    def set_size(self, width, height):
        self.width = width
        self.height = height


class DescriptionWidget(QWidget):
    def __init__(self, description, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.description = copy.deepcopy(description)
        self.show()

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QPen(Qt.black, 7))
        painter.setFont(QFont('Helvetica', 16))
        painter.drawText(
            0, 0, self.width, self.height,
            Qt.AlignCenter, self.description.get_text()
        )
        painter.drawLine(0, 0, self.width, 0)
        painter.end()

    def set_size(self, width, height):
        self.width = width
        self.height = height

class GraphWidget(QWidget):
    radius = 50
    depth = 4
    def __init__(self, visualiser, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.visualiser = copy.deepcopy(visualiser)
        self.visualiser.model._fetch_coordinates(self.width, self.height)
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
