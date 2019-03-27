from queue import Queue

from common.common import Colorable
from common.colors import get_color


class Vertex(Colorable):
    def __init__(self, label, index, coordinates):
        super(Vertex, self).__init__()

        self.label = label or index
        self.index = index
        self.area_color = get_color('white')
        self.color = get_color()
        self.coordinates = coordinates

        self._depth = None
        self._prev = None
        self._height = None
        self._min_width = 0

    def set_border_color(self, color):
        self.color = get_color(color)

    def set_area_color(self, color):
        self.area_color = get_color(color)

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates


class Edge(Colorable):
    def __init__(self, first_vertex, second_vertex, is_directed=False, max_flow=None, weight=None):
        super(Edge, self).__init__()

        self.first_vertex = first_vertex
        self.second_vertex = second_vertex
        self.is_directed = is_directed
        self.current_flow = 0
        self.max_flow = max_flow
        self.weight = weight

    def set_current_flow(self, flow):
        if flow > self.max_flow:
            raise ValueError('Incorrect flow')
        self.current_flow = flow


class Graph():
    def __validate(self, ribs, vertices, flows, coordinates):
        correct_types = (list, tuple)
        assert isinstance(ribs, correct_types)
        n = len(ribs)
        if vertices is not None:
            assert isinstance(vertices, correct_types)
            assert len(vertices) == n
        if flows is not None:
            assert isinstance(flows, correct_types)
            assert len(flows) == n
            for i in flows:
                assert isinstance(i, correct_types)
                assert len(i) == n
        if coordinates is not None:
            assert isinstance(coordinates, correct_types)
            assert len(coordinates) == n
            for i in coordinates:
                assert isinstance(i, correct_types)
                assert len(i) == 2
        for i in ribs:
            assert isinstance(i, correct_types)
            assert len(i) == n

    def __init__(self, ribs=None, weighted=None, vertices=None, directed=False, has_flow=False, flows=None, coordinates=None):
        self.__validate(ribs, vertices, flows, coordinates)
        self.vertices = []
        self.ribs = []
        self.directed = directed
        self.max_index = len(ribs)
        self.flow = has_flow

        for i in range(len(ribs)):
            label = vertices[i] if vertices else i
            current_coordinates = coordinates[i] if coordinates else None
            self.vertices.append(Vertex(label, i, current_coordinates))

        for i in range(len(ribs)):
            for j in range(len(ribs[i])):
                if i != j and ribs[i][j] is not None:
                    if has_flow:
                        max_flow = flows[i][j] if flows else 0
                    else:
                        max_flow = None
                    weight = ribs[i][j] if weighted else None
                    if directed or (not directed and not self.find_rib(i, j)):
                        self.ribs.append(Edge(self.vertices[i], self.vertices[j], directed, max_flow, weight))
        if not coordinates:
            self.fetch_coordinates()

    def get_width(self, default=1200):
        return getattr(self, '_width', default)

    def get_height(self, default=900):
        return getattr(self, '_height', default)

    def find_vertex(self, index):
        for vertex in self.vertices:
            if vertex.index == index:
                return vertex

    def set_vertex_border_color(self, index, color):
        vertex = self.find_vertex(index)
        try:
            vertex.set_border_color(color)
        except Exception:
            pass

    def set_vertex_area_color(self, index, color):
        vertex = self.find_vertex(index)
        try:
            vertex.set_area_color(color)
        except Exception:
            pass

    def find_rib(self, vertex_in_index, vertex_out_index):
        vertex_in = self.find_vertex(vertex_in_index)
        vertex_out = self.find_vertex(vertex_out_index)
        for rib in self.ribs:
            if rib.first_vertex == vertex_in and rib.second_vertex == vertex_out:
                return rib
            elif not self.directed and rib.second_vertex == vertex_in and rib.first_vertex == vertex_out:
                return rib

    def find_ribs(self, vertex):
        return [edge for edge in self.ribs if edge.first_vertex == vertex or edge.second_vertex == vertex]

    def delete_vertex(self, index):
        vertex = self.find_vertex(index)
        ribs = self.find_ribs(vertex)
        for rib in ribs:
            self.ribs.remove(rib)
        self.vertices.remove(vertex)

    def delete_edge(self, vertex_in_index, vertex_out_index):
        edge = self.find_rib(vertex_in_index, vertex_out_index)
        self.ribs.remove(edge)

    def set_flow(self, vertex_in_index, vertex_out_index, flow):
        edge = self.find_rib(vertex_in_index, vertex_out_index)
        edge.set_current_flow(flow)

    def set_flows(self, flows):
        for k, v in flows.items():
            index_in, index_out = k
            edge = self.find_rib(index_in, index_out)
            if edge:
                edge.set_current_flow(v)

    def set_edge_color(self, vertex_in, vertex_out, color):
        edge = self.find_rib(vertex_in, vertex_out)
        edge.set_color(color)

    def set_vertices_color(self, colors):
        for k, v in colors.items():
            vertex = self.find_vertex(k)
            if vertex:
                if v.get('border'):
                    vertex.set_border_color(v.get('border'))
                if v.get('area'):
                    vertex.set_area_color(v.get('area'))

    def set_ribs_color(self, colors):
        for k, v in colors.items():
            index_in, index_out = k
            edge = self.find_rib(index_in, index_out)
            if edge:
                edge.set_color(v)

    def add_edge(self, index_in, index_out, max_flow=None, weight=None):
        vertex_in = self.find_vertex(index_in)
        vertex_out = self.find_vertex(index_out)
        self.ribs.append(Edge(vertex_in, vertex_out, self.directed, max_flow, weight))

    def add_vertex(self, label, coordinates):
        self.vertices.append(Vertex(label, self.max_index, coordinates))
        self.max_index += 1

    def fetch_coordinates(self):
        pass


