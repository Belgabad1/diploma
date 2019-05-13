from visualizers.graph_visualiser import GraphVisualiser

K = 4

def init_graph():
    ribs = list(list(None for i in range(K)) for _ in range(K))
    flows = list(list(None for i in range(K)) for _ in range(K))

    def add_ribs(x, y, flow=1, doubled=False):

        ribs[x - 1][y - 1] = 1
        ribs[y - 1][x - 1] = 1

    for i in range(1, K + 1):
        for j in range(i + 1, K + 1):
            add_ribs(i, j)

    visualiser = GraphVisualiser(ribs=ribs)
    visualiser.next_step()
    visualiser.show()

if __name__ == '__main__':
    init_graph()
