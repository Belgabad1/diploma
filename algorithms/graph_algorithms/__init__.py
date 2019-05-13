from common import colors
from queue import Queue


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

    comp_colors = [['red', 'green'], ['turquoise', 'orange']]
    comp = 0
    for i in range(len(visited)):
        if not visited[i]:
            index = comp % len(comp_colors)
            _bfs(i, comp_colors[index][0], comp_colors[index][1])
            visualizer.next_step()
            comp += 1
    visualizer.show()


ALGORITHMS = {
    'dfs': dfs,
    'bfs': bfs,
    'components': components,
}
