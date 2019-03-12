from PyQt5.QtWidgets import QApplication

from models.graph_models import get_model as graph_get_model
from models.ui import Widget


class Variables(object):
    TYPES = ['integer', 'float', 'list', 'dict', 'matrix', 'boolean']
    DEFAULT = {
        'integer': 0,
        'float': 0.0,
        'list': [],
        'dict': dict(),
        'matrix': [[]],
        'boolean': False,
    }

    def __init__(self, variables):
        assert isinstance(variables, dict)
        for k, v in variables:
            if v not in self.TYPES:
                raise ValueError('Variables', 'Invalid type: required one of {}, found {}'.format(str(self.TYPES), v))
        self.variables = dict()
        for k, v in variables:
            self.variables[k] = self.DEFAULT[v]

    def set_variable(self, key, value):
        assert key in self.variables
        assert isinstance(self.variables[key], value)
        self.variables[key] = value


class Description(object):
    def __init__(self):
        self.text = ''

    def set_text(self, text):
        if not isinstance(text, str):
            raise ValueError('Text must be string')
        self.text = text


class Visualizer(object):
    def init_ui(self):
        self.app = QApplication([])
        self.user_interface = Widget()

    def __init__(self, has_variables=False, variables=None, has_description=False, **kwargs):
        self.variables = Variables(variables) if has_variables else None
        self.description = Description() if has_description else None
        self.init_ui()

    def set_description(self, text):
        self.description.set_text(text)

    def set_variable(self, key, value):
        self.variables.set_variable(key, value)


class GraphVisualiser(Visualizer):
    def __init__(self, **kwargs):
        super(GraphVisualiser, self).__init__(**kwargs)
        kwargs.pop('has_variables', '')
        kwargs.pop('variables', '')
        kwargs.pop('has_description', '')
        self.model = graph_get_model(**kwargs)

    def next_step(self):
        self.user_interface.add_widget(self)
