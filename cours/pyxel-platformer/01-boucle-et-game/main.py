import pyxel


SCREEN_WIDTH = 128
SCREEN_HEIGHT = 128
GROUND_Y = 96

PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLAYER_SPEED = 1

BACKGROUND_COLOR = pyxel.COLOR_DARK_BLUE
GROUND_COLOR = pyxel.COLOR_GREEN
PLAYER_COLOR = pyxel.COLOR_YELLOW
TEXT_COLOR = pyxel.COLOR_WHITE


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
        pyxel.rect(
            self.x,
            self.y,
            self.width,
            self.height,
            PLAYER_COLOR,
        )


class Game:
    def __init__(self):
        pyxel.init(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            title="Leçon 1 - Boucle de jeu",
        )

        self.player = Player(
            20,
            GROUND_Y - PLAYER_HEIGHT,
        )

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.player.update()

    def draw(self):
        pyxel.cls(BACKGROUND_COLOR)
        pyxel.rect(
            0,
            GROUND_Y,
            pyxel.width,
            pyxel.height - GROUND_Y,
            GROUND_COLOR,
        )
        pyxel.text(
            4,
            4,
            "Leçon 1 - boucle de jeu",
            TEXT_COLOR,
        )
        pyxel.text(
            4,
            12,
            f"Image {pyxel.frame_count}",
            TEXT_COLOR,
        )

        self.player.draw()


Game()
