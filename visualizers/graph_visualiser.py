from PyQt5.QtWidgets import QApplication

from models.graph_models import get_model as graph_get_model
from models.ui import Widget
from visualizers.models import Visualizer

app = QApplication([])
user_interface = Widget()


class GraphVisualiser(Visualizer):
    def __init__(self, **kwargs):
        super(GraphVisualiser, self).__init__(**kwargs)
        kwargs.pop('has_variables', '')
        kwargs.pop('variables', '')
        kwargs.pop('has_description', '')
        self.model = graph_get_model(**kwargs)

    def next_step(self):
        user_interface.add_graph_widget(self)

    def set_vertex_border_color(self, index, color):
        self.model.set_vertex_border_color(index, color)

    def set_vertex_area_color(self, index, color):
        self.model.set_vertex_area_color(index, color)

    def set_edge_color(self, vertex_in, vertex_out, color):
        self.model.set_edge_color(vertex_in, vertex_out, color)

    def set_vertices_color(self, colors):
        self.model.set_vertices_color(colors)

    def set_ribs_color(self, colors):
        self.model.set_ribs_color(colors)

    def delete_vertex(self, index):
        self.model.delete_vertex(index)

    def delete_edge(self, index_in, index_out):
        self.model.delete_edge(index_in, index_out)

    def add_edge(self, index_in, index_out):
        self.model.add_edge(index_in, index_out)

    def show(self):
        app.exec_()