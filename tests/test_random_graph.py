from visualizers.graph_visualiser import GraphVisualiser


def init_graph():
    ribs = list(list(None for i in range(15)) for _ in range(15))
    flows = list(list(None for i in range(15)) for _ in range(15))

    def add_ribs(x, y, flow=1, doubled=False):

        ribs[x - 1][y - 1] = 1
        ribs[y - 1][x - 1] = 1

    add_ribs(1, 2)
    add_ribs(1, 3)
    add_ribs(1, 4)
    add_ribs(2, 4)
    add_ribs(3, 4)
    add_ribs(3, 6)
    add_ribs(4, 5)
    add_ribs(4, 7)
    add_ribs(5, 8)
    add_ribs(5, 9)
    add_ribs(6, 9)
    add_ribs(6, 10)
    add_ribs(6, 11)
    add_ribs(7, 8)
    add_ribs(7, 11)
    add_ribs(8, 15)
    add_ribs(9, 10)
    add_ribs(9, 12)
    add_ribs(10, 11)
    add_ribs(10, 12)
    add_ribs(11, 12)
    add_ribs(11, 13)
    add_ribs(12, 13)
    add_ribs(12, 14)
    add_ribs(13, 14)
    add_ribs(14, 15)

    visualiser = GraphVisualiser(ribs=ribs)
    visualiser.next_step()
    visualiser.show()

if __name__ == '__main__':
    init_graph()
