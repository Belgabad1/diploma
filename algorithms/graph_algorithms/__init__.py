import heapq
import random

from common import colors
from queue import Queue

from models.graph_models import Edge

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
        visualizer.set_description('Проверяем вершину {}'.format(i))
        visualizer.set_vertex_area_color(i, colors.GREEN_LIGHT)
        visualizer.next_step()
        if not visited[i]:
            visualizer.set_vertex_area_color(i, colors.WHITE)
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
        else:
            visualizer.set_description('Компонента связности, содержащая вершину {} была найдена ранее'.format(i))
            visualizer.set_vertex_area_color(i, colors.WHITE)
            visualizer.next_step()
    visualizer.set_description('Все компоненты найдены.')
    visualizer.next_step()
    visualizer.show()


def dijkstra(visualizer, start_vertex, finish_vertex=None):
    heap = []
    graph = visualizer.model
    for vertex in graph.vertices:
        if vertex.index != start_vertex:
            vertex.data['dist'] = MAX_DIST
            vertex.set_label('{}\n{}; -1'.format(vertex.index, 'inf'))
        else:
            vertex.data['dist'] = 0
            vertex.data['parent'] = -1
            vertex.set_label('{}\n{}; -1'.format(vertex.index, '0'))
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
                    if finish_vertex:
                        ver = graph.vertices[u]
                        visualizer.set_vertex_label(u, '{}; {}'.format(ver.label, v))
                    graph.vertices[u].data['dist'] = dist + weight
                    graph.vertices[u].data['parent'] = v
                    heapq.heappush(heap, (dist + weight, u))
                else:
                    visualizer.set_description('Ранее был найден более оптимальный путь в вершину {}'.format(u))
                visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.DEFAULT)
                visualizer.next_step()
        visualizer.set_vertex_border_color(v, colors.RED)
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


def prim(visualizer):
    graph = visualizer.model
    n = len(graph.vertices)
    visited = [False for _ in range(n)]
    min_len = [MAX_DIST for _ in range(n)]
    parent = [-1 for _ in range(n)]
    min_len[0] = 0

    answer = 0
    for edge in graph.ribs:
        visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.GREY_LIGHT)
    for vertex in graph.vertices:
        visualizer.set_vertex_border_color(vertex.index, colors.GREY_LIGHT)
        if vertex.index != 0:
            vertex.set_label('{}\n{}; {}'.format(vertex.index, 'inf', -1))
        else:
            vertex.set_label('0\n0; -1')
    visualizer.set_description('Начнем визуализацию алгоритма Прима')
    visualizer.next_step()
    for _ in range(n):
        v = -1
        visualizer.set_description('Найдем непомеченную вершину с определенной минимальной длиной')
        visualizer.next_step()
        for i in range(n):
            visualizer.set_description('Рассмотрим вершину {}'.format(i))
            visualizer.set_vertex_border_color(i, colors.RED)
            visualizer.next_step()
            if not visited[i]:
                if (v == -1 or min_len[i] < min_len[v]):
                    if v == -1:
                        visualizer.set_description('На этой итерации раньше не выбиралась вершина для добавления, '
                                                   'выберем вершину {}'.format(i))
                    else:
                        visualizer.set_description('Вершина {} оптимальнее вершины {}, пометим её'.format(v, i))
                        visualizer.set_vertex_border_color(v, colors.GREY_LIGHT)
                    visualizer.set_vertex_border_color(i, colors.GREEN)
                    v = i
                elif min_len[i] == MAX_DIST:
                    visualizer.set_description('Вершина {} не связана с вершинами, помеченными ранее'.format(i))
                    visualizer.set_vertex_border_color(i, colors.GREY_LIGHT)
                else:
                    visualizer.set_description('Увы, вершина {} не оптимальна на этой итерации'.format(i))
                    visualizer.set_vertex_border_color(i, colors.GREY_LIGHT)
            else:
                visualizer.set_description('Вершина {} уже помечена'.format(i))
                visualizer.set_vertex_border_color(i, colors.DEFAULT)
            visualizer.next_step()
        visited[v] = True
        answer += min_len[v]
        text = 'Добавим вершину {} в итоговое минимальное остовное дерево'.format(v)
        visualizer.set_vertex_border_color(v, colors.DEFAULT)
        if parent[v] != -1:
            text += '\nДобавим ребро ({}, {}) в итоговое минимальное остовное дерево'.format(v, parent[v])
            visualizer.set_edge_color(parent[v], v, colors.DEFAULT)
        visualizer.set_description(text)
        visualizer.next_step()

        visualizer.set_description('Обновим минимальные длины и родителей для непосещенных вершин')
        visualizer.next_step()
        for u in range(n):
            edge = graph.find_rib(v, u)
            if edge:
                visualizer.set_description('Рассмотрим ребро ({}, {})'.format(v, u))
                visualizer.next_step()
                if visited[u]:
                    visualizer.set_description('Вершина {} уже помечена'.format(u))
                    visualizer.next_step()
                elif (edge.weight or 1) < min_len[u]:
                    visualizer.set_description('Оптимизируем минимальное расстояние для вершины {}'.format(u))
                    vertex = graph.vertices[u]
                    min_len[u] = edge.weight or 1
                    parent[u] = v
                    vertex.set_label('{}\n{}; {}'.format(u, min_len[u], parent[u]))
                    visualizer.next_step()
                else:
                    visualizer.set_description('Вершина уже имеет более оптимального предка')
                    visualizer.next_step()
    visualizer.set_description(
        'Алгоритм завершился.'
        'Вес минимального остовного дерева {}.'.format(answer)
    )
    visualizer.next_step()
    visualizer.show()


