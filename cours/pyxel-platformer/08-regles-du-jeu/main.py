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
COIN_TILE = (3, 1)
ENEMY_TILE = (4, 0)
EMPTY_TILE = (5, 5)

PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLAYER_SPEED = 2
GRAVITY = 1
JUMP_SPEED = -11
PLAYER_TILE_X = 0
PLAYER_TILE_Y = 0
PLAYER_START_X = 8
PLAYER_START_Y = GROUND_Y - PLAYER_HEIGHT

ENEMY_SPEED = 1

BACKGROUND_COLOR = pyxel.COLOR_DARK_BLUE
TEXT_COLOR = pyxel.COLOR_WHITE
TRANSPARENT_COLOR = 0

MUSIC = 0
JUMP_SOUND = 0
COIN_SOUND = 1
HIT_SOUND = 2


class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.is_alive = True

    def update(self):
        pass

    def draw(self):
        tile_x, tile_y = COIN_TILE
        pyxel.blt(
            self.x,
            self.y,
            0,
            tile_x * TILE_SIZE,
            tile_y * TILE_SIZE,
            self.width,
            self.height,
            TRANSPARENT_COLOR,
        )


class Enemy:
    def __init__(self, x, y, min_x, max_x):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.dx = ENEMY_SPEED
        self.min_x = min_x
        self.max_x = max_x

    def update(self):
        self.x += self.dx

        if self.x < self.min_x:
            self.x = self.min_x
            self.dx = ENEMY_SPEED
        elif self.x > self.max_x:
            self.x = self.max_x
            self.dx = -ENEMY_SPEED

    def draw(self):
        tile_x, tile_y = ENEMY_TILE
        pyxel.blt(
            self.x,
            self.y,
            0,
            tile_x * TILE_SIZE,
            tile_y * TILE_SIZE,
            self.width,
            self.height,
            TRANSPARENT_COLOR,
        )


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

    def take_coins(self):
        positions = []

        for tile_y in range(LEVEL_HEIGHT):
            for tile_x in range(LEVEL_WIDTH):
                if self.tilemap.pget(tile_x, tile_y) == COIN_TILE:
                    self.tilemap.pset(tile_x, tile_y, EMPTY_TILE)
                    positions.append(
                        (tile_x * TILE_SIZE, tile_y * TILE_SIZE),
                    )

        return positions


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
            title="Chapitre 8 - but du jeu",
        )
        pyxel.load(RESOURCE_FILE)

        self.level = Level()
        self.player = Player(
            PLAYER_START_X,
            PLAYER_START_Y,
            self.level,
        )

        self.coins = []
        for x, y in self.level.take_coins():
            self.coins.append(Coin(x, y))

        self.enemies = [
            Enemy(88, 216, 88, 160),
            Enemy(104, 144, 104, 160),
        ]

        self.score = 0
        self.is_game_over = False

        pyxel.playm(MUSIC, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.is_game_over:
            return

        self.player.update()

        for coin in self.coins:
            coin.update()

        for enemy in self.enemies:
            enemy.update()

        self.check_coins()
        self.check_enemies()

    def draw(self):
        pyxel.cls(BACKGROUND_COLOR)
        self.level.draw()

        for coin in self.coins:
            coin.draw()

        for enemy in self.enemies:
            enemy.draw()

        self.player.draw()

        pyxel.text(
            4,
            4,
            "Chapitre 8 - but du jeu",
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
            f"Score : {self.score}  Restantes : {len(self.coins)}",
            TEXT_COLOR,
        )

        if self.is_game_over:
            pyxel.rect(48, 96, 160, 32, pyxel.COLOR_BLACK)
            pyxel.text(102, 100, "Partie perdue", pyxel.COLOR_RED)
            pyxel.text(110, 112, f"Score : {self.score}", TEXT_COLOR)

    def collide(self, a, b):
        return (
            a.x < b.x + b.width
            and a.x + a.width > b.x
            and a.y < b.y + b.height
            and a.y + a.height > b.y
        )

    def check_coins(self):
        for coin in self.coins:
            if self.collide(self.player, coin):
                coin.is_alive = False
                self.score += 1
                pyxel.play(1, COIN_SOUND)

        self.coins = [coin for coin in self.coins if coin.is_alive]

    def check_enemies(self):
        for enemy in self.enemies:
            if self.collide(self.player, enemy):
                self.is_game_over = True
                pyxel.play(2, HIT_SOUND)


Game()
