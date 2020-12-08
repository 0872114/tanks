import arcade
from level import Level
from config import Config
from tanks import Tank
from controllers import GamepadController
from blocks import PlayerRespawn
from matrix import Matrix
from interactive_object import InteractiveObject


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT,
                         Config.SCREEN_TITLE, resizable=False)

        self.level = Level()

        self.current_brush = 1
        self.brush_on = False

        self.buttons_down = set()

    def setup_gamepads(self):
        gamepads = arcade.get_game_controllers()
        if gamepads:
            for gamepad in gamepads:
                for (x, y), ctrl in self.level.respawns.items():
                    if isinstance(ctrl, GamepadController) and ctrl.gamepad == gamepad:
                        break
                    if isinstance(ctrl, PlayerRespawn):
                        gamepad.open()
                        ctrl = self.level.add_tank(Tank, x, y, GamepadController)
                        ctrl.gamepad = gamepad
                        gamepad.on_joybutton_press = ctrl.on_press
                        gamepad.on_joyaxis_motion = ctrl.on_motion
                        self.level.respawns[(x, y)] = ctrl
                        break

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()

        if self.level.frame.enabled:
            # todo: draw sprite of current, level - add brush sprite
            self.level.frame.draw()
            self.level.frame.sprite_list.draw()

        self.level.ground.draw()
        self.level.shells.draw()
        self.level.tanks.draw()
        self.level.air.draw()

        for block in self.level.effects:
            if block is not None and block.overlay:
                arcade.draw_texture_rectangle(block.x, block.y,
                                              block.tile_size, block.tile_size, block.texture)

        arcade.draw_text(str(self.level.msg),
                         Config.SCREEN_WIDTH // 2,
                         Config.SCREEN_HEIGHT // 2,
                         (200, 0, 0), font_size=18, font_name='arial', bold=True, anchor_x="center",
                         anchor_y="center")

    def on_key_press(self, key, key_modifiers):
        print(key)

        if key in (
                arcade.key.UP,
                arcade.key.DOWN,
                arcade.key.LEFT,
                arcade.key.RIGHT,
        ):
            self.buttons_down = {key}

        if key == arcade.key.SPACE:
            self.level.test()

        if key == arcade.key.S:
            self.level.save()

        if key in ('30064771072', arcade.key.J):
            self.setup_gamepads()

        if key == arcade.key.L:
            self.level.load()

        if key == arcade.key.R:
            self.level.stop_all()
            self.level = Level()
            self.level.load()
            self.setup_gamepads()
            self.level.start_game()

        if key == arcade.key.W:
            self.setup_gamepads()
            self.level.start_game()

        if key == arcade.key.F:
            self.level.frame.enabled = not self.level.frame.enabled

        if key == arcade.key.B:
            self.current_brush += 1
            if self.current_brush >= len(self.level.blocks):
                self.current_brush = 0

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in self.buttons_down:
            self.buttons_down.remove(symbol)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.level.append(self.current_brush, x, y)
            self.brush_on = True

        if button == arcade.MOUSE_BUTTON_MIDDLE:
            self.level.add_tank(Tank, x, y)

        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.level.remove(x, y)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if self.brush_on:
            self.level.append(self.current_brush, x, y)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        self.current_brush += 1
        if self.current_brush >= len(self.level.blocks):
            self.current_brush = 0

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        self.brush_on = False


def main():
    MyGame()
    arcade.run()


if __name__ == "__main__":
    main()
