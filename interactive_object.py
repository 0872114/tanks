import arcade
from copy import deepcopy
from config import Config


class InteractiveObject:

    tile_coords = []
    tile_size = Config.BLOCK_SIZE
    adjust = None
    overlay = False
    logical = False
    matrix = [[1]]

    def __init__(self, x, y):
        self.sprite = None
        self.textures = []
        mx, my = Config.m_point(x, y)
        self.x, self.y = Config.abs_point(mx, my, self.tile_size)
        self.m_points = []
        self.destroy = False

    def load_textures(self):
        for x, y in self.tile_coords:
            self.textures.append(arcade.load_texture(
                Config.TILE_MAP, x * self.tile_size, y * self.tile_size,
                self.tile_size, self.tile_size))

    def create_sprite(self):
        self.sprite = arcade.Sprite()
        for texture in self.textures:
            self.sprite.append_texture(texture)

        self.sprite.set_texture(0)
        self.sprite.angle = self.angle
        self.sprite.set_position(self.x, self.y)

        return self.sprite

    def animate(self):
        pass

    def move(self):
        return False

    @property
    def angle(self):
        return 0

