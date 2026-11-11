import pyxel


SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
RESOURCE_FILE = "res.pyxres"

TILE_SIZE = 8
LEVEL_WIDTH = 32
LEVEL_HEIGHT = 32
GROUND_Y = 224
SOLID_TILES = [
    (0, 1),
    (1, 1),
    (2, 1),
]

PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLAYER_SPEED = 2
GRAVITY = 1
JUMP_SPEED = -11
PLAYER_TILE_X = 0
PLAYER_TILE_Y = 0
PLAYER_START_X = 8
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

    def move_player(self, x, y, dx, dy):
        return self.tilemap.collide(
            x,
            y,
            PLAYER_WIDTH,
            PLAYER_HEIGHT,
            dx,
            dy,
            SOLID_TILES,
        )


class Player:
    def __init__(self, x, y, level):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.dx = 0
        self.dy = 0
        self.is_on_ground = True
        self.level = level

    def update(self):
        self.dx = 0

        if pyxel.btn(pyxel.KEY_LEFT):
            self.dx = -PLAYER_SPEED
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.dx = PLAYER_SPEED

        if pyxel.btnp(pyxel.KEY_SPACE) and self.is_on_ground:
            self.dy = JUMP_SPEED
            pyxel.play(0, JUMP_SOUND)

        self.dy += GRAVITY

        was_falling = self.dy > 0
        self.dx, self.dy = self.level.move_player(
            self.x,
            self.y,
            self.dx,
            self.dy,
        )

        self.x += self.dx
        self.x = pyxel.clamp(
            self.x,
            0,
            pyxel.width - self.width,
        )
        self.y += self.dy

        self.is_on_ground = was_falling and self.dy == 0

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
            title="Chapitre 6 - collisions",
        )
        pyxel.load(RESOURCE_FILE)

        self.level = Level()
        self.player = Player(
            PLAYER_START_X,
            PLAYER_START_Y,
            self.level,
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

        if self.player.is_on_ground:
            state = "oui"
        else:
            state = "non"

        pyxel.text(
            4,
            4,
            "Chapitre 6 - collisions",
            TEXT_COLOR,
        )
        pyxel.text(
            4,
            12,
            "Gauche et droite : marcher, Espace : sauter",
            TEXT_COLOR,
        )
        pyxel.text(
            4,
            20,
            f"Au sol : {state}",
            TEXT_COLOR,
        )

        self.player.draw()


Game()
