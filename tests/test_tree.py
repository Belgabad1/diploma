from visualizers.graph_visualiser import GraphVisualiser


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
    visualiser.next_step()
    visualiser.set_vertex_border_color(5, 'red')
    visualiser.set_description('Стартовая вершина имеет номер 5')
    visualiser.next_step()
    visualiser.set_description('Из вершины с номером 5 можем пойти в вершина с номерами 7, 11, 3.\n'
                               'Добавляем в очередь вершины 7, 11, 3, помечаем 5 как пройденную.\n'
                               'Переходим в вершину 7.')
    visualiser.set_vertices_color({
        5: {'border': 'blue'},
        7: {'border': 'red'},
        11: {'border': 'green'},
        3: {'border': 'green'}
    })
    visualiser.next_step()
    visualiser.set_description('Удаляем вершину с номером 0.')
    visualiser.delete_vertex(0)
    visualiser.next_step()
    visualiser.set_description('Удаляем ребро (4, 11).')
    visualiser.delete_edge(4, 11)
    visualiser.next_step()
    visualiser.set_description('Помечаем ребра (2, 12), (10, 9), (7, 6).\n'
                               'Добавляем ребро (4, 11).')
    visualiser.set_ribs_color({
        (2, 12): 'turquoise',
        (10, 9): 'turquoise',
        (7, 6): 'turquoise'
    })
    visualiser.add_edge(4, 11)
    visualiser.next_step()
    visualiser.show()

if __name__ == '__main__':
    init_graph()
