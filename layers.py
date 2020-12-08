import arcade
from config import Config
from matrix import Matrix


class Layer(arcade.SpriteList):

    def __init__(self, id=None, matrix=None, *args, **kwargs):
        # foreground and background
        self.matrix = matrix
        self._items = list()
        super().__init__(*args, **kwargs)
        self.sprite_list = arcade.SpriteList()

        # schedule update

    def append(self, item):
        if self.matrix is not None:
            m_points = self.matrix.append(item)
            if not m_points:
                return False
            item.m_points = m_points

        self._items.append(item)
        item.load_textures()
        item.create_sprite()
        super(Layer, self).append(item.sprite)
        assert item.sprite in self.sprite_list
        return True

    def __iter__(self):
        for item in self._items:
            yield item

    def get(self, x, y):
        return self.matrix.get(x, y)

    def remove(self, item):
        del self._items[self._items.index(item)]

        assert item.sprite in self.sprite_list
        super(Layer, self).remove(item.sprite)

        item.sprite.kill()
        for mx, my in item.m_points:
            self.matrix.remove(mx, my)


class Frame(arcade.ShapeElementList):

    def __init__(self):
        super().__init__()
        self.sprite_list = arcade.SpriteList()
        self._items = []
        self.matrix = Matrix(Config.X_SIZE, Config.Y_SIZE)
        self.enabled = False
        bg_rect = arcade.create_rectangle_outline(Config.CENTER_X + Config.BLOCK_SIZE // 2,
                                                  Config.CENTER_Y + Config.BLOCK_SIZE // 2,
                                                  Config.BLOCK_SIZE * Config.X_SIZE,
                                                  Config.BLOCK_SIZE * Config.Y_SIZE,
                                                  (120, 120, 120), 2)

        center = arcade.create_rectangle_outline(Config.CENTER_X + Config.BLOCK_SIZE // 2,
                                                 Config.CENTER_Y + Config.BLOCK_SIZE // 2,
                                                 Config.BLOCK_SIZE * 2,
                                                 Config.BLOCK_SIZE * 2,
                                                 (120, 120, 120), 2)

        self.append(bg_rect)

        for i in range(Config.X_SIZE // 2 + 5):
            vline = arcade.create_line(Config.LEFT + i * 2 * Config.BLOCK_SIZE,
                                       Config.BOTTOM,
                                       Config.LEFT + i * 2 * Config.BLOCK_SIZE,
                                       Config.BOTTOM + Config.Y_SIZE * Config.BLOCK_SIZE,
                                       (30, 80, 30), 2)
            self.append(vline)
            xline = arcade.create_line(Config.LEFT,
                                       Config.BOTTOM + i * 2 * Config.BLOCK_SIZE,
                                       Config.LEFT + Config.X_SIZE * Config.BLOCK_SIZE,
                                       Config.BOTTOM + i * 2 * Config.BLOCK_SIZE,
                                       (30, 80, 30), 2)
            self.append(xline)

    def add_item(self, item):
        m_points = self.matrix.append(item)
        if not m_points:
            return False
        item.m_points = m_points

        self._items.append(item)
        item.load_textures()
        item.create_sprite()
        self.sprite_list.append(item.sprite)
        assert item.sprite in self.sprite_list
        return True

    def remove_item(self, x, y):
        item = self.matrix.get(x, y)
        if item:
            self.sprite_list.remove(item.sprite)
            item.sprite.kill()
            for mx, my in item.m_points:
                self.matrix.remove(mx, my)
            return item
