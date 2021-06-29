from typing import List
from random import randint

class Node:
    def __init__(self, _cost: int, _cost_from_start: int, _visited: bool = False):
        self.cost = _cost  # cost of node
        self.cost_from_start = _cost_from_start  # cost from the start
        self.visited = _visited  # has this node been visited yet
        self.neighbours = {}  # dict that contains neibourghing noded
        self.previous = None
        self.active = False  # (for building graph representation)

'''
Generate Plane
'''

class GenerateGraph:
    def __init__(self, verticies :List[int]):
        '''
        Description:
        Parameters:
        > maxNodeCost: -> int
            maximum cost that one node can have
        > rows: -> int
            vertical dimension of the plane
        > cols: -> int
            horizontal dimension of the plane
        '''
        self.rows = len(verticies)
        self.cols = len(verticies[0])
        self._result_plane = []
        self._verticies = verticies

        '''Start Finish'''
        self.s_x = None
        self.s_y = None
        self.f_x = None
        self.f_y = None

        self._append_values()
        self._set_start_finish()
        self._append_neibourghs()

    def get_plane(self):
        return self._result_plane

    def n_of_verticies(self):
        return self.rows * self.cols

    def set_start(self, new_x, new_y):
        self.s_x = new_x
        self.s_y = new_y

    def set_finish(self, new_x, new_y):
        self.f_x = new_x
        self.f_y = new_y

    def get_start(self):
        return self._result_plane[self.s_y][self.s_x]

    def get_finish(self):
        return self._result_plane[self.f_y][self.f_x]

    def _append_values(self) -> None:
        node_cost_start = float('inf')
        node_visited = False

        # iterate through rows
        for row in self._verticies:
            # iterate through columns
            row_content = []
            for vertex_cost in row:
                node = Node(vertex_cost, node_cost_start, node_visited)
                row_content.append(node)  # insert random node
            self._result_plane.append(row_content)

    def _set_start_finish(self) -> None:
        '''
        This function generates starting end ending point on the plane.
        It returns the coordinates to the starting end ending point.
        '''
        ''' CONCEPT 1
        points = [
            # Pair of points
            [[1,1], [9,9]],
            [[0,9], [9,0]],
            ]
        start_x, start_y = randint(0, self.cols), randint(0, self.rows)
        finish_x, finish_y = randint(0, self.cols), randint(0, self.rows)
        '''

        ''' APPEND POINTS TO PLANE '''

        self._set_point(self.s_x, self.s_y)
        self._set_point(self.f_x, self.f_y)

    def _set_point(self, x: int, y: int, cost: int = 0) -> None:
        for row in range(self.rows):
            if row == y:
                for col in range(self.cols):  # iterate through columns in a row
                    if col == x:
                        self._result_plane[y][x].cost = cost  # change cost of the node object

    def _append_neibourghs(self):
        '''
            ... 1   2   3
            ... 4   5   6
            ... 7   8   9
        '''
        for row in range(0, self.rows):
                for col in range(0, self.cols):  # iterate through columns in a row
                    # set neibourghs to current node
                    current_node = self._result_plane[row][col]
                    try:
                        # if there is a node on the right side of the current node
                        if col < self.cols - 1:
                            neibourgh = self._result_plane[row][col+1]
                            current_node.neighbours[neibourgh] = neibourgh.cost

                        # if there is a node on the left side of the current node
                        if col > 0:
                            neibourgh = self._result_plane[row][col-1]
                            current_node.neighbours[neibourgh] = neibourgh.cost

                        # if there is a node on above the current node
                        if row > 0:
                            neibourgh = self._result_plane[row-1][col]
                            current_node.neighbours[neibourgh] = neibourgh.cost

                        # if there is a node on below the current node
                        if row < self.rows - 1:
                            neibourgh = self._result_plane[row+1][col]
                            current_node.neighbours[neibourgh] = neibourgh.cost
                    except IndexError as s:  # if there is no
                        print('Out or range')
                        print(current_node.cost)
                        print(f'neighbours: \t{[nei.cost for nei in current_node.neighbours]}\n')

    def print_plane(self) -> None:
        # plane dimensions
        width = len(self._result_plane[0])
        height = len(self._result_plane)

        print('\nUnmodified plane:')
        horizontal_line = '| '+ (width)*'= ' +'|'
        print(horizontal_line)

        for x in self._result_plane:
            row = '|'
            for y in x:
                row += ' ' + str(y.cost)
            row += ' |'
            print(row)
        print(horizontal_line)

    def print_plane_after_dijkstra(self) -> None:
        # plane dimensions
        width = len(self._result_plane[0])
        height = len(self._result_plane)

        print('Shortest path:')
        horizontal_line = '| '+ (width)*'= ' +'|'
        print(horizontal_line)

        for x in self._result_plane:
            row = '|'
            for y in x:
                if (y.active):
                    row += ' ' + str(y.cost)
                else: row += '  '
            row += ' |'
            print(row)
        print(horizontal_line)

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, node: Node) -> Node:

        neighbour_cost = node.neighbours.values()  # list that holds cost of each neighbour node
        index_of_min_node = neighbour_cost.index(min(neighbour_cost))

        # return node with minimum cost
        return node.neighbours.keys()[index_of_min_node]

    def dijkstra(self) -> None:
        start_node = self.get_start()
        finish_node = self.get_finish()
        dijkstra_table = {}

        # fill dijkstra table with all the nodes
        for row in range(0, len(self._result_plane)):
            for col in range(0, len(self._result_plane[row])):
                node = self._result_plane[row][col]
                if node != start_node:
                    dijkstra_table[node] = [float('inf'), None]  # append infinity as a distance to every node
                else:
                    dijkstra_table[node] = [0, None]

        visited = []
        current_distance = 0

        # dijkstra table[node] = [cost from the beginning, previous node]
        '''
            | NODE | COST | PREVIOUS
            |   A     3        B
        '''

        def iterate_through_neighbours(current_node, current_distance):
            # iterate through neighbouring nodes
            # print(f'Neibghours: {current_node.neighbours.values()}')

            # current_node.neighbours = {'NODE': cost}
            for neighbour, distance in current_node.neighbours.items():
                # if neighbour in visited: return 0
                new_distance = distance + current_distance

                if dijkstra_table[neighbour][0] > new_distance:
                    dijkstra_table[neighbour][0] = new_distance  # update cost
                    dijkstra_table[neighbour][1] = current_node  # update previous node
                    iterate_through_neighbours(neighbour, new_distance)
                else:
                    continue

        iterate_through_neighbours(start_node, current_distance)
        self.applyDijkstra(dijkstra_table, start_node, finish_node)

    def applyDijkstra(self, dijkstra_table: dict, start_node: Node, finish_node: Node) -> None:
        start_node.active, finish_node.active = True, True
        # iterate through previous nodes until it reaches first one
        previous_node = dijkstra_table[finish_node][1]
        while previous_node != start_node:
            previous_node.active = True
            # previous_node.cost = '-'
            previous_node = dijkstra_table[previous_node][1]