def dinic(visualizer, s, t):
    graph = visualizer.model
    new_ribs = []

    def add_edge(edge):
        edge.first_vertex.data['ribs'].append(len(new_ribs))
        new_ribs.append(Edge(edge.first_vertex, edge.second_vertex, is_directed=True, max_flow=edge.max_flow))
        edge.second_vertex.data['ribs'].append(len(new_ribs))
        new_ribs.append(Edge(edge.second_vertex, edge.first_vertex, is_directed=True, max_flow=0))

    visualizer.set_description('Начнем алгоритм Диница')
    visualizer.next_step()
    visualizer.set_description('Построим остаточную сеть для графа')
    n = len(graph.ribs)
    for vertex in graph.vertices:
        vertex.data['ribs'] = []
        vertex.data['pointer'] = 0
    for i in range(n):
        add_edge(graph.ribs[i])
    graph.ribs = new_ribs
    visualizer.next_step()

    def _fetch_pointer():
        for vertex in graph.vertices:
            vertex.data['pointer'] = 0

    def _bfs(d):
        q = Queue()
        q.put(s)
        n = len(graph.vertices)
        d[s] = 0
        for vertex in graph.vertices:
            vertex.set_label('{}\n{}'.format(vertex.index, d[vertex.index]))
        visualizer.set_description('Установим расстояние 0 для стока, занесем сток в очередь')
        visualizer.next_step()
        while not q.empty():
            v = q.get()
            visualizer.set_description('Рассмотрим вершину {}'.format(v))
            visualizer.set_vertex_border_color(v, colors.RED)
            visualizer.next_step()
            for u in range(n):
                edge = graph.find_rib(v, u)
                if edge:
                    visualizer.set_description('Рассмотрим ребро ({}, {})'.format(v, u))
                    visualizer.set_edge_color(v, u, colors.RED)
                    visualizer.next_step()
                    if edge.current_flow == edge.max_flow:
                        visualizer.set_description('Поток ребра ({}, {}) уже максимален'.format(v, u))
                        visualizer.next_step()
                    elif d[u] != -1:
                        visualizer.set_description('Для вершины {} уже найдено кратчайшее расстояние'.format(u))
                        visualizer.next_step()
                    else:
                        visualizer.set_description('Устанавливаем расстояние к вершине {}\nДобавляем её в очередь'.format(u))
                        q.put(u)
                        d[u] = d[v] + 1
                        graph.vertices[u].set_label('{}\n{}'.format(u, d[u]))
                        visualizer.set_vertex_border_color(u, colors.GREY)
                        visualizer.next_step()
                    visualizer.set_edge_color(v, u, colors.DEFAULT)
            visualizer.set_description('Обход для вершины {} закончен'.format(v))
            visualizer.set_vertex_border_color(v, colors.DEFAULT)
            visualizer.next_step()
        return d[t] != -1

    def _dfs(v, flow, d):
        visualizer.set_description('Переходим в вершину {}'.format(v))
        visualizer.set_vertex_border_color(v, colors.RED)
        visualizer.next_step()
        if not flow:
            visualizer.set_description('Увеличивающий поток из данной вершины не найден')
            visualizer.set_vertex_border_color(v, colors.DEFAULT)
            visualizer.next_step()
            return 0
        if v == t:
            visualizer.set_description('Найден увеличивающий поток величины {}'.format(flow))
            visualizer.set_vertex_border_color(v, colors.DEFAULT)
            visualizer.next_step()
            return flow
        vertex = graph.vertices[v]
        while vertex.data['pointer'] < len(vertex.data['ribs']):
            id = vertex.data['ribs'][vertex.data['pointer']]
            u = graph.ribs[id].second_vertex.index
            vertex.data['pointer'] += 1
            if d[u] != d[v] + 1:
                continue

            visualizer.set_description('Рассмотрим ребро ({}, {})'.format(v, u))
            visualizer.set_edge_color(v, u, colors.RED)
            visualizer.next_step()
            pushed = _dfs(u, min(flow, graph.ribs[id].max_flow - graph.ribs[id].current_flow), d)
            visualizer.set_edge_color(v, u, colors.DEFAULT)
            visualizer.set_description('Возвращаемся в вершину {}'.format(v))
            visualizer.next_step()
            if pushed:
                visualizer.set_description('Прибавим ребру ({v}, {u}) поток величины {flow}\n'
                                           'Соответственно, отнимем поток этой же величины у ребре ({u}, {v})'.format(v=v, u=u, flow=pushed)
                )
                visualizer.set_vertex_border_color(v, colors.DEFAULT)
                graph.ribs[id].current_flow += pushed
                graph.ribs[id ^ 1].current_flow -= pushed
                visualizer.next_step()
                return pushed
        visualizer.set_vertex_border_color(v, colors.DEFAULT)
        visualizer.set_description('Обход для вершины {} завершен, увеличивающий поток не найден'.format(v))
        visualizer.next_step()

    def _dinic():
        flow = 0
        d = [-1 for _ in range(len(graph.vertices))]
        visualizer.set_description('Построим слоистую сеть для остаточной сети')
        visualizer.next_step()
        while _bfs(d):
            visualizer.set_description('Слоистая сеть найдена, перейдем к поиску блокирующего потока')
            for edge in graph.ribs:
                if d[edge.second_vertex.index] != d[edge.first_vertex.index] + 1:
                    visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.GREY)
            visualizer.next_step()
            _fetch_pointer()
            pushed = 1
            while pushed:
                pushed = _dfs(s, MAX_DIST, d)
                if pushed:
                    flow += pushed
            visualizer.set_description('Итерация завершена, текущий поток {}'.format(flow))
            for edge in graph.ribs:
                visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.DEFAULT)
            visualizer.next_step()
            d = [-1 for _ in range(len(graph.vertices))]
        visualizer.set_description('Для данной сети не существует слоистой сети')
        visualizer.next_step()
        return flow

    flow = _dinic()
    new_ribs = []
    for i in range(0, len(graph.ribs), 2):
        new_ribs.append(graph.ribs[i])
    graph.ribs = new_ribs
    for edge in graph.ribs:
        if edge.current_flow > 0:
            edge.set_color(colors.BLUE)
            edge.first_vertex.set_color(colors.BLUE)
            edge.second_vertex.set_color(colors.BLUE)
        else:
            edge.set_color(colors.DEFAULT)
    visualizer.set_description('Алгоритм завершен. Величина максимального потока - {}'.format(flow))
    visualizer.next_step()
    visualizer.show()


