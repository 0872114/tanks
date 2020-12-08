import random
from config import Config


class GamepadController:

    def __init__(self, tank):
        self.tank = tank
        self.tank.direction = [0, 0]
        self.gamepad = None

    def on_motion(self, gamepad, axis, value):
        if axis == 'x':
            if value ** 2 == 1:
                self.tank.direction[0] = value
                self.tank.direction[1] = 0
            else:
                self.tank.direction[0] = 0

        if axis == 'y':
            if value ** 2 == 1:
                self.tank.direction[1] = -value
                self.tank.direction[0] = 0
            else:
                self.tank.direction[1] = 0

        self.tank.update_angle()

    def on_press(self, gamepad, button):
        if self.tank.stop:
            return

        self.tank.fire()

    def move(self):
        if self.tank.stop:
            return

        if any(self.tank.direction):
            self.tank.animate()
            self.tank.move(*self.tank.direction)


class EnemyController:

    def __init__(self, tank):
        self.tank = tank
        #self.direction = (self.tank.LEFT, self.tank.RIGHT,
        #                  self.tank.UP, self.tank.DOWN)[random.randrange(4)]
        self.direction = tank.direction
        self.default_direction = tank.direction
        self.prev_direction = None

    def move(self):
        if Config.DELETE_KILLED_TANKS and self.tank.destroy:
            # todo: tank.remove method?
            self.tank.level.remove_tank(self.tank)
        if self.tank.stop:
            return
        self.tank.animate()
        solution = random.randrange(128)
        # TODO: fix
        if solution in (1, 2):
            self.tank.fire()
        success = self.tank.move(*self.direction)
        if success is 5:
            success = self.tank.move(self.direction[1], self.direction[0])
        if not success:

            self.prev_direction = self.direction
            self.direction = (self.tank.LEFT, self.tank.RIGHT,
                              self.tank.UP, self.tank.DOWN)[random.randrange(4)]

        if self.prev_direction == self.direction:
            self.direction = (self.tank.LEFT, self.tank.RIGHT,
                              self.tank.UP, self.tank.DOWN)[random.randrange(4)]

        solution = random.randrange(1024)
        if solution == 4:
            self.direction = (self.default_direction[0], -self.default_direction[0])
        if solution == 5:
            self.direction = self.tank.LEFT
        if solution == 6:
            self.direction = self.tank.RIGHT
        elif solution in range(8, 24):
            self.direction = self.default_direction