import random

import numpy as np

from common.common import Colorable
from common.colors import get_color
from common.util import get_crossing_number, min_length
from math import pi, cos, sin


def _get_coordinates(nnodes, width=1200, height=900, radius=400):
    pos = []
    for angle in np.arange(0.0, 2 * pi, 2 * pi / nnodes):
        pos.append([1 / 2 + radius * cos(angle) / width, 1 / 2 + radius * sin(angle) / height])
    return np.asarray(pos)


def get_result(pos, A):
    minx = 100
    miny = 100
    for ver in pos:
        minx = min(minx, ver[0])
        miny = min(miny, ver[1])
    for ver in pos:
        ver[0] -= minx
        ver[1] -= miny
    maxx = 0
    maxy = 0
    for ver in pos:
        maxx = max(maxx, ver[0])
        maxy = max(maxy, ver[1])
    result = []
    for i in range(pos.shape[0]):
        result.append([pos[i][0] * 1200 / maxx + 50, pos[i][1] * 900 / maxy + 50])
    lines = []
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if A[i][j] == 1.0:
                lines.append([result[i][0], result[i][1], result[j][0], result[j][1]])
    return result, lines


def _get_optimal_coordinates(A):
    nnodes, _ = A.shape
    pos = _fruchterman_reingold(np.asarray(A), _get_coordinates(nnodes))
    result, lines = get_result(pos, A)
    optimal = get_crossing_number(lines)
    min_len = min_length(result)
    answer = result
    for _ in range(100):
        coordinates = [[random.random(), random.random()] for _ in range(nnodes)]
        pos = _fruchterman_reingold(np.asarray(A), np.asarray(coordinates))
        result, lines = get_result(pos, A)
        len = min_length(result)
        if len < 50:
            continue
        crossing_number = get_crossing_number(lines)
        if crossing_number < optimal or (crossing_number == optimal and len > min_len):
            optimal, answer, min_len = crossing_number, result, len
    return np.asarray(answer)


def _fruchterman_reingold(A, pos, iterations=50, threshold=1e-5):
    nnodes, _ = A.shape

    k = np.sqrt(1.0 / nnodes)
    t = max(max(pos.T[0]) - min(pos.T[0]), max(pos.T[1]) - min(pos.T[1])) * 0.1
    dt = t / float(iterations + 1)
    delta = np.zeros((pos.shape[0], pos.shape[0], pos.shape[1]), dtype=A.dtype)
    for iteration in range(iterations):
        delta = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]
        distance = np.linalg.norm(delta, axis=-1)
        np.clip(distance, 0.01, None, out=distance)
        displacement = np.einsum('ijk,ij->ik',
                                 delta,
                                 (k * k / distance ** 2 - A * distance / k))
        length = np.linalg.norm(displacement, axis=-1)
        length = np.where(length < 0.01, 0.1, length)
        delta_pos = np.einsum('ij,i->ij', displacement, t / length)
        pos += delta_pos
        t -= dt
        err = np.linalg.norm(delta_pos) / nnodes
        if err < threshold:
            break
    return pos


class Vertex(Colorable):
    def __init__(self, label, index, coordinates):
        super(Vertex, self).__init__()

        self.label = label or index
        self.index = index
        self.area_color = get_color('white')
        self.color = get_color()
        self.coordinates = coordinates

        self.data = {}

    def set_border_color(self, color):
        self.color = get_color(color)

    def set_area_color(self, color):
        self.area_color = get_color(color)

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def set_label(self, label):
        self.label = label


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

    def __init__(self, ribs=None, weighted=None, labels=None, directed=False, has_flow=False, flows=None, coordinates=None):
        self.__validate(ribs, labels, flows, coordinates)
        self.vertices = []
        self.ribs = []
        self.directed = directed
        self.max_index = len(ribs)
        self.flow = has_flow

        for i in range(len(ribs)):
            label = labels[i] if labels else i
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

    def set_vertex_label(self, index, label):
        vertex = self.find_vertex(index)
        vertex.set_label(label)

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

    def get_second_directed_vertex(self, edge, v):
        if edge.first_vertex.index == v:
            return edge.second_vertex.index
        elif edge.second_vertex.index == v and not self.directed:
            return edge.first_vertex.index
        else:
            return None

    def fetch_coordinates(self):
        self._width = 1350
        self._height = 1050
        A = [[0.0 for _ in range(len(self.vertices))] for _ in range(len(self.vertices))]
        for edge in self.ribs:
            A[edge.first_vertex.index][edge.second_vertex.index] = 1.0
        pos = _get_optimal_coordinates(np.asarray(A))
        for i in range(pos.shape[0]):
            self.vertices[i].coordinates = pos[i]


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
            if not visited[i]:
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
            self.vertices[v].data['height'] = 1
            for edge in self.ribs:
                u = self._get_second_vertex(edge, v)
                if u is not None and not visited[u]:
                    dfs(u)
                    self.vertices[v].data['height'] = max(self.vertices[v].data['height'], self.vertices[u].data['height'] + 1)

        for root in roots:
            dfs(root)

    def _fetch_depth(self, roots):
        visited = [False for _ in range(len(self.vertices))]

        def dfs(v, depth):
            visited[v] = True
            self.vertices[v].data['depth'] = depth
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
        max_depth = max([vertex.data.get('depth') for vertex in self.vertices])
        delta = (height - 3 * indent) // (max(max_depth - 1, 1))

        def dfs(v, border, depth):
            visited[v] = True
            self.vertices[v].coordinates = [(2 * border + self.vertices[v].data.get('min_width', 0)) // 2, indent + depth * delta]
            index = self.vertices[v].index
            for edge in self.ribs:
                u = self._get_second_vertex(edge, index)
                if u is not None and not visited[u]:
                    dfs(u, border, depth + 1)
                    border += self.vertices[u].data.get('min_width', 0)

        border = 0
        for i in range(len(roots)):
            dfs(roots[i], border, 0)
            border += self.vertices[roots[i]].data.get('min_width', 0)

    def _sort_vertices_by_heights(self, vertices):
        sorted_vertices = sorted(vertices, key=lambda index: -self.vertices[index].data['height'])
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
            self.vertices[v].data['min_width'] = 0
            for edge in self.ribs:
                u = self._get_second_vertex(edge, v)
                if u is not None and not visited[u]:
                    dfs(u)
                    self.vertices[v].data['min_width'] += self.vertices[u].data.get('min_width', 0)
            if self.vertices[v].data.get('min_width') == 0:
                self.vertices[v].data['min_width'] = min_width

        min_width = 0
        for i in roots:
            dfs(i)
            min_width += self.vertices[i].data.get('min_width', 0)
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
