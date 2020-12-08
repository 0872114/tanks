from interactive_object import InteractiveObject
from config import Config
import arcade


class Explosion:
    tile_coords = [(16, 8), (17, 8), (18, 8)]
    tile_size = 32
    adjust = 16

    tile_coords_big = [(9.5, 4), (10.5, 4)]
    tile_size_big = 64

    overlay = True
    matrix = [[1, 0],
              [0, 0]]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.textures = []

        for x, y in self.tile_coords:
            self.textures.append(arcade.load_texture(
                Config.TILE_MAP, x * self.tile_size, y * self.tile_size,
                self.tile_size, self.tile_size))
        for x, y in self.tile_coords_big:
            self.textures.append(arcade.load_texture(
                Config.TILE_MAP, x * self.tile_size_big, y * self.tile_size_big,
                self.tile_size_big, self.tile_size_big))
        self.current_texture = 0
        self.increment = 1
        self.destroy = False

    def animate(self):
        if self.current_texture == len(self.textures) - 1:
            self.increment = -1

        self.current_texture += self.increment

        if self.current_texture == 0:
            self.increment = 0
            self.destroy = True

        if self.current_texture > 2:
            self.tile_size = self.tile_size_big
        else:
            self.tile_size = self.tile_size

    @property
    def texture(self):
        return self.textures[self.current_texture]
