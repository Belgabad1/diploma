from visualizers.graph_visualiser import GraphVisualiser


def init_graph():
    ribs = list(list(None for i in range(14)) for _ in range(14))

    def add_ribs(x, y):

        ribs[x - 1][y - 1] = 1
        ribs[y - 1][x - 1] = 1


    add_ribs(1, 10)
    add_ribs(2, 4)
    add_ribs(2, 14)
    add_ribs(3, 9)
    add_ribs(3, 13)
    add_ribs(3, 12)
    add_ribs(4, 6)
    add_ribs(5, 12)
    add_ribs(6, 8)
    add_ribs(6, 12)
    add_ribs(7, 8)
    add_ribs(10, 11)
    add_ribs(11, 12)

    visualiser = GraphVisualiser(ribs=ribs, has_description=True)
    visualiser.visualize('dfs', 5)


if __name__ == '__main__':
    init_graph()
