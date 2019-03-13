from visualizers.graph_visualiser import GraphVisualiser


def init_graph():
    ribs = list(list(None for i in range(7)) for _ in range(7))

    def add_ribs(x, y):

        ribs[x - 1][y - 1] = 1
        ribs[y - 1][x - 1] = 1


    add_ribs(1, 2)
    add_ribs(1, 3)
    add_ribs(1, 4)
    add_ribs(2, 3)
    add_ribs(2, 4)
    add_ribs(3, 4)
    add_ribs(3, 5)
    add_ribs(4, 5)
    add_ribs(5, 6)
    add_ribs(5, 7)
    add_ribs(6, 7)

    visualiser = GraphVisualiser(ribs=ribs, coordinates=[
        [100, 200], [100, 400], [300, 200], [300, 400], [500, 400], [700, 200], [700, 400]
    ], has_description=True)
    visualiser.set_description('Граф с заданными координатами')
    visualiser.next_step()
    visualiser.delete_vertex(4)
    visualiser.set_description('Удалена вершина с номером 4')
    visualiser.next_step()
    visualiser.show()

if __name__ == '__main__':
    init_graph()
