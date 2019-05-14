from visualizers.graph_visualiser import GraphVisualiser
import random

def init_graph():
    ribs = list(list(None for i in range(15)) for _ in range(15))
    flows = list(list(None for i in range(15)) for _ in range(15))

    def add_ribs(x, y):
        weight = random.randint(0, 100)
        ribs[x - 1][y - 1] = weight
        ribs[y - 1][x - 1] = weight

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

    visualiser = GraphVisualiser(ribs=ribs, weighted=True, has_description=True)
    visualiser.visualize('kruskal')


if __name__ == '__main__':
    init_graph()
