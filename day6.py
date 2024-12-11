from icecream import ic
from utils import read_input_file
from enum import Enum


obstuction = '#'


class Direction(Enum):
    UP = '^'
    RIGHT = '>'
    DOWN = 'v'
    LEFT = '<'

    @staticmethod
    def from_value(char: str):
        switch = {
            '^': Direction.UP,
            '>': Direction.RIGHT,
            'v': Direction.DOWN,
            '<': Direction.LEFT
        }
        return switch[char]

    @staticmethod
    def transformation(direction) -> dict[str: int]:
        switch = {
            Direction.UP: {'x': 0, 'y': -1},
            Direction.RIGHT: {'x': 1, 'y': 0},
            Direction.DOWN: {'x': 0, 'y': 1},
            Direction.LEFT: {'x': -1, 'y': 0},
        }
        transformation = switch[direction]
        return transformation

    @staticmethod
    def next(current):
        switch = {
            Direction.UP: Direction.RIGHT,
            Direction.RIGHT: Direction.DOWN,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP
        }
        return switch.get(current)


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def apply_transformation(self, transformation: dict[str, int]):
        self.x += transformation['x']
        self.y += transformation['y']
        return self

    @staticmethod
    def from_(position, transformation=None):
        pos = Position(position.x, position.y)
        if transformation is not None:
            return pos.apply_transformation(transformation)
        else:
            return pos

    def __eq__(self, other):
        if type(other) != Position:
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x}, {self.y})"


class Map:
    def __init__(self, data: list[str]):
        self.map = data

    def position(self, position: Position) -> str:
        return self.map[position.y][position.x]

    def is_blocked(self, position: Position) -> bool:
        return self.map[position.y][position.x] == obstuction

    def in_bounds(self, position: Position) -> bool:
        if position.y >= len(self.map) or position.y < 0:
            return False
        if position.x >= len(self.map[0]) or position.x < 0:
            return False
        return True

    def add_block(self, position: Position):
        self._replace_in_map(position, obstuction)

    def remove_block(self, position: Position):
        self._replace_in_map(position, '.')

    def _replace_in_map(self, position: Position, char: str):
        string = self.map[position.y]
        new_string = string[:position.x] + char + string[position.x + 1:]
        self.map[position.y] = new_string

    def __len__(self):
        return len(map)

class Vector:
    def __init__(self, position: Position, direction: Direction):
        self.position = position
        self.direction = direction

    def __eq__(self, other):
        if type(other) != Vector:
            return False
        return self.position == other.position and self.direction == other.direction

    def __str__(self):
        return f'{self.direction.value}({self.position.x}, {self.position.y})'

    def __hash__(self):
        return hash((hash(self.position), hash(self.direction)))

class Guard:
    def __init__(self, vector: Vector):
        self.vector = vector

    def position(self) -> Position:
        return self.vector.position

    def rotate(self):
        self.vector.direction = self.vector.direction.next(self.vector.direction)

    def move(self, transformation: dict[str: int]):
        self.vector.position = self.vector.position.apply_transformation(transformation)

    def move_to(self, new_position: Vector):
        self.vector = new_position

    def __str__(self):
        return str(self.vector)


class Engine:
    def __init__(self, data: list[str]):
        self.map: Map = Map(data)
        self.guard: Guard = create_guard(self.map)
        self.visited_positions: set[Position] = {self.guard.vector.position}
        self.visited_vectors: set[Vector] = set()

    def step(self) -> bool:
        current_position = self.guard.vector.position
        transformation = Direction.transformation(self.guard.vector.direction)
        next_position: Position = Position.from_(current_position, transformation)
        in_bounds = self.map.in_bounds(next_position)
        if not in_bounds:
            return False
        is_next_blocked = self.map.is_blocked(next_position)
        if is_next_blocked:
            self.guard.rotate()
        else:
            new_vector = Vector(next_position, self.guard.vector.direction)
            self.guard.move_to(new_vector)
            self.visited_positions.add(new_vector.position)
        return True

    def is_loop(self) -> 1:
        continue_ = True
        while continue_:
            continue_ = self.step()
            if continue_:
                if self.guard.vector in self.visited_vectors:
                    return True
            self.visited_vectors.add(self.guard.vector)
        return False

    def reset(self, data, vector):
        self.map = Map(data)
        self.guard.vector = vector
        self.visited_vectors = set()
        self.visited_positions = set()

def create_guard(map_: Map):
    for y_index, row in enumerate(map_.map):
        for x_index, column in enumerate(row):
            try:
                return Guard(Vector(Position(x_index, y_index), Direction.from_value(column)))
            except KeyError:
                continue


def main():
    data = read_input_file(file_name='day6')
    ic(first(data))
    ic(second(data))


def first(data: list[str]):
    engine = Engine(data)
    continue_ = True
    while continue_:
        ic(str(engine.guard))
        continue_ = engine.step()
    return len(engine.visited_positions)


def second(data: list[str]):
    number_of_loops = 0
    for x in range(0, len(data)):
        for y in range(0, len(data)):
            engine = Engine(data.copy())
            to_test = Position(x, y)
            if to_test == engine.guard.position() or engine.map.is_blocked(to_test):
                continue
            engine.map.add_block(Position(x, y))
            if engine.is_loop():
                ic(str(to_test), 'is a loop')
                number_of_loops += 1
    return number_of_loops


if __name__ == '__main__':
    main()
