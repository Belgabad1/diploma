from visualizers.graph_visualiser import GraphVisualiser


def init_graph():
    ribs = list(list(None for i in range(7)) for _ in range(7))
    flows = list(list(None for i in range(7)) for _ in range(7))

    def add_ribs(x, y, flow, dist):

        flows[x - 1][y - 1] = flow
        ribs[x - 1][y - 1] = dist

    add_ribs(1, 2, 5, 14)
    add_ribs(1, 3, 9, 5)
    add_ribs(1, 4, 4, 9)
    add_ribs(4, 2, 6, 1)
    add_ribs(3, 4, 9, 8)
    add_ribs(3, 5, 10, 8)
    add_ribs(4, 5, 7, 13)
    add_ribs(3, 6, 8, 7)
    add_ribs(5, 7, 17, 4)
    add_ribs(6, 7, 3, 6)

    visualiser = GraphVisualiser(ribs=ribs, coordinates=[
        [100, 200], [100, 600], [400, 200], [400, 600], [700, 600], [1000, 200], [1000, 600]
    ], has_description=True, directed=True, weighted=True, has_flow=True, flows=flows)
    visualiser.visualize('min_cost_max_flow', 0, 6, 10)


if __name__ == '__main__':
    init_graph()
