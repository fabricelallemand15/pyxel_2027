import pyxel


SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
RESOURCE_FILE = "res.pyxres"

TILE_SIZE = 8
LEVEL_WIDTH = 32
LEVEL_HEIGHT = 32

PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLAYER_SPEED = 1
PLAYER_TILE_X = 0
PLAYER_TILE_Y = 0
PLAYER_START_X = 40
PLAYER_START_Y = 216

BACKGROUND_COLOR = pyxel.COLOR_DARK_BLUE
TEXT_COLOR = pyxel.COLOR_WHITE
TRANSPARENT_COLOR = 0

BOUNCE_SOUND = 1
MUSIC = 0


class Level:
    def __init__(self):
        self.width = LEVEL_WIDTH * TILE_SIZE
        self.height = LEVEL_HEIGHT * TILE_SIZE

    def draw(self):
        pyxel.bltm(
            0,
            0,
            0,
            0,
            0,
            self.width,
            self.height,
        )


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.dx = PLAYER_SPEED

    def update(self):
        self.x += self.dx

        if self.x <= 0:
            self.x = 0
            self.dx = abs(self.dx)
        elif self.x + self.width >= pyxel.width:
            self.x = pyxel.width - self.width
            self.dx = -abs(self.dx)

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
            title="Leçon 2 - ressources",
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

        direction = self.player.dx
        self.player.update()

        if self.player.dx != direction:
            pyxel.play(0, BOUNCE_SOUND)

    def draw(self):
        pyxel.cls(BACKGROUND_COLOR)
        self.level.draw()

        pyxel.text(
            4,
            4,
            "Leçon 2 - ressources",
            TEXT_COLOR,
        )
        pyxel.text(
            4,
            12,
            "Images, tilemap et audio",
            TEXT_COLOR,
        )

        self.player.draw()


Game()
