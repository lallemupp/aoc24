from utils import read_input_file, Point
from matrix import centered_submatrix_from
from icecream import ic


class ElevationPoint(Point):
    def __init__(self, x: int, y: int, elevation: str):
        Point.__init__(self, x, y)
        self.elevation: str = elevation

    def __eq__(self, other):
        if type(other) is not type(self):
            return False
        return super.__eq__(self, other) and int(self.elevation) == int(other.elevation)

    def __str__(self):
        return f'{self.elevation}({self.x}, {self.y})'

    def __lt__(self, other):
        return int(self.elevation) < int(other.elevation)

    def __gt__(self, other):
        return int(self.elevation) > int(other.elevation)

    def is_next(self, other):
        try:
            return (int(other.elevation) - int(self.elevation)) == 1
        except ValueError:
            return False

    def __hash__(self):
        return hash(f'{self.x}{self.y}')


class Map:
    def __init__(self, data: list[str]):
        self.points = []
        self.start_points = []
        for y, row in enumerate(data):
            for x, char in enumerate(row):
                try:
                    self.points[y].append(ElevationPoint(x, y, char))
                except IndexError:
                    self.points.append([ElevationPoint(x, y, char)])
                if char == '0':
                    self.start_points.append(ElevationPoint(x, y, '0'))

    def find_trail_heads(self) -> int:
        trail_heads = 0
        for start_point in self.start_points:
            found_heads = set()
            self.find_next(start_point, found_heads)
            print(f'found heads at {[str(head) for head in found_heads]}')
            trail_heads += len(found_heads)
        return trail_heads

    def find_next(self, current: ElevationPoint, found: set[ElevationPoint]):
        print(f'checking {current}')
        if self.points[current.y][current.x].elevation == '9':
            found.add(current)
        else:
            sub_matrix = centered_submatrix_from(self.points, 1, current.x, current.y)
            sub_matrix = modified_matrix(sub_matrix, current)
            for row in sub_matrix:
                for point in row:
                    if current.is_next(point):
                        self.find_next(point, found)

    def find_ratings(self):
        ratings = 0
        for start_point in self.start_points:
            print(f'starting point {start_point}')
            ratings += self.find_next_node(start_point, 0)
        return ratings

    def find_next_node(self, current: ElevationPoint, rating: int) -> int:
        print(f'checking {current}')
        if current.elevation == '9':
            rating += 1
            return rating
        else:
            sub_matrix = centered_submatrix_from(self.points, 1, current.x, current.y)
            sub_matrix = modified_matrix(sub_matrix, current)
            sum_ = 0
            for row in sub_matrix:
                for point in row:
                    if current.is_next(point):
                        sum_ += self.find_next_node(point, rating)
        print(f'Dead end {rating}')
        return sum_

    def __str__(self):
        lists = []
        for y, column in enumerate(self.points):
            for point in column:
                try:
                    lists[y].append(point.elevation)
                except IndexError:
                    lists.append([point.elevation])
        result = ''
        for a_list in lists:
            result += ''.join(a_list)
            result += '\n'
        return result


def modified_matrix(matrix: list[list], center: ElevationPoint) -> list[list]:
    modified = matrix.copy()
    for y, column in enumerate(matrix):
        for x, point in enumerate(column):
            if not point.is_ortho_to(center):
                modified[y][x] = ElevationPoint(x, y, '.')
    return modified


def main():
    data = read_input_file(file_name='day10')
    # ic(first(data))
    ic(second(data))


def first(data: list[str]) -> int:
    map_ = Map(data)
    return map_.find_trail_heads()


def second(data: list[str]) -> int:
    map_ = Map(data)
    return map_.find_ratings()

if __name__ == '__main__':
    main()

# part 2: 4497932914 to high