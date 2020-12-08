class Config:

    TILE_MAP = 'sprites/sprites.png'
    SCREEN_TITLE = "Tank"
    BLOCK_SIZE = 16
    X_SIZE = 26
    Y_SIZE = 26

    SCREEN_HEIGHT = Y_SIZE * BLOCK_SIZE + BLOCK_SIZE * 2
    SCREEN_WIDTH = X_SIZE * BLOCK_SIZE + BLOCK_SIZE * 8

    BOTTOM = BLOCK_SIZE
    LEFT = BLOCK_SIZE * 4

    CENTER_X = LEFT + (X_SIZE * BLOCK_SIZE) // 2 - BLOCK_SIZE // 2
    CENTER_Y = BOTTOM + (Y_SIZE * BLOCK_SIZE) // 2 - BLOCK_SIZE // 2

    ENEMIES = 30  # врагов на уровень
    ENEMIES_RESPAWN = 4  # Частота респавна врагов, сек.

    DELETE_KILLED_TANKS = True  # оставлять горы трупов (не удалять дохлые танки)
    MOVE_KILLED_TANKS = False  # таскать трупы для баррикад
    PATH_THROUGH_KILLED = True  # снаряд не пролетает трупы
    FRIENDLY_FIRE = False  # мочить ребят из своей команды

    MSG_GAME_OVER = 'Это пиздец.'
    MSG_PLAYERS_KILLED = 'герои пали,\nно война \nпродолжается...'  # когда все игроки убиты, но орел жив
    MSG_WIN = 'ПОБЕДА!'

    # todo: add levels
    LEVELS = [
        '1.bin', '2.bin'
    ]

    @classmethod
    def m_point(cls, x, y):
        mx = (x - cls.LEFT - 1) // cls.BLOCK_SIZE
        my = (y - cls.BOTTOM - 1) // cls.BLOCK_SIZE
        # print(x - Config.LEFT, y - Config.BOTTOM, '=>', mx, my)
        return mx, my

    @classmethod
    def abs_point(cls, mx, my, tile_size):
        abs_x = (cls.LEFT + mx * cls.BLOCK_SIZE) + tile_size // 2
        abs_y = (cls.BOTTOM + my * cls.BLOCK_SIZE) + tile_size // 2
        # print(mx, my, '=>', abs_x - Config.LEFT, abs_y - Config.BOTTOM)
        return abs_x, abs_y
