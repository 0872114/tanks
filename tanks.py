from interactive_object import InteractiveObject
from matrix import Matrix
from tank_shell import TankShell
from uuid import uuid4
from config import Config
import arcade
from blocks import Brick, Armor, Water, Forest, Flag
from effects import Explosion


class Tank(InteractiveObject):
    tile_coords = [(0, 0), (1, 0),
                   (0, 1), (1, 1),
                   (0, 2), (1, 2),
                   (0, 3), (1, 3),
                   (0, 4), (1, 4)]
    matrix = [[1, 1], [1, 1]]
    tile_size = 32

    UP = (0, 1)
    DOWN = (0, -1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    team = 1

    tanks = [
        dict(
            speed=1,
            shots=1,
        ),
        dict(
            speed=0.5,
            shots=1,
        ),
        dict(
            speed=1,
            shots=2,
        ),
        dict(
            speed=.25,
            shots=2,
        ),
        dict(
            speed=0.5,
            shots=4,
        ),
    ]

    _shells = 2

    def __init__(self, level, x, y):
        self.uid = uuid4()

        super().__init__(x, y)

        self.foreground = Matrix(Config.X_SIZE, Config.Y_SIZE)
        self.background = level.ground.matrix

        self.direction = [0, 1]
        self.position = [0, 1]
        self.can_move = True
        self.stop = False

        self.tank_type = 0 #
        self.stars = 0
        self.lives = 4

        self.speed = 1#
        self.tick = 0

        self.friendly_fire = 1
        self.destroy = False

        # ammo
        self.level = level
        self.shells = list()
        for _ in range(self._shells):
            shell = TankShell(self)
            self.shells.append(shell)

        self.barriers = {1, 2, 3, 6} #

        self.respawn(x, y)
        self.current_texture = 0

    def respawn(self, x, y):
        self.direction = [0, 1]
        self.stars = 0
        self.lives = 3
        self.tick = 0

    def fire(self):
        for shell in self.shells:
            if not shell.flying:
                self.level.add_shell(shell)
                shell.fire()
                break

    def update_angle(self):
        if self.stop:
            return

        if any(self.direction):
            dx, dy = self.direction
            angle = -90 * dx
            if dy < 0:
                angle -= 180
            self.sprite.angle = angle

    def move(self, dx, dy):
        if self.destroy:
            return
        # For new ones
        if not self.sprite:
            return

        self.direction = [dx, dy]
        if any(self.direction):
            self.position = self.direction[:]

        # todo: adjuster to conf or _method?
        if dy:
            self.x = round(self.x / Config.BLOCK_SIZE, 0) * Config.BLOCK_SIZE
        if dx:
            self.y = round(self.y / Config.BLOCK_SIZE, 0) * Config.BLOCK_SIZE

        barriers = self.background.get_barriers(self, dx, dy)
        if barriers:
            for _, _, item in barriers:
                if isinstance(item, Brick) or isinstance(item, Armor) \
                        or isinstance(item, Water) or isinstance(item, Flag) \
                        or item is None:
                    return False

        point1 = Config.m_point(self.x + dx * Config.BLOCK_SIZE,
                                self.y + dy * Config.BLOCK_SIZE)
        for tank in self.level.tanks:
            point2 = Config.m_point(tank.x, tank.y)
            if tank is not self and [x // 2 for x in point1] == [x // 2 for x in point2]:
                # TODO: tank.offset x y\
                if not tank.destroy or tank.team == self.team:
                    return
                if Config.MOVE_KILLED_TANKS:
                    tank.x = self.x + dx * self.tile_size
                    tank.y = self.y + dy * self.tile_size
                    tank.sprite.set_position(self.x + dx * self.tile_size, self.y + dy * self.tile_size)

        self.x += dx
        self.y += dy
        self.sprite.set_position(self.x, self.y)

        # to update fn?
        angle = -90 * dx
        if dy < 0:
            angle -= 180
        self.sprite.angle = angle

        return True

    def animate(self):
        if self.current_texture % 2:
            self.current_texture -= 1
        else:
            self.current_texture += 1

        if self.sprite:
            self.sprite.set_texture(self.current_texture)

    def move_shells(self):
        for shell in self.shells:
            if shell.flying:
                shell.fly()


class Tank2(Tank):
    tile_coords = [(8, 0), (9, 0),
                   (8, 1), (9, 1),
                   (8, 2), (9, 2),
                   (8, 3), (9, 3),
                   (8, 4), (9, 4)]
    matrix = [[2, 2], [2, 2]]
    team = 2
    _shells = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction = (0, -1)
        self.friendly_fire = 2
