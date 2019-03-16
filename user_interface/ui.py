import copy
from math import cos, pi, sin, tan, atan, sqrt

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget, QGridLayout

from common.util import get_circle_point, get_angle, get_distance
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

    def widgets(self):
        return [self.widget.widget(i) for i in range(self.widget.count())]

    def resizeEvent(self, QResizeEvent):
        for widget in self.widgets():
            if getattr(widget, 'set_size', None):
                widget.set_size(self.size())


class MainWidget(QWidget):
    def __init__(self, central_widget, visualiser, size):
        super().__init__()
        self.visualiser = visualiser
        self.central_widget = central_widget
        width, height = size.width(), size.height()
        grid = QGridLayout()
        l, r = 1, 6
        if self.visualiser.variables:
            self.variables = VariablesWidget(visualiser.variables, width, height // 6)
            grid.addWidget(self.variables, l, 0)
            l += 1
        if self.visualiser.description:
            self.description = DescriptionWidget(visualiser.description, width, height // 6)
            grid.addWidget(self.description, r, 0)
            r -= 1
        self.central = central_widget(visualiser, width, height * (r - l + 1) // 6)
        grid.addWidget(self.central, l, 0, r, 0)
        self.setLayout(grid)
        self.show()

    def set_size(self, size):
        width, height = size.width(), size.height()
        r = 6
        if getattr(self, 'variables', None):
            self.variables.set_size(width, height // 6)
            r -= 1
        if getattr(self, 'description', None):
            self.description.set_size(width, height // 6)
            r -= 1
        self.central.set_size(width, height * r // 6)


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
        self.repaint()


class DescriptionWidget(QWidget):
    MIN_FONT_SIZE = 12
    MAX_FONT_SIZE = 18

    def __init__(self, description, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.description = copy.deepcopy(description)
        self.show()

    @property
    def FONT_SIZE(self):
        size = min(self.width, self.height) // 7
        return max(min(self.MAX_FONT_SIZE, size), self.MIN_FONT_SIZE)

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QPen(Qt.black, 7))
        painter.setFont(QFont('Helvetica', self.FONT_SIZE))
        painter.drawText(
            0, 0, self.width, self.height,
            Qt.AlignCenter, self.description.get_text()
        )
        painter.drawLine(0, 0, self.width, 0)
        painter.end()

    def set_size(self, width, height):
        self.width = width
        self.height = height
        self.repaint()


class GraphWidget(QWidget):
    MIN_RADIUS = 10
    MAX_RADIUS = 30
    DEPTH = 3
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 600

    def __init__(self, visualiser, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.visualiser = copy.deepcopy(visualiser)
        self.show()

    @property
    def RADIUS(self):
        radius = min(self.width, self.height) // 30
        return max(min(self.MAX_RADIUS, radius), self.MIN_RADIUS)

    def _draw_vertices(self, painter):
        vertices = self.visualiser.model.vertices
        for vertex in vertices:
            x_center, y_center = vertex.coordinates
            x_center, y_center = self.resize(x_center, y_center)
            painter.setPen(QPen(QColor(vertex.color), self.DEPTH))
            painter.setBrush(QColor(vertex.area_color))
            painter.drawEllipse(x_center - self.RADIUS, y_center - self.RADIUS, 2 * self.RADIUS, 2 * self.RADIUS)
            painter.setPen(QPen(Qt.black, self.DEPTH))
            painter.drawText(
                x_center - self.RADIUS, y_center - self.RADIUS, 2 * self.RADIUS, 2 * self.RADIUS,
                Qt.AlignCenter, str(vertex.label)
            )

    def resize(self, x, y):
        return x * self.width / self.DEFAULT_WIDTH, y * self.height / self.DEFAULT_HEIGHT

    def _draw_direct(self, painter, x1, y1, x2, y2, line_length=12, offset=15, angle=pi/6):
        x_beg, y_beg = get_circle_point(x1, y1, x2, y2, self.RADIUS)
        x_fin, y_fin = get_circle_point(x1, y1, x2, y2, self.RADIUS + line_length)
        l = offset * tan(angle)
        ang = get_angle(x1, y1, x2, y2)
        new_x = x_fin + l * sin(pi - ang)
        new_y = y_fin + l * cos(pi - ang)
        painter.drawLine(x_beg, y_beg, new_x, new_y)
        new_x = x_fin - l * sin(pi - ang)
        new_y = y_fin - l * cos(pi - ang)
        painter.drawLine(x_beg, y_beg, new_x, new_y)

    def _draw_weight(self, painter, x1, y1, x2, y2, text):
        x_fin, y_fin = (x1 + x2) / 2, (y1 + y2) / 2
        l = 15
        ang = get_angle(x1, y1, x2, y2)
        new_x = x_fin - l * sin(pi - ang)
        new_y = y_fin - l * cos(pi - ang)
        painter.setPen(QPen(Qt.black, self.DEPTH))
        painter.drawText(new_x - 15, new_y - 15, 30, 30, Qt.AlignCenter, text)

    def _get_flow_text(self, edge):
        return '{}/{}'.format(edge.current_flow, edge.max_flow)

    def _draw_flow(self, painter, x1, y1, x2, y2, text):
        x_fin, y_fin = (x1 + x2) / 2, (y1 + y2) / 2
        l = 16
        ang = get_angle(x1, y1, x2, y2)
        new_x = x_fin + l * sin(pi - ang)
        new_y = y_fin + l * cos(pi - ang)
        painter.setPen(QPen(Qt.black, self.DEPTH))
        painter.drawText(new_x - 20, new_y - 20, 40, 40, Qt.AlignCenter, text)

    def _draw_edges(self, painter):
        ribs = self.visualiser.model.ribs
        for edge in ribs:
            x1, y1 = edge.first_vertex.coordinates
            x1, y1 = self.resize(x1, y1)
            x2, y2 = edge.second_vertex.coordinates
            x2, y2 = self.resize(x2, y2)
            painter.setPen(QPen(QColor(edge.color), self.DEPTH))
            painter.drawLine(x1, y1, x2, y2)
            if edge.is_directed:
                self._draw_direct(painter, x1, y1, x2, y2)
            if edge.weight:
                self._draw_weight(painter, x1, y1, x2, y2, str(edge.weight))
            if edge.max_flow:
                self._draw_flow(painter, x1, y1, x2, y2, self._get_flow_text(edge))

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self._draw_edges(painter)
        self._draw_vertices(painter)
        pen = QPen(Qt.black, self.DEPTH, Qt.SolidLine)
        painter.setPen(pen)
        painter.end()

    def set_size(self, width, height):
        self.width = width
        self.height = height
        self.repaint()
