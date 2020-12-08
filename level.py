from interactive_object import InteractiveObject
from matrix import Matrix
from blocks import *
from effects import *
from tanks import *
from controllers import *
from layers import Layer, Frame
from config import Config
import arcade


class Level:

    blocks = [Flag, Brick, Armor, Water, Forest, PlayerRespawn, EnemyRespawn]
    effects = []

    def __init__(self):
        self.frame = Frame()
        # HACK: cannot use the same matrix with ground
        self.air = Layer(matrix=Matrix(Config.X_SIZE, Config.Y_SIZE))
        self.ground = Layer(matrix=Matrix(Config.X_SIZE, Config.Y_SIZE))

        print(id(self.ground.sprite_list), id(self.air.sprite_list))

        self.shells = Layer()
        self.tanks = Layer()
        self.respawns = dict()

        self.map = dict()

        self.controllers = []
        self.enemies = Config.ENEMIES
        arcade.schedule(self._animate_effects, 0.1)

        self.msg = ''

    def stop_all(self):
        arcade.unschedule(self._control_enemies)
        arcade.unschedule(self._move_tank_shells)
        arcade.unschedule(self._add_enemies)
        arcade.unschedule(self._animate_effects)

    def stop_game(self, msg):
        self.msg = msg
        arcade.unschedule(self._control_enemies)  # 1/60
        arcade.unschedule(self._move_tank_shells)
        arcade.unschedule(self._add_enemies)

    def start_game(self):
        self.msg = ''
        self.start_enemies()
        arcade.schedule(self._control_enemies, 1/60)  # 1/60
        arcade.schedule(self._move_tank_shells, 0.005)

    def start_enemies(self):
        self.enemies = Config.ENEMIES
        arcade.schedule(self._add_enemies, Config.ENEMIES_RESPAWN)

    def append(self, block_id, x, y):
        block_cls = self.blocks[block_id]
        block = block_cls(x, y)
        # foreground and background

        if block.logical:
            layer = self.frame
            if layer.add_item(block):
                mx, my = Config.m_point(x, y)
                self.map[block] = block_id, mx, my
                self.respawns[(x, y)] = block
            return

        if block.overlay:
            layer = self.air
        else:
            layer = self.ground
        if layer.append(block):
            mx, my = Config.m_point(x, y)
            self.map[block] = block_id, mx, my

    def add_item(self, block_cls, x, y):
        block = block_cls(x, y)
        # foreground and background
        if block.overlay:
            layer = self.air
        else:
            layer = self.ground
        layer.append(block)

    def get(self, x, y):
        return self.ground.get(x, y)

    def remove(self, x, y):
        _removed = self.frame.remove_item(x, y)
        if _removed:
            if self.map.get(_removed):
                del self.map[_removed]
                return True

        layer = self.ground
        item = layer.get(x, y)
        if item is None:
            layer = self.air
            item = layer.get(x, y)
        if not item:
            return False
        layer.remove(item)
        if self.map.get(item):
            del self.map[item]
            return True
        return False

    def save(self):
        with open('levels/byte.bin', 'wb') as f:
            for block_id, mx, my in self.map.values():
                f.write(bytes([block_id, mx, my]))

    def load(self):
        with open('levels/byte.bin', 'rb') as f:
            eof = False
            while not eof:
                item = f.read(3)
                if not item:
                    eof = True
                    continue
                block_id, mx, my = item
                block_cls = self.blocks[block_id]
                abs_x, abs_y = Config.abs_point(mx, my, block_cls.tile_size)
                self.append(item[0], abs_x, abs_y)

    # Tanks

    def add_tank(self, cls_tank, x, y, controller_cls=None):
        tank = cls_tank(self, x, y)
        # TODO: fix
        self.tanks.append(tank)
        if controller_cls is None:
            ctrl = EnemyController(tank)
        else:
            ctrl = controller_cls(tank)
        self.controllers.append(ctrl)
        return ctrl

    def remove_tank(self, tank):
        self.tanks.remove(tank)


    def add_shell(self, cls):
        self.shells.append(cls)

    @classmethod
    def add_effect(cls, effect_cls):
        cls.effects.append(effect_cls)
        return True

    # Timers

    def _control_enemies(self, _):
        if not self.controllers:
            return

        enemies = 0
        game_over = True
        for c_id, controller in enumerate(self.controllers):
            if isinstance(controller, EnemyController):
                enemies += 1
            if isinstance(controller, GamepadController):
                game_over = False
                self.msg = ''
            if controller.tank.destroy:
                print('DESTROYED')
                del self.controllers[c_id]
            controller.move()

        if game_over:
            self.msg = Config.MSG_PLAYERS_KILLED

        if not self.enemies and not enemies:
            for (x, y), respawn in self.respawns.items():
                if isinstance(respawn, EnemyRespawn):
                    self.add_effect(Explosion(x, y))
            self.stop_game(Config.MSG_WIN)

    def _move_tank_shells(self, _):
        # todo: refactor
        for n, shell in enumerate(self.shells):
            if shell.flying and not shell.fly():
                shell.flying = False
            if shell.destroy and shell in self.shells:
                self.shells.remove(shell)
                if shell in self.shells._items:
                    del self.shells._items[n]

    def _animate_effects(self, _):
        for block_id, block in enumerate(self.effects):
            if block is None:
                continue
            if block.destroy:
                del self.effects[block_id]
                del block
                continue
            block.animate()

    def _add_enemies(self, _):
        if self.enemies <= 0:
            arcade.unschedule(self._add_enemies)
            return

        for (x, y), respawn in self.respawns.items():
            if isinstance(respawn, EnemyRespawn):
                self.enemies -= 1
                self.add_tank(Tank2, x, y)
                if self.enemies <= 0:
                    break
