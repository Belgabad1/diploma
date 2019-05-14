import heapq
import random

from common import colors
from queue import Queue


MAX_DIST = 1 << 100


def dfs(visualizer, start_vertex):
    graph = visualizer.model
    visited = [False for _ in graph.vertices]

    def _dfs(v):
        visualizer.set_description('Переходим в вершину {}'.format(v))
        visualizer.set_vertex_border_color(v, colors.BLUE)
        visualizer.next_step()
        visited[v] = True
        for edge in graph.ribs:
            u = graph.get_second_directed_vertex(edge, v)
            if u is not None:
                visualizer.set_description(
                    'Рассматриваем ребро ({}, {})'.format(v, u)
                )
                visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.RED)
                visualizer.next_step()
                if not visited[u]:
                    visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.GREEN_NEON)
                    visualizer.set_vertex_border_color(v, colors.GREY)
                    _dfs(u)
                    if visualizer.description:
                        text = visualizer.description.get_text()
                    else:
                        text = ''
                    text += '\nВозвращаемся в вершину {}'.format(v)
                    visualizer.set_description(text)
                    visualizer.set_vertex_border_color(v, colors.BLUE)
                    visualizer.next_step()
                else:
                    visualizer.set_description('Вершина {} была помечена ранее'.format(u))
                    visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.GREEN_NEON)
                    visualizer.next_step()
        visualizer.set_description('Обход из вершины {} закончился, помечаем вершину как пройденную.'.format(v))
        visualizer.set_vertex_border_color(v, colors.RED)

    _dfs(start_vertex)
    visualizer.set_description('Обход завершен.')
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
            visualizer.set_description('Переходим в вершину {}'.format(v))
            visualizer.set_vertex_border_color(v, colors.BLUE)
            visualizer.next_step()
            for edge in graph.ribs:
                u = graph.get_second_directed_vertex(edge, v)
                if u is not None:
                    visualizer.set_description(
                        'Рассматриваем ребро ({}, {})'.format(v, u)
                    )
                    visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.RED)
                    visualizer.next_step()
                    if not visited[u]:
                        visualizer.set_description(
                            'Вершина {} не посещалась ранее.\n Добавляем вершину в очередь'.format(u)
                        )
                        visited[u] = True
                        q.put(u)
                        visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.GREEN_NEON)
                        visualizer.set_vertex_border_color(u, colors.GREY)
                        visualizer.next_step()
                    else:
                        visualizer.set_description('Вершина {} была помечена ранее'.format(u))
                        visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.GREEN_NEON)
                        visualizer.next_step()
            visualizer.set_vertex_border_color(v, colors.RED)
            visualizer.set_description('Обход из вершины {} закончился, помечаем вершину как пройденную.'.format(v))
            visualizer.next_step()

    _bfs(start_vertex)
    visualizer.set_description('Обход завершен.')
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
            visualizer.set_description('Переходим в вершину {}.'.format(v))
            visualizer.set_vertex_border_color(v, colors.BLUE)
            visualizer.next_step()
            for edge in graph.ribs:
                u = graph.get_second_directed_vertex(edge, v)
                if u is not None:
                    visualizer.set_description(
                        'Рассматриваем ребро ({}, {}).'.format(v, u)
                    )
                    visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.RED)
                    visualizer.next_step()
                    if not visited[u]:
                        visualizer.set_description(
                            'Вершина {} не посещалась ранее.\n'
                            'Добавляем вершину в очередь'.format(u)
                        )
                        visited[u] = True
                        q.put(u)
                        visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, edge_color)
                        visualizer.set_vertex_border_color(u, colors.GREY)
                        visualizer.next_step()
                    else:
                        visualizer.set_description('Вершина {} была помечена ранее'.format(u))
                        visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, edge_color)
                        visualizer.next_step()
            visualizer.set_vertex_border_color(v, vertex_color)
            visualizer.set_description('Обход из вершины {} закончился, помечаем вершину как пройденную.'.format(v))
            visualizer.next_step()

    comp = 0
    for i in range(len(visited)):
        if not visited[i]:
            visualizer.set_description(
                'Переходим к компоненте, содержащей вершину {}.\n'
                'Для поиска всех вершин компоненты применим bfs.'.format(i)
            )
            visualizer.next_step()
            col = random.choices(colors.COLORS_LIST, k=2)
            _bfs(i, col[0], col[1])
            visualizer.set_description('Компонента, содержащая вершину {} найдена'.format(i))
            visualizer.next_step()
            comp += 1
    visualizer.set_description('Все компоненты найдены.')
    visualizer.next_step()
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
    visualizer.set_description(
        'Инициируем граф.\n'
        'Добавляем всем вершинам кроме стартовой расстояние inf.\n'
        'Добавляем стартовую вершину в кучу.'
    )
    visualizer.next_step()
    while heap:
        dist, v = heapq.heappop(heap)
        if graph.vertices[v].data['dist'] != dist:
            continue
        visualizer.set_description('Переходим в вершину {}.'.format(v))
        visualizer.set_vertex_border_color(v, colors.BLUE)
        visualizer.next_step()
        for edge in graph.ribs:
            u = graph.get_second_directed_vertex(edge, v)
            weight = edge.weight or 1
            if u is not None:
                visualizer.set_description(
                    'Рассматриваем ребро ({}, {})'.format(v, u)
                )
                visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.RED)
                visualizer.next_step()
                d = graph.vertices[u].data['dist']
                if dist + weight < d:
                    visualizer.set_description(
                        'Найден более оптимальный путь в вершину {}.\n'
                        'Устанавливаем расстояние до вершины {}'.format(u, dist + weight)
                    )
                    visualizer.set_vertex_label(u, '{}\n{}'.format(u, dist + weight))
                    graph.vertices[u].data['dist'] = dist + weight
                    graph.vertices[u].data['parent'] = v
                    heapq.heappush(heap, (dist + weight, u))
                else:
                    visualizer.set_description('Ранее был найден более оптимальный путь в вершину {}'.format(u))
                visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.DEFAULT)
                visualizer.next_step()
        visualizer.set_vertex_border_color(v, colors.DEFAULT)
        visualizer.set_description('Обход из вершины {} окончен.'.format(v))
    visualizer.set_description('Все кратчайшие расстояния найдены')
    visualizer.next_step()
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
            description += '.'
            visualizer.set_description(description)
        visualizer.next_step()
    visualizer.show()


