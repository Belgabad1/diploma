from visualizers.graph_visualiser import GraphVisualiser


def init_graph():
    ribs = list(list(None for i in range(7)) for _ in range(7))
    flows = list(list(None for i in range(7)) for _ in range(7))

    def add_ribs(x, y, dist):

        ribs[x - 1][y - 1] = dist

    add_ribs(1, 2, 5)
    add_ribs(1, 3, 6)
    add_ribs(1, 4, 4)
    add_ribs(4, 2, 6)
    add_ribs(3, 4, 9)
    add_ribs(3, 5, 10)
    add_ribs(5, 4, 1)
    add_ribs(5, 6, 8)
    add_ribs(5, 7, 17)
    add_ribs(6, 7, 3)

    visualiser = GraphVisualiser(ribs=ribs, coordinates=[
        [100, 200], [100, 600], [400, 200], [400, 600], [700, 600], [1000, 200], [1000, 600]
    ], has_description=True, directed=True, weighted=True)
    visualiser.visualize('dijkstra', 0, 6)


if __name__ == '__main__':
    init_graph()
