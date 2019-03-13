from visualizers.graph_visualiser import GraphVisualiser


def init_graph():
    ribs = list(list(None for i in range(14)) for _ in range(14))

    def add_ribs(x, y, weight=1):

        ribs[x - 1][y - 1] = weight

    add_ribs(1, 10, 5)
    add_ribs(2, 4, 15)
    add_ribs(2, 14, 4)
    add_ribs(3, 9, 1)
    add_ribs(13, 3, 7)
    add_ribs(3, 12, 8)
    add_ribs(6, 4, -1)
    add_ribs(12, 5, 1)
    add_ribs(6, 8, 3)
    add_ribs(6, 12, 99)
    add_ribs(8, 7, -10)
    add_ribs(10, 11)
    add_ribs(11, 12)

    visualiser = GraphVisualiser(ribs=ribs, has_description=True, directed=True, weighted=True)
    visualiser.set_description('Ориентированное взвешенное дерево')
    visualiser.next_step()
    visualiser.set_description('Помечены некоторые ребра')
    visualiser.set_ribs_color({
        (0, 9): 'blue',
        (9, 10): 'green',
        (5, 3): 'orange'
    })
    visualiser.next_step()
    visualiser.show()

if __name__ == '__main__':
    init_graph()
