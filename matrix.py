from copy import copy
import pickle
import os
from config import Config


class Matrix:

    def __init__(self, x_size=10, y_size=20):
        self.coord = dict()
        self.x_size = x_size
        self.y_size = y_size

    def _append(self, item, x0, y0):
        m = item.matrix
        for x, row in enumerate(m):
            for y, val in enumerate(row):
                self.coord[(x0 + x, y0 + y)] = item

    def append(self, item):
        m = item.matrix
        x0, y0 = Config.m_point(item.x, item.y)
        m_points = []
        for x, row in enumerate(m):
            for y, val in enumerate(row):
                m_points.append((x0 + x, y0 + y))
                if any([x0 + x >= self.x_size,
                        y0 + y >= self.y_size,
                        x0 + x < 0,
                        y0 + y < 0,
                        self.coord.get((x0 + x, y0 + y)) is not None]):
                    return False
        self._append(item, x0, y0)
        return m_points

    def get(self, x, y):
        mx, my = Config.m_point(x, y)
        return self.coord.get((mx, my))

    def remove(self, x, y):
        if self.coord.get((x, y)):
            del self.coord[(x, y)]
            return True
        return False

    def clear(self):
        self.coord = dict()

    def get_barriers(self, item, dx, dy):
        x0, y0 = Config.m_point(item.x - Config.BLOCK_SIZE // 2 + dx * Config.BLOCK_SIZE // 2,
                                item.y - Config.BLOCK_SIZE // 2 + dy * Config.BLOCK_SIZE // 2)
        barriers = []
        for x, row in enumerate(item.matrix):
            for y, val in enumerate(row):
                if val:
                    if any([x0 + x >= self.x_size,
                            y0 + y >= self.y_size,
                            x0 + x < 0,
                            y0 + y < 0]):
                        barriers.append((x0 + x, y0 + y, None))
                    if self.coord.get((x0 + x, y0 + y)) is not None:
                        barriers.append((x0 + x, y0 + y, self.coord[x0 + x, y0 + y]))
        return barriers


    # Unneed

    def collision(self, m, x0, y0):
        collisions = []
        for x, row in enumerate(m):
            for y, val in enumerate(row):
                if val:
                    if any([x0 + x > self.x_size, y0 + y > self.y_size,
                            x0 + x <= 0, y0 + y <= 0]):
                        return None
                    if self.coord.get((x0 + x, y0 + y)) is not None:
                        collisions.append((x0 + x, y0 + y, self.coord[x0 + x, y0 + y]))
        return collisions

    def set(self, value, x, y):
        if self.coord.get((x, y)) is None:
            return False
        self.coord[(x, y)] = value


    def put(self, m, x0, y0):
        coord = {}
        for x, row in enumerate(m):
            for y, val in enumerate(row):
                if val:
                    if any([x0 + x > self.x_size,
                            y0 + y > self.y_size,
                            x0 + x < 1,
                            x0 + x < 1,
                            self.coord.get((x0 + x, y0 + y)) is not None]):
                        return False
                    else:
                        coord[(x0 + x, y0 + y)] = val
        for key, val in coord.items():
            self.coord[key] = val
        return True

    def move(self, delta_x, delta_y, stop=True):
        coord = {}
        for (x, y), val in self.coord.items():
            if 0 < x + delta_x <= self.x_size and 0 < y + delta_y <= self.y_size:
                coord[(x + delta_x, y + delta_y)] = val
            elif stop:
                return False

        self.coord = coord
        return True

    def badaadd(self, other):
        coord = copy(self.coord)
        for (x, y), val in other.coord.items():
            if self.coord.get((x, y)) is not None:
                #print(self.coord, other.coord)
                return False
            else:
                coord[(x, y)] = val
        return True

    def __add__(self, other):
        coord = copy(self.coord)
        for (x, y), val in other.coord.items():
            if self.coord.get((x, y)) is not None:
                #print(self.coord, other.coord)
                return False
            else:
                coord[(x, y)] = val
        return True

    def fire(self, other):
        barriers = []
        for (x, y), val in other.coord.items():
            if self.coord.get((x, y)) is not None:
                barriers.append((x, y, self.coord.get((x, y))))
        return barriers

    def add(self, other):
        coord = copy(self.coord)
        for (x, y), val in other.coord.items():
            if self.coord.get((x, y)) is not None:
                return False
            else:
                coord[(x, y)] = val
        for key, val in coord.items():
            self.coord[key] = val
        return True

    def get_min_coord(self):
        x0 = self.x_size
        y0 = self.y_size
        for x, y in self.coord.keys():
            if x < x0:
                x0 = x
            if y < y0:
                y0 = y
        return x0, y0

    def extract_matrix(self):
        x0, y0 = self.get_min_coord()
        matrix = []
        xmax = ymax = 0
        for x, y in self.coord.keys():
            if xmax < x - x0:
                xmax = x - x0
            if ymax < y - y0:
                ymax = y - y0
        print('max', xmax, ymax)
        for x in range(xmax+1):
            row = []
            for y in range(ymax+1):
                row.append(0)
            matrix.append(row)
        print('M',matrix)
        for (x, y), val in self.coord.items():
            print(x, y)
            matrix[x-x0][y-y0] = val
            print(matrix[x-x0][y-y0])
        return matrix

    def get_full_lines(self):
        full_lines = []
        y_exist = []
        for x, y in self.coord.keys():
            if y not in y_exist:
                line_is_full = True
                for i in range(1, self.x_size+1):
                    if self.coord.get((i, y)) is None:
                        line_is_full = False
                        break
                if line_is_full:
                    full_lines.append(y)
            y_exist.append(y)
        return full_lines

    def drop(self):
        full_lines = self.get_full_lines()
        coord = {}
        counter = len(set(full_lines))
        for y0 in sorted(full_lines):
            for (x, y), val in self.coord.items():
                if y < y0:
                    coord[(x, y+1)] = self.coord[(x, y)]
                elif y > y0:
                    coord[(x, y)] = self.coord[(x, y)]
        self.coord = coord
        return counter

    def save(self, filename):
        i = 0
        path = filename
        while os.path.isfile(path):
            i += 1
            name = os.path.basename(filename).split('.')
            path = os.path.dirname(filename) + '/' + name[0] + str(i) + '.' + name[1]
        with open(path, 'wb') as f:
            pickle.dump(self.coord, f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            self. coord = pickle.load(f)
