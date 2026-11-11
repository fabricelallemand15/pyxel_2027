import pyxel


SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
RESOURCE_FILE = "res.pyxres"

TILE_SIZE = 8
LEVEL_WIDTH = 32
LEVEL_HEIGHT = 32
GROUND_Y = 224
SOLID_TILES = (
    (0, 1),
    (1, 1),
    (2, 1),
)

PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLAYER_SPEED = 2
GRAVITY = 1
JUMP_SPEED = -11
PLAYER_TILE_X = 0
PLAYER_TILE_Y = 0
PLAYER_START_X = 40
PLAYER_START_Y = GROUND_Y - PLAYER_HEIGHT

BACKGROUND_COLOR = pyxel.COLOR_DARK_BLUE
TEXT_COLOR = pyxel.COLOR_WHITE
TRANSPARENT_COLOR = 0

MUSIC = 0
JUMP_SOUND = 0


class Level:
    def __init__(self):
        self.tilemap = pyxel.tilemaps[0]
        self.width = LEVEL_WIDTH * TILE_SIZE
        self.height = LEVEL_HEIGHT * TILE_SIZE

    def draw(self):
        pyxel.bltm(
            0,
            0,
            self.tilemap,
            0,
            0,
            self.width,
            self.height,
        )

    def is_solid(self, tile_x, tile_y):
        tile = self.tilemap.pget(tile_x, tile_y)
        return tile in SOLID_TILES


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.dx = 0
        self.dy = 0
        self.is_on_ground = True

    def update(self):
        self.dx = 0

        if pyxel.btn(pyxel.KEY_LEFT):
            self.dx = -PLAYER_SPEED
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.dx = PLAYER_SPEED

        self.x += self.dx
        self.x = pyxel.clamp(
            self.x,
            0,
            pyxel.width - self.width,
        )

        if pyxel.btnp(pyxel.KEY_SPACE) and self.is_on_ground:
            self.dy = JUMP_SPEED
            pyxel.play(0, JUMP_SOUND)

        self.dy += GRAVITY
        self.y += self.dy

        if self.y + self.height >= GROUND_Y:
            self.y = GROUND_Y - self.height
            self.dy = 0
            self.is_on_ground = True
        else:
            self.is_on_ground = False

    def draw(self):
        pyxel.blt(
            self.x,
            self.y,
            0,
            PLAYER_TILE_X * TILE_SIZE,
            PLAYER_TILE_Y * TILE_SIZE,
            self.width,
            self.height,
            TRANSPARENT_COLOR,
        )


class Game:
    def __init__(self):
        pyxel.init(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            title="Leçon 5 - niveau",
        )
        pyxel.load(RESOURCE_FILE)

        self.level = Level()
        self.player = Player(
            PLAYER_START_X,
            PLAYER_START_Y,
        )

        pyxel.playm(MUSIC, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.player.update()

    def draw(self):
        pyxel.cls(BACKGROUND_COLOR)
        self.level.draw()

        tile_x = self.player.x // TILE_SIZE
        tile_y = (self.player.y + self.player.height) // TILE_SIZE

        if self.level.is_solid(tile_x, tile_y):
            state = "solide"
        else:
            state = "vide"

        pyxel.text(
            4,
            4,
            "Leçon 5 - niveau",
            TEXT_COLOR,
        )
        pyxel.text(
            4,
            12,
            "Flèches : déplacer, Espace : sauter",
            TEXT_COLOR,
        )
        pyxel.text(
            4,
            20,
            f"Case {tile_x},{tile_y} : {state}",
            TEXT_COLOR,
        )

        self.player.draw()


Game()
