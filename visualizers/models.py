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
        for k, v in variables.items():
            if v not in self.TYPES:
                raise ValueError('Variables', 'Invalid type: required one of {}, found {}'.format(str(self.TYPES), v))
        self.variables = dict()
        for k, v in variables.items():
            self.variables[k] = self.DEFAULT[v]

    def set_variable(self, key, value):
        assert key in self.variables
        assert isinstance(self.variables[key], value)
        self.variables[key] = value


class Description(object):
    def __init__(self):
        self._text = ''

    def set_text(self, text):
        if not isinstance(text, str):
            raise ValueError('Text must be string')
        self._text = text

    def get_text(self):
        return self._text


class Visualizer(object):
    def __init__(self, has_variables=False, variables=None, has_description=False, **kwargs):
        self.variables = Variables(variables) if has_variables else None
        self.description = Description() if has_description else None

    def set_description(self, text):
        if self.description:
            self.description.set_text(text)

    def set_variable(self, key, value):
        if self.variables:
            self.variables.set_variable(key, value)
