from interactive_object import InteractiveObject


class Brick(InteractiveObject):
    tile_coords = [(32 + i, 8) for i in range(5)]


class Armor(InteractiveObject):
    tile_coords = [(32, 3)]


class Water(InteractiveObject):
    tile_coords = [(33, 5), (33, 7), (34, 7)]

    def animate(self):
        self.current_texture += 1
        if self.current_texture >= len(self.textures):
            self.current_texture = 0


class Forest(InteractiveObject):
    tile_coords = [(34, 5)]
    overlay = True


class Ice(InteractiveObject):
    tile_coords = [(36, 5)]


class Flag(InteractiveObject):
    tile_coords = [(19, 2), (20, 2)]  # next if one-flag game
    tile_size = 32
    matrix = [[1, 0],
              [0, 0]]


class CapturedFlag(InteractiveObject):
    tile_coords = [(20, 2)]  # for many-flag game
    tile_size = 32
    matrix = [[1, 0],
              [0, 0]]


class PlayerRespawn(InteractiveObject):
    tile_coords = [(0, 0)]
    tile_size = 32
    logical = True
    matrix = [[1, 0],
              [0, 0]]


class EnemyRespawn(InteractiveObject):
    tile_coords = [(8, 0)]
    tile_size = 32
    logical = True
    matrix = [[1, 0],
              [0, 0]]

    @property
    def angle(self):
        return 180
