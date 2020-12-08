from interactive_object import InteractiveObject
from effects import Explosion
from config import Config
from blocks import Brick, Armor, Flag, CapturedFlag


class TankShell(InteractiveObject):
    tile_coords = [(40, 12.5)]
    matrix = [[1, 1],
              [1, 1]]

    def __init__(self, tank):
        super().__init__(tank.x, tank.y)
        self.tank = tank
        self.direction = (0, 1)
        self.position = [0, 1]
        self.flying = False

    def fire(self):
        self.x = self.tank.x
        self.y = self.tank.y

        self.position = self.tank.position[:]
        if self.position == (0, 0):
            self.destroy = True
            return False

        dx, dy = self.position
        angle = -90 * dx
        if dy < 0:
            angle -= 180
        self.sprite.angle = angle
        self.destroy = False
        self.flying = True
        return True

    def fly(self):
        dx, dy = self.position
        if self.destroy or not self.flying:
            self.x = 0
            self.y = 0
            return False

        self.x += dx
        self.y += dy
        self.sprite.set_position(self.x, self.y)

        barriers = self.tank.background.get_barriers(self, dx, dy)
        if barriers:
            for _, _, item in barriers:
                if isinstance(item, Brick) or isinstance(item, Armor) or item is None:
                    self.flying = False
                    self.destroy = True
                if isinstance(item, Brick):
                    self.tank.level.remove(item.x, item.y)
                    # Brick corrupt angle!
                if isinstance(item, Flag):
                    self.tank.level.add_effect(Explosion(item.x, item.y))
                    self.tank.level.remove(item.x, item.y)
                    self.tank.level.add_item(CapturedFlag, item.x, item.y)
                    self.tank.level.stop_game(Config.MSG_GAME_OVER)

        point1 = Config.m_point(self.x + dx,
                                self.y + dy)
        for tank in self.tank.level.tanks:
            point2 = Config.m_point(tank.x, tank.y)
            if tank is not self.tank and \
                    [x // 2 for x in point1] == [x // 2 for x in point2]:

                if Config.FRIENDLY_FIRE or tank.team != self.tank.team:
                    if not tank.destroy:
                        self.tank.level.add_effect(Explosion(tank.x, tank.y))
                    tank.stop = True
                    tank.destroy = True

                if not Config.PATH_THROUGH_KILLED or not tank.destroy:
                    self.flying = False
                    self.destroy = True
                    return False

        self.x += dx
        self.y += dy
        self.sprite.set_position(self.x, self.y)
        return True
