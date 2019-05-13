from visualizers.graph_visualiser import GraphVisualiser


def init_graph():
    ribs = list(list(None for i in range(14)) for _ in range(14))
    flows = list(list(None for i in range(14)) for _ in range(14))

    def add_ribs(x, y, flow=1, doubled=False):

        ribs[x - 1][y - 1] = 1
        ribs[y - 1][x - 1] = 1

    add_ribs(1, 3)
    add_ribs(2, 3)
    add_ribs(3, 4)
    add_ribs(3, 5)
    add_ribs(3, 7)
    add_ribs(4, 6)
    add_ribs(5, 8)
    add_ribs(6, 7)
    add_ribs(7, 8)
    add_ribs(7, 9)
    add_ribs(7, 10)
    add_ribs(11, 12)
    add_ribs(11, 13)
    add_ribs(12, 14)
    add_ribs(13, 14)

    visualiser = GraphVisualiser(ribs=ribs)
    visualiser.visualize('components')

if __name__ == '__main__':
    init_graph()
