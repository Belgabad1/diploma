import heapq
import random

from common import colors
from queue import Queue


MAX_DIST = 1 << 100


def dfs(visualizer, start_vertex):
    graph = visualizer.model
    visited = [False for _ in graph.vertices]

    def _dfs(v):
        visualizer.set_vertex_border_color(v, colors.BLUE)
        visualizer.next_step()
        visited[v] = True
        for edge in graph.ribs:
            u = graph.get_second_directed_vertex(edge, v)
            if u is not None:
                visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.RED)
                visualizer.next_step()
                if not visited[u]:
                    visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.GREEN_NEON)
                    visualizer.set_vertex_border_color(v, colors.GREY)
                    _dfs(u)
                    visualizer.set_vertex_border_color(v, colors.BLUE)
                    visualizer.next_step()
                else:
                    visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.GREEN_NEON)
                    visualizer.next_step()
        visualizer.set_vertex_border_color(v, colors.RED)

    _dfs(start_vertex)
    visualizer.next_step()
    visualizer.show()


def bfs(visualizer, start_vertex):
    graph = visualizer.model
    visited = [False for _ in graph.vertices]

    def _bfs(start):
        visited[start] = True
        q = Queue()
        q.put(start)
        while not q.empty():
            v = q.get()
            visualizer.set_vertex_border_color(v, colors.BLUE)
            visualizer.next_step()
            for edge in graph.ribs:
                u = graph.get_second_directed_vertex(edge, v)
                if u is not None:
                    visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.RED)
                    visualizer.next_step()
                    if not visited[u]:
                        visited[u] = True
                        q.put(u)
                        visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.GREEN_NEON)
                        visualizer.set_vertex_border_color(u, colors.GREY)
                        visualizer.next_step()
                    else:
                        visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.GREEN_NEON)
                        visualizer.next_step()
            visualizer.set_vertex_border_color(v, colors.RED)

    _bfs(start_vertex)
    visualizer.next_step()
    visualizer.show()


def components(visualizer):
    graph = visualizer.model
    visited = [False for _ in graph.vertices]

    def _bfs(start, vertex_color, edge_color):
        visited[start] = True
        q = Queue()
        q.put(start)
        while not q.empty():
            v = q.get()
            visualizer.set_vertex_border_color(v, colors.BLUE)
            visualizer.next_step()
            for edge in graph.ribs:
                u = graph.get_second_directed_vertex(edge, v)
                if u is not None:
                    visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.RED)
                    visualizer.next_step()
                    if not visited[u]:
                        visited[u] = True
                        q.put(u)
                        visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, edge_color)
                        visualizer.set_vertex_border_color(u, colors.GREY)
                        visualizer.next_step()
                    else:
                        visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, edge_color)
                        visualizer.next_step()
            visualizer.set_vertex_border_color(v, vertex_color)

    comp = 0
    for i in range(len(visited)):
        if not visited[i]:
            col = random.choices(colors.COLORS_LIST, k=2)
            _bfs(i, col[0], col[1])
            visualizer.next_step()
            comp += 1
    visualizer.show()


def dijkstra(visualizer, start_vertex, finish_vertex=None):
    heap = []
    graph = visualizer.model
    for vertex in graph.vertices:
        if vertex.index != start_vertex:
            vertex.data['dist'] = MAX_DIST
            vertex.set_label('{}\n{}'.format(vertex.index, 'inf'))
        else:
            vertex.data['dist'] = 0
            vertex.data['parent'] = -1
            vertex.set_label('{}\n{}'.format(vertex.index, '0'))
    heapq.heappush(heap, (graph.vertices[start_vertex].data['dist'], start_vertex))
    while heap:
        dist, v = heapq.heappop(heap)
        visualizer.set_vertex_border_color(v, colors.BLUE)
        visualizer.next_step()
        for edge in graph.ribs:
            u = graph.get_second_directed_vertex(edge, v)
            weight = edge.weight or 1
            if u is not None:
                visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.RED)
                visualizer.next_step()
                d = graph.vertices[u].data['dist']
                if dist + weight < d:
                    visualizer.set_vertex_label(u, '{}\n{}'.format(u, dist + weight))
                    graph.vertices[u].data['dist'] = dist + weight
                    graph.vertices[u].data['parent'] = v
                    heapq.heappush(heap, (dist + weight, u))
                visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.DEFAULT)
                visualizer.next_step()
        visualizer.set_vertex_border_color(v, colors.DEFAULT)
    if finish_vertex:
        v = graph.vertices[finish_vertex]
        if not v.data.get('parent'):
            visualizer.set_description(u'Пути из вершины {} в вершину {} не существует'.format(start_vertex, finish_vertex))
        else:
            description = 'Длина кратчайшего маршрута из вершины {} в вершину {} составляет {}.\n'.format(
                start_vertex, finish_vertex, v.data['dist']
            )
            description += 'Путь: '
            ride = [str(v.index)]
            visualizer.set_vertex_border_color(v.index, colors.ORANGE)
            while v.data['parent'] != -1:
                visualizer.set_edge_color(v.data['parent'], v.index, colors.ORANGE)
                v = graph.vertices[v.data['parent']]
                ride.append(str(v.index))
                visualizer.set_vertex_border_color(v.index, colors.ORANGE)
            description += ' -> '.join(reversed(ride))
            visualizer.set_description(description)
    visualizer.next_step()
    visualizer.show()


ALGORITHMS = {
    'dfs': dfs,
    'bfs': bfs,
    'components': components,
    'dijkstra': dijkstra
}
