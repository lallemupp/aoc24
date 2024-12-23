from icecream import ic

from utils import read_input_file


class Node:
    def __init__(self, x: int, y: int, type_: str, anti_node=False):
        self.x = x
        self.y = y
        self.type = type_
        self.anti_node = anti_node

    def distance_to(self, other) -> int:
        distance_x = abs(self.x - other.x)
        distance_y = abs(self.y - other.y)
        return distance_x + distance_y

    def __str__(self):
        return f'{self.type}({self.x},{self.y})'


class Matrix:
    def __init__(self, data: list[str]):
        self.matrix: list[list[Node]] = []
        self.node_dict: dict[str: list] = {}
        for y, line in enumerate(data):
            row = []
            for x, char in enumerate(line):
                row.append(Node(x, y, char))
                if char != '.':
                    self.node_dict.setdefault(char, []).append(Node(x, y, char))
            self.matrix.append(row)

    def count_anti_nodes(self, all_=False) -> int:
        anti_nodes = []
        for char, nodes in self.node_dict.items():
            anti_nodes += self.find_anti_nodes(nodes, all_)
        for node in anti_nodes:
            self.matrix[node.y][node.x].anti_node = True
        sum_ = 0
        for row in self.matrix:
            for column in row:
                if column.anti_node:
                    sum_ += 1
        return sum_

    def find_anti_nodes(self, nodes: list[Node], all_: bool) -> list[Node]:
        anti_nodes: list[Node] = []
        for i, first_node in enumerate(nodes):
            for j, second_node in enumerate(nodes[i + 1:]):
                try:
                    if all_:
                        anti_nodes += self._find_line_anti_nodes(first_node, second_node)
                    else:
                        anti_nodes += self._find_anti_nodes(first_node, second_node)
                except IndexError:
                    break
        return anti_nodes

    def print(self):
        for row in self.matrix:
            for column in row:
                if column.anti_node:
                    if column.type != '.':
                        print(f'\033[95m{column.type}\033[0m', end='')
                    else:
                        print('#', end='')
                else:
                    print(column.type, end='')
            print()

    def _find_anti_nodes(self, first_node: Node, second_node: Node) -> list[Node]:
        diff_x: int = abs(first_node.x - second_node.x)
        diff_y: int = abs(first_node.y - second_node.y)
        if first_node.x > second_node.x:
            anti_nodes = (Node(first_node.x + diff_x, first_node.y - diff_y, '#', True),
                          Node(second_node.x - diff_x, second_node.y + diff_y, '#', True))
        else:
            anti_nodes = (Node(first_node.x - diff_x, first_node.y - diff_y, '#', True),
                          Node(second_node.x + diff_x, second_node.y + diff_y, '#', True))
        filtered_nodes = self.filter_out_invalid_anti_nodes(anti_nodes)
        for node in anti_nodes:
            if self.valid_anti_node(node):
                filtered_nodes.append(node)
        return filtered_nodes

    def _find_line_anti_nodes(self, first_node, second_node):
        diff_x: int = abs(first_node.x - second_node.x)
        diff_y: int = abs(first_node.y - second_node.y)
        anti_nodes = [Node(first_node.x, first_node.y, "#", True), Node(second_node.x, second_node.y, "#", True)]
        if first_node.x > second_node.x:
            x, y = first_node.x, first_node.y
            while 0 <= x < len(self.matrix[0]) and 0 <= y < len(self.matrix):
                x, y = x + diff_x, y - diff_y
                next_anti_node = Node(x, y, '#', True)
                anti_nodes.append(next_anti_node)
            x, y = second_node.x, second_node.y
            while 0 <= x < len(self.matrix[0]) and 0 <= y < len(self.matrix):
                x, y = x - diff_x, y + diff_y
                next_anti_node = Node(x, y, '#', True)
                anti_nodes.append(next_anti_node)
        else:
            x, y = first_node.x, first_node.y
            while 0 <= x < len(self.matrix[0]) and 0 <= y < len(self.matrix):
                x, y = x - diff_x, y - diff_y
                next_anti_node = Node(x, y, '#', True)
                anti_nodes.append(next_anti_node)
            x, y = second_node.x, second_node.y
            while 0 <= x < len(self.matrix[0]) and 0 <= y < len(self.matrix):
                x, y = x + diff_x, y + diff_y
                next_anti_node = Node(x, y, '#', True)
                anti_nodes.append(next_anti_node)
        filtered = self.filter_out_invalid_anti_nodes(anti_nodes)
        return filtered

    def filter_out_invalid_anti_nodes(self, anti_nodes) -> list[Node]:
        filtered = []
        for node in anti_nodes:
            if self.valid_anti_node(node):
                filtered.append(node)
        return filtered

    def valid_anti_node(self, anti_node: Node) -> bool:
        inside_x = 0 <= anti_node.x < len(self.matrix[0])
        inside_y = 0 <= anti_node.y < len(self.matrix)
        inside_matrix = inside_x > 0 and inside_y > 0
        if not inside_matrix:
            return False
        return inside_matrix


def main():
    data = read_input_file(file_name='day8')
    matrix = Matrix(data)
    ic(first(matrix))
    data = read_input_file(file_name='day8')
    matrix = Matrix(data)
    ic(second(matrix))


def first(matrix):
    return matrix.count_anti_nodes()


def second(matrix):
    return matrix.count_anti_nodes(all_=True)


if __name__ == '__main__':
    main()

# part 1 279 too high
# part 1 260 too low
# part 1 273 CORRECT!
# part 2 990 not correct