def min_cost_max_flow(visualizer, s, t, k=None):
    graph = visualizer.model
    new_ribs = []

    def add_edge(edge):
        edge.first_vertex.data['ribs'].append(len(new_ribs))
        ind = len(new_ribs)
        new_ribs.append(Edge(
            edge.first_vertex, edge.second_vertex, weight=edge.weight, is_directed=True, max_flow=edge.max_flow
        ))
        new_ribs[-1].data['index'] = ind + 1
        edge.second_vertex.data['ribs'].append(len(new_ribs))
        new_ribs.append(Edge(
            edge.second_vertex, edge.first_vertex, weight=-edge.weight, is_directed=True, max_flow=0
        ))
        new_ribs[-1].data['index'] = ind

    if k:
        text = 'Начнем поиск потока величины {} минимальной стоимости'.format(k)
    else:
        text = 'Начнем поиск максимального потока минимальной стоимости'
    visualizer.set_description(text)
    visualizer.next_step()
    visualizer.set_description('Построим граф с обратными ребрами')
    n = len(graph.ribs)
    for vertex in graph.vertices:
        vertex.data['ribs'] = []
        vertex.data['pointer'] = 0
    for i in range(n):
        add_edge(graph.ribs[i])
    graph.ribs = new_ribs
    visualizer.next_step()

    def _min_cost_max_flow():
        flow = 0
        cost = 0
        while True:
            visualizer.set_description('Построим остаточную сеть')
            for edge in graph.ribs:
                if edge.current_flow == edge.max_flow:
                    visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.GREY)
                else:
                    visualizer.set_edge_color(edge.first_vertex.index, edge.second_vertex.index, colors.DEFAULT)
            visualizer.next_step()
            dist = [MAX_DIST for _ in range(len(graph.vertices))]
            dist[s] = 0
            heap = []
            heapq.heappush(heap, (dist[s], s))
            parent = [-1 for _ in range(len(graph.vertices))]
            visualizer.set_description('Найдем кратчайшее расстояния из стока в исток')
            visualizer.next_step()
            while heap:
                d, v = heapq.heappop(heap)
                if d != dist[v]:
                    continue
                visualizer.set_description('Рассмотрим вершину {}'.format(v))
                visualizer.set_vertex_border_color(v, colors.RED)
                visualizer.next_step()
                for edge in graph.ribs:
                    if edge.first_vertex.index == v:
                        u = edge.second_vertex.index
                        if edge.current_flow < edge.max_flow:
                            visualizer.set_description('Рассмотрим ребро ({}, {})'.format(v, u))
                            visualizer.set_edge_color(v, u, colors.RED)
                            visualizer.next_step()
                            if dist[v] + edge.weight < dist[u]:
                                visualizer.set_description(
                                    'Обновляем кратчайшее расстояние, а так же родителя для вершины {}'.format(u)
                                )
                                visualizer.set_vertex_border_color(u, colors.TURQUOISE)
                                dist[u] = dist[v] + edge.weight
                                parent[u] = v
                                ver = graph.vertices[u]
                                ver.set_label('{}\n{}; {}'.format(ver.index, dist[u], parent[u]))
                                heapq.heappush(heap, (dist[u], u))
                                visualizer.next_step()
                            else:
                                visualizer.set_description('Для вершины {} уже найдено более оптимальное расстояние'.format(u))
                                visualizer.next_step()
                            visualizer.set_edge_color(v, u, colors.DEFAULT)
                visualizer.set_description('Обход из вершины {} завершен'.format(v))
                visualizer.set_vertex_border_color(v, colors.DEFAULT)
                visualizer.next_step()
            if parent[t] == -1:
                visualizer.set_description('Путь из истока в сток не найден')
                visualizer.next_step()
                return flow, cost
            addflow = k - flow if k else MAX_DIST
            cur_v = t
            while cur_v != s:
                visualizer.set_vertex_border_color(cur_v, colors.BLUE)
                visualizer.set_edge_color(parent[cur_v], cur_v, colors.BLUE)
                edge = graph.find_rib(parent[cur_v], cur_v)
                addflow = min(addflow, edge.max_flow - edge.current_flow)
                cur_v = parent[cur_v]
            visualizer.set_vertex_border_color(cur_v, colors.BLUE)
            visualizer.set_description('Найден путь из истока в сток, прибавим поток величины {} для его ребер'.format(addflow))
            visualizer.next_step()
            cur_v = t
            while cur_v != s:
                edge = graph.find_rib(parent[cur_v], cur_v)
                edge.current_flow += addflow
                graph.ribs[edge.data['index']].current_flow -= addflow
                cost += addflow * edge.weight
                cur_v = parent[cur_v]
            flow += addflow
            cur_v = t
            while cur_v != s:
                visualizer.set_vertex_border_color(cur_v, colors.DEFAULT)
                visualizer.set_edge_color(parent[cur_v], cur_v, colors.DEFAULT)
                cur_v = parent[cur_v]
            visualizer.set_vertex_border_color(cur_v, colors.DEFAULT)
            if k and flow == k:
                visualizer.set_description('Поток величины {} найден'.format(k))
                visualizer.next_step()
                return flow, cost
            visualizer.set_description('Итерация завершена, текущий поток - {}, стоимость - {}'.format(flow, cost))
            visualizer.next_step()

    flow, cost = _min_cost_max_flow()
    new_ribs = []
    for i in range(0, len(graph.ribs), 2):
        new_ribs.append(graph.ribs[i])
    graph.ribs = new_ribs
    for edge in graph.ribs:
        if edge.current_flow > 0:
            edge.set_color(colors.BLUE)
            edge.first_vertex.set_color(colors.BLUE)
            edge.second_vertex.set_color(colors.BLUE)
        else:
            edge.set_color(colors.DEFAULT)
    for vertex in graph.vertices:
        vertex.set_label(vertex.index)
    visualizer.set_description('Алгоритм завершен. Найден поток величины {} стоимости {}'.format(flow, cost))
    visualizer.next_step()
    visualizer.show()


ALGORITHMS = {
    'dfs': dfs,
    'bfs': bfs,
    'components': components,
    'dijkstra': dijkstra,
    'kruskal': kruskal,
    'prim': prim,
    'dinic': dinic,
    'min_cost_max_flow': min_cost_max_flow
}
