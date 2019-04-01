from visualizers.graph_visualiser import GraphVisualiser


def init_graph():
    ribs = list(list(None for i in range(7)) for _ in range(7))
    flows = list(list(None for i in range(7)) for _ in range(7))

    def add_ribs(x, y, flow=1, doubled=False):

        ribs[x - 1][y - 1] = 1
        flows[x - 1][y - 1] = flow

    add_ribs(1, 2, 5, doubled=True)
    add_ribs(1, 3, 6)
    add_ribs(1, 4, 4)
    add_ribs(4, 2, 6, doubled=True)
    add_ribs(3, 4, 9)
    add_ribs(3, 5, 10)
    add_ribs(5, 4, 1)
    add_ribs(5, 6, 8)
    add_ribs(5, 7, 2)
    add_ribs(6, 7, 3)

    visualiser = GraphVisualiser(ribs=ribs, coordinates=[
        [100, 200], [100, 600], [400, 200], [400, 600], [700, 600], [1000, 200], [1000, 600]
    ], has_description=True, directed=True, weighted=True, has_flow=True, flows=flows)
    visualiser.set_description('Ориентированный граф с заданными координатами')
    visualiser.set_flows({
        (2, 7): 4,
        (5, 6): 1,
        (0, 1): 4,
        (3, 1): 4,
    })
    visualiser.next_step()
    visualiser.add_vertex([700, 400])
    visualiser.add_edge(2, 7, max_flow=4)
    visualiser.add_edge(7, 5, max_flow=6)
    visualiser.set_description('Добавлена вершина 7 и ребра (2, 7), (7, 5)')
    visualiser.next_step()
    visualiser.delete_vertex(4)
    visualiser.set_description('Удалена вершина с номером 4')
    visualiser.next_step()
    visualiser.set_flows({
        (2, 7): 4,
        (5, 6): 1,
        (0, 1): 4,
        (3, 1): 4,
    })
    visualiser.set_description('Меняем поток для некоторых ребер')
    visualiser.next_step()
    visualiser.show()

if __name__ == '__main__':
    init_graph()