class Forest(Graph):
    name = 'forest'

    @staticmethod
    def is_forest(ribs):
        visited = [False for _ in range(len(ribs))]

        def dfs(v, prev=-1):
            is_forest = True
            visited[v] = True
            for i in range(len(ribs[v])):
                if i != prev and i != v and visited[i] and (ribs[v][i] is not None or ribs[i][v] is not None):
                    return False
                elif not visited[i] and (ribs[v][i] is not None or ribs[i][v] is not None):
                    is_forest &= dfs(i, v)
            return is_forest
        result = True
        for i in range(len(ribs)):
            if not visited:
                result = result & dfs(i)
        return result

    def _get_second_vertex(self, edge, v):
        if edge.first_vertex.index == v:
            return edge.second_vertex.index
        elif edge.second_vertex.index == v:
            return edge.first_vertex.index
        else:
            return None

    def _find_root(self, component):
        visited = [False for _ in range(len(self.vertices))]

        def dfs(v, depth=0):
            visited[v] = True
            result_depth = depth
            for edge in self.ribs:
                u = self._get_second_vertex(edge, v)
                if u is not None and not visited[u]:
                    result_depth = max(dfs(u, depth + 1), result_depth)
            return result_depth

        depths = []
        for v in component:
            visited = [False for _ in range(len(self.vertices))]
            depths.append(dfs(v))
        return component[depths.index(min(depths))]

    def _find_components(self):
        visited = [False for _ in range(len(self.vertices))]
        components = []
        current_component = []

        def dfs(v):
            visited[v] = True
            current_component.append(v)
            for edge in self.ribs:
                u = self._get_second_vertex(edge, v)
                if u is not None and not visited[u]:
                    dfs(u)

        for i in range(len(self.vertices)):
            if not visited[i]:
                dfs(i)
                components.append(sorted(current_component))
                current_component = []

        return components

    def _find_roots(self):
        components = self._find_components()
        roots = [self._find_root(component) for component in components]
        return roots

    def _fetch_height(self, roots):
        visited = [False for _ in range(len(self.vertices))]

        def dfs(v):
            visited[v] = True
            self.vertices[v]._height = 1
            for edge in self.ribs:
                u = self._get_second_vertex(edge, v)
                if u is not None and not visited[u]:
                    dfs(u)
                    self.vertices[v]._height = max(self.vertices[v]._height, self.vertices[u]._height + 1)

        for root in roots:
            dfs(root)

    def _fetch_depth(self, roots):
        visited = [False for _ in range(len(self.vertices))]

        def dfs(v, depth):
            visited[v] = True
            self.vertices[v]._depth = depth
            for edge in self.ribs:
                u = self._get_second_vertex(edge, v)
                if u is not None and not visited[u]:
                    dfs(u, depth + 1)

        for root in roots:
            dfs(root, 1)

    def _fetch_coordinates(self, roots, width=1200, height=900, indent=45):
        self._width = width + indent
        self._height = height
        visited = [False for _ in range(len(self.vertices))]
        max_depth = max([vertex._depth for vertex in self.vertices])
        delta = (height - 3 * indent) // (max_depth-1)

        def dfs(v, border, depth):
            visited[v] = True
            self.vertices[v].coordinates = [(2 * border + self.vertices[v]._min_width) // 2, indent + depth * delta]
            index = self.vertices[v].index
            for edge in self.ribs:
                u = self._get_second_vertex(edge, index)
                if u is not None and not visited[u]:
                    dfs(u, border, depth + 1)
                    border += self.vertices[u]._min_width

        border = 0
        for i in range(len(roots)):
            dfs(roots[i], border, 0)
            border += self.vertices[roots[i]]._min_width

    def _sort_vertices_by_heights(self, vertices):
        sorted_vertices = sorted(vertices, key=lambda index: -self.vertices[index]._height)
        even_vertices, odd_vertices, result = [], [], []
        for i in range(0, len(vertices), 2):
            even_vertices.append(sorted_vertices[i])
        for i in range(1, len(vertices), 2):
            odd_vertices.append(sorted_vertices[i])
        if odd_vertices:
            even_vertices.extend(reversed(odd_vertices))
        return even_vertices

    def get_min_width(self, roots):
        visited = [False for _ in range(len(self.vertices))]

        def dfs(v, min_width=100):
            visited[v] = True
            self.vertices[v]._min_width = 0
            for edge in self.ribs:
                u = self._get_second_vertex(edge, v)
                if u is not None and not visited[u]:
                    dfs(u)
                    self.vertices[v]._min_width += self.vertices[u]._min_width
            if self.vertices[v]._min_width == 0:
                self.vertices[v]._min_width = min_width

        min_width = 0
        for i in roots:
            dfs(i)
            min_width += self.vertices[i]._min_width
        return min_width

    def fetch_coordinates(self):
        roots = self._find_roots()
        self._fetch_height(roots)
        self._fetch_depth(roots)
        min_width = self.get_min_width(roots)
        self._fetch_coordinates(roots, width=min_width)


class Planar(Graph):
    name = 'planar'

    @staticmethod
    def is_planar(ribs):
        pass

    def fetch_coordinates(self):
        pass


MODELS = [Forest, Planar]


def get_model(**kwargs):
    ribs = kwargs['ribs']
    for model in MODELS:
        if getattr(model, 'is_{}'.format(model.name))(ribs):
            return model(**kwargs)
    return Graph(**kwargs)
