
def itergrid(x, y, ox=0, oy=0):
    for _x in range(x):
        for _y in range(y):
            yield (_x+ox, _y+oy)

class Directions:
    up = '↑'
    down = '↓'
    left = '←'
    right = '→'
    dirs = {'left': 'right', 'right': 'left',
            'up': 'down', 'down': 'up'}

    @staticmethod
    def flip(d):
        return Directions.dirs[d]


class Cell:

    def __init__(self, x, y, passable=True):
        #position
        self.x = x
        self.y = y
        self.distance = 0
        
        #for pathing
        self.visited = False
        self.direction = None
        self.neighbors = {}

        #is a wall?
        self.passable = passable

    @property
    def pos(self):
        return(self.x, self.y)

    def surrounding(self):
        directions = {'up': (0, 1), 'down': (0, -1), 'left': (-1, 0), 'right': (1, 0)}
        return ((key, (self.x + value[0], self.y + value[1])) for key, value in directions.items())

    def __repr__(self):
        return '<Cell {}, {}>'.format(self.x, self.y)

    def __str__(self):
        if self.visited:
            return self.direction
        if not self.passable:
            return '█'
        return '.'

class Grid(dict):

    def __init__(self, x, y, walls):
        for col, row in itergrid(x, y):
            passable = False if (row, col) in walls else True
            if row not in self:
                self[row] = dict()
            self[row][col] = Cell(row, col, passable)
        
        for cell in self.traversable:
            self.fill_neighbors(cell)

    def fill_neighbors(self, cell):
        for direction, pos in cell.surrounding():
            # since we're just extending dict a -1 index will KeyError
            # 100% intentional because I don't want to do boundary checks
            x, y = pos
            try:
                if self[x][y].passable:
                    d = Directions.flip(direction)
                    self[x][y].neighbors[d] = cell
            except(KeyError):
                pass

    @property
    def somename(self):
        for cell in self.traversable:
            if not cell.visited and any(c.visited for c in cell.neighbors.values()):
                yield cell

    @property
    def traversable(self):
        for row, cols in self.items():
            for col, cell in cols.items():
                if cell.passable:
                    yield cell

    @property
    def printable(self):
        return [[str(col[1]) for col in sorted(row[1].items())] for row in sorted(self.items())]

    def __str__(self):
        return '\n'.join(' '.join(row) for row in self.printable)



