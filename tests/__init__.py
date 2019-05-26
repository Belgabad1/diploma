from common.colors import COLORS
from visualizers.graph_visualiser import GraphVisualiser


def init_graph():
    ribs = [[None for _ in range(9)] for _ in range(9)]

    def add_ribs(x, y):

        ribs[x - 1][y - 1] = 1

    visualiser = GraphVisualiser(ribs=[[1, 1], [1, 1]], has_description=False, directed=True,
                                 coordinates=[[200, 200], [500, 400]]
    )
    visualiser.next_step()
    visualiser.show()

if __name__ == '__main__':
    init_graph()

