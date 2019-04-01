from common.colors import COLORS
from visualizers.graph_visualiser import GraphVisualiser


def init_graph():
    ribs = [[None for _ in range(9)] for _ in range(9)]

    def add_ribs(x, y):

        ribs[x - 1][y - 1] = 1

    visualiser = GraphVisualiser(ribs=ribs, has_description=True,
                                 coordinates=[[i, 450] for i in range(200, 1100, 100)], labels=[
            'a', 'aba', 2, 3, 4, 5, 'label', 7, 8
        ]
    )
    color = list(COLORS.keys())
    for i in range(8):
        visualiser.set_vertex_area_color(i, color[i])
        visualiser.set_vertex_border_color(i, color[i + 1])
    visualiser.next_step()
    visualiser.show()

if __name__ == '__main__':
    init_graph()

