from visualizers.models import GraphVisualiser


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

    visualiser = GraphVisualiser(ribs=ribs)
    a = [v.index for v in visualiser.model.vertices]
    assert a == [5, 3, 7, 11, 1, 6, 2, 4, 10, 13, 8, 12, 9, 0]
    for i in range(1, 14):
        assert visualiser.model.vertices[i]._depth >= visualiser.model.vertices[i - 1]._depth
    visualiser.next_step()
    visualiser.app.exec_()

if __name__ == '__main__':
    init_graph()

