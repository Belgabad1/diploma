from queue import Queue

from models.common import Colorable
from models.colors import get_color


class Vertex(Colorable):
    INDENT = 50
    DELTA = 100

    def __init__(self, label, index, coordinates):
        super(Vertex, self).__init__()

        self.label = label
        self.index = index
        self.area_color = get_color('white')
        self.color = get_color()
        self.coordinates = coordinates

        self._depth = None
        self._prev = None

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

    def __init__(self, ribs=None, vertices=None, directed=False, has_flow=False, flows=None, coordinates=None):
        self.__validate(ribs, vertices, flows, coordinates)
        self.vertices = []
        self.ribs = []
        self.directed = directed

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
                    weight = ribs[i][j] if directed else None
                    if directed or (not directed and not self.find_rib(i, j)):
                        self.ribs.append(Edge(self.vertices[i], self.vertices[j], directed, max_flow, weight))
        if not coordinates:
            self.fetch_coordinates()

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

    def fetch_coordinates(self):
        pass

    def draw(self, widget):
        for rib in self.ribs:
            rib.draw(widget)
        for vertex in self.vertices:
            vertex.draw(widget)


class Tree(Graph):
    @staticmethod
    def is_tree(ribs):
        visited = [False for _ in range(len(ribs))]

        def dfs(v, prev=-1):
            is_tree = True
            visited[v] = True
            for i in range(len(ribs[v])):
                if i != prev and i != v and visited[i] and ribs[v][i] is not None:
                    return False
                elif not visited[i] and ribs[v][i] is not None:
                    is_tree &= dfs(i, v)
            return is_tree
        result = dfs(0)
        for i in visited:
            result = result & i
        return result

    def _get_second_vertex(self, edge, v):
        if edge.first_vertex.index == v:
            return edge.second_vertex.index
        elif not edge.is_directed and edge.second_vertex.index == v:
            return edge.first_vertex.index
        else:
            return None

    def _find_root(self):
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
        for v in range(len(self.vertices)):
            visited = [False for _ in range(len(self.vertices))]
            depths.append(dfs(v))
        return depths.index(min(depths))

    def _fetch_depth(self, root):
        visited = [False for _ in range(len(self.vertices))]

        def dfs(v, depth=0, prev=0):
            visited[v] = True
            self.vertices[v]._depth = depth
            self.vertices[v]._prev = self.vertices[prev]
            for edge in self.ribs:
                u = self._get_second_vertex(edge, v)
                if u is not None and not visited[u]:
                    dfs(u, depth + 1, v)
        dfs(root, 0, root)

    def _fetch_coordinates(self, width=800, height=600):
        l, r = 0, 0
        depth = 0
        n = len(self.vertices)
        max_depth = self.vertices[-1]._depth
        delta = (height - 3 * Vertex.INDENT) // max_depth
        while l < n and r < n:
            while r < n and self.vertices[r]._depth == depth:
                r += 1
            count = r - l
            num = 1
            while l < r:
                self.vertices[l].coordinates = [width * num / (count + 1), Vertex.INDENT + depth * delta]
                l += 1
                num += 1
            depth += 1

    def fetch_coordinates(self):
        root = self._find_root()
        self._fetch_depth(root)

        queue = Queue()
        queue.put(root)
        vertices = [self.vertices[root]]
        visited = [False for _ in range(len(self.vertices))]
        visited[root] = True
        while not queue.empty():
            v = queue.get()
            for edge in self.ribs:
                u = self._get_second_vertex(edge, v)
                if u is not None and not visited[u]:
                    visited[u] = True
                    queue.put(u)
                    vertices.append(self.vertices[u])

        self.vertices = vertices
        self._fetch_coordinates()


class Planar(Graph):
    @staticmethod
    def is_planar(ribs):
        pass

    def fetch_coordinates(self):
        pass


def get_model(**kwargs):
    ribs = kwargs['ribs']
    if Tree.is_tree(ribs):
        return Tree(**kwargs)
    if Planar.is_planar(ribs):
        return Planar(**kwargs)
    return Graph(**kwargs)
