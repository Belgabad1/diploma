from visualizers.graph_visualiser import GraphVisualiser


def init_graph():
    ribs = list(list(None for i in range(26)) for _ in range(26))

    def add_ribs(x, y):

        ribs[x - 1][y - 1] = 1


    add_ribs(1, 2)
    add_ribs(1, 3)
    add_ribs(4, 5)
    add_ribs(4, 6)
    add_ribs(5, 7)
    add_ribs(5, 8)
    add_ribs(6, 9)
    add_ribs(6, 10)
    add_ribs(11, 12)
    add_ribs(11, 13)
    add_ribs(11, 14)
    add_ribs(12, 15)
    add_ribs(12, 16)
    add_ribs(14, 17)
    add_ribs(14, 18)
    add_ribs(15, 19)
    add_ribs(18, 22)
    add_ribs(19, 20)
    add_ribs(19, 21)
    add_ribs(22, 23)
    add_ribs(22, 24)
    add_ribs(23, 25)
    add_ribs(25, 26)

    visualiser = GraphVisualiser(ribs=ribs, has_description=True)
    visualiser.visualize('components')


if __name__ == '__main__':
    init_graph()

