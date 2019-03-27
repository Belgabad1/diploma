from visualizers.graph_visualiser import GraphVisualiser


def init_graph():
    ribs = list(list(None for i in range(31)) for _ in range(31))

    def add_ribs(x, y):

        ribs[x - 1][y - 1] = 1
        ribs[y - 1][x - 1] = 1


    for i in range(1, 16):
        add_ribs(i, i * 2)
        add_ribs(i, i * 2 + 1)

    visualiser = GraphVisualiser(ribs=ribs)
    visualiser.next_step()
    visualiser.show()

if __name__ == '__main__':
    init_graph()

