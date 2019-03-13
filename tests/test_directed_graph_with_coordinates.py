from visualizers.graph_visualiser import GraphVisualiser


def init_graph():
    ribs = list(list(None for i in range(8)) for _ in range(8))

    def add_ribs(x, y):

        ribs[x - 1][y - 1] = 1

    add_ribs(1, 2)
    add_ribs(3, 1)
    add_ribs(1, 4)
    add_ribs(2, 3)
    add_ribs(4, 2)
    add_ribs(3, 4)
    add_ribs(3, 5)
    add_ribs(5, 4)
    add_ribs(5, 6)
    add_ribs(5, 7)
    add_ribs(6, 7)
    add_ribs(3, 8)
    add_ribs(8, 6)

    visualiser = GraphVisualiser(ribs=ribs, coordinates=[
        [100, 200], [100, 400], [300, 200], [300, 400], [500, 400], [700, 200], [700, 400], [500, 300]
    ], has_description=True, directed=True)
    visualiser.set_description('Ориентированный граф с заданными координатами')
    visualiser.next_step()
    visualiser.delete_vertex(4)
    visualiser.set_description('Удалена вершина с номером 4')
    visualiser.next_step()
    visualiser.show()

if __name__ == '__main__':
    init_graph()
