import pyxel
from pyxel.cube import Camera, Mat4, Node, Shading, Vec3


SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
FONT_WIDTH = 4
BACKGROUND_COLOR = pyxel.COLOR_BLACK

GROUND_SIZE = 200.0
GROUND_COLOR = pyxel.COLOR_GREEN
ARENA_SIZE = 80.0

PLAYER_SIZE = 16.0
PLAYER_COLOR = pyxel.COLOR_CYAN
PLAYER_SPEED = 2.0
PLAYER_START = Vec3(0.0, PLAYER_SIZE / 2, 0.0)

GEM_SIZE = 10.0
GEM_COLOR = pyxel.COLOR_YELLOW
GEM_HEIGHT = 12.0
GEM_RADIUS = 14.0
GEM_POSITIONS = [
    Vec3(-56.0, GEM_HEIGHT, 0.0),
    Vec3(-28.0, GEM_HEIGHT, -48.0),
    Vec3(28.0, GEM_HEIGHT, -48.0),
    Vec3(56.0, GEM_HEIGHT, 0.0),
    Vec3(28.0, GEM_HEIGHT, 48.0),
    Vec3(-28.0, GEM_HEIGHT, 48.0),
]

CAMERA_HEIGHT = 70.0
CAMERA_DISTANCE = 90.0

TEXT_COLOR = pyxel.COLOR_WHITE


class Ground(Node):
    def on_draw(self):
        self.box(
            Mat4.from_translation(Vec3(0.0, -1.0, 0.0)),
            Vec3(GROUND_SIZE, 2.0, GROUND_SIZE),
            GROUND_COLOR,
        )


class Player(Node):
    def __init__(self):
        super().__init__()
        self.position = PLAYER_START
        self.transform = Mat4.from_translation(PLAYER_START)

    def on_update(self):
        dx = 0
        if pyxel.btn(pyxel.KEY_LEFT):
            dx = -PLAYER_SPEED
        elif pyxel.btn(pyxel.KEY_RIGHT):
            dx = PLAYER_SPEED

        dz = 0
        if pyxel.btn(pyxel.KEY_UP):
            dz = -PLAYER_SPEED
        elif pyxel.btn(pyxel.KEY_DOWN):
            dz = PLAYER_SPEED

        self.position = Vec3(
            pyxel.clamp(
                self.position.x + dx,
                -ARENA_SIZE,
                ARENA_SIZE,
            ),
            self.position.y,
            pyxel.clamp(
                self.position.z + dz,
                -ARENA_SIZE,
                ARENA_SIZE,
            ),
        )
        self.transform = Mat4.from_translation(self.position)

    def on_draw(self):
        self.box(
            Mat4.IDENTITY,
            Vec3(PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE),
            PLAYER_COLOR,
        )


class Gem(Node):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.is_taken = False

    def on_update(self):
        spin = Mat4.from_euler(
            Vec3(0.0, pyxel.frame_count * 2.0, 0.0),
        )
        self.transform = Mat4.from_translation(self.position) * spin

    def on_draw(self):
        if not self.is_taken:
            self.box(
                Mat4.IDENTITY,
                Vec3(GEM_SIZE, GEM_SIZE, GEM_SIZE),
                GEM_COLOR,
            )


class Scene(Node):
    def __init__(self):
        super().__init__()

        self.shading = Shading(pyxel.colors)

        self.camera = Camera()
        self.camera.clear_color = BACKGROUND_COLOR

        self.add_child(Ground())

        self.player = Player()
        self.add_child(self.player)

        self.gems = []
        self.start_game()

    def start_game(self):
        for gem in self.gems:
            self.remove_child(gem)

        self.gems = []

        for position in GEM_POSITIONS:
            gem = Gem(position)
            self.add_child(gem)
            self.gems.append(gem)

        self.player.position = PLAYER_START
        self.player.transform = Mat4.from_translation(PLAYER_START)
        self.player.active = True

        self.score = 0
        self.is_won = False

    def update_camera(self):
        target = self.player.position
        eye = Vec3(
            target.x,
            target.y + CAMERA_HEIGHT,
            target.z + CAMERA_DISTANCE,
        )
        self.camera.transform = Mat4.look_at(eye, target)

    def on_update(self):
        if self.is_won:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.start_game()
            return

        for gem in self.gems:
            if gem.is_taken:
                continue

            distance = self.player.position.distance_to(gem.position)

            if distance < GEM_RADIUS:
                gem.is_taken = True
                self.score += 1

        if self.score == len(self.gems):
            self.is_won = True
            self.player.active = False


class App:
    def __init__(self):
        pyxel.init(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            title="Cube 3 - petit jeu 3D",
        )

        self.scene = Scene()

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.scene.update()

    def draw(self):
        self.scene.update_camera()
        self.scene.draw(0, 0, pyxel.width, pyxel.height)

        score = f"Score : {self.scene.score}"
        pyxel.text(4, 4, score, TEXT_COLOR)

        if self.scene.is_won:
            pyxel.rect(48, 96, 160, 48, pyxel.COLOR_BLACK)
            pyxel.text(self.text_x("Victoire"), 104, "Victoire", TEXT_COLOR)
            pyxel.text(self.text_x(score), 116, score, TEXT_COLOR)
            hint = "Espace : rejouer"
            pyxel.text(self.text_x(hint), 128, hint, TEXT_COLOR)

    def text_x(self, text):
        return (SCREEN_WIDTH - FONT_WIDTH * len(text)) // 2


App()