def kruskal(visualizer):
    graph = visualizer.model
    p = [i for i in range(len(graph.vertices))]

    def find_parent(v):
        if p[v] != v:
            p[v] = find_parent(p[v])
        return p[v]

    def unite(v, u):
        v = find_parent(v)
        u = find_parent(u)
        if random.randint(0, 1):
            v, u = u, v
        p[u] = v

    sorted_ribs = sorted([[edge.weight or 1, edge.first_vertex.index, edge.second_vertex.index] for edge in graph.ribs])
    for edge in graph.ribs:
        visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.GREY_LIGHT)
    visualizer.set_description(
        'Инициируем граф.\n'
        'Добавим каждую вершину в свое множество.'
    )
    visualizer.next_step()
    weight = 0
    for edge in sorted_ribs:
        e = graph.find_rib(edge[1], edge[2])
        v, u = edge[1], edge[2]
        visualizer.set_description('Рассмотрим ребро ({}, {})'.format(edge[1], edge[2]))
        visualizer.set_edge_color(edge[1], edge[2], colors.RED)
        visualizer.next_step()
        if find_parent(v) != find_parent(u):
            visualizer.set_description(
                'Вершины {} и {} находятся в разных множествах.\n'
                'Добавим ребро ({}, {}) в итоговый остов.'.format(edge[1], edge[2], edge[1], edge[2])
            )
            visualizer.set_edge_color(v, u, colors.DEFAULT)
            unite(v, u)
            weight += edge[0]
        else:
            visualizer.set_description(
                'Вершины {} и {} уже находятся в одном множестве.'.format(edge[1], edge[2])
            )
            visualizer.set_edge_color(v, u, colors.GREY_LIGHT)
        visualizer.next_step()
    visualizer.set_description(
        'Алгоритм завершился.'
        'Вес минимального остовного дерева {}.'.format(weight)
    )
    visualizer.next_step()
    visualizer.show()


ALGORITHMS = {
    'dfs': dfs,
    'bfs': bfs,
    'components': components,
    'dijkstra': dijkstra,
    'kruskal': kruskal,
}
