import pyxel
from pyxel.cube import Camera, Mat4, Node, Shading, Vec3


SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
BACKGROUND_COLOR = pyxel.COLOR_BLACK

GROUND_SIZE = 200.0
GROUND_COLOR = pyxel.COLOR_GREEN

CUBE_SIZE = 32.0
CUBE_COLOR = pyxel.COLOR_CYAN
CUBE_HEIGHT = 16.0
CUBE_SPEED = 1.0

CAMERA_HEIGHT = 60.0
CAMERA_DISTANCE = 140.0


class Ground(Node):
    def on_draw(self):
        self.box(
            Mat4.from_translation(Vec3(0.0, -1.0, 0.0)),
            Vec3(GROUND_SIZE, 2.0, GROUND_SIZE),
            GROUND_COLOR,
        )


class Cube(Node):
    def on_update(self):
        spin = Mat4.from_euler(
            Vec3(0.0, pyxel.frame_count * CUBE_SPEED, 0.0),
        )
        self.transform = (
            Mat4.from_translation(Vec3(0.0, CUBE_HEIGHT, 0.0)) * spin
        )

    def on_draw(self):
        self.box(
            Mat4.IDENTITY,
            Vec3(CUBE_SIZE, CUBE_SIZE, CUBE_SIZE),
            CUBE_COLOR,
        )


class Scene(Node):
    def __init__(self):
        super().__init__()

        self.shading = Shading(pyxel.colors)

        self.camera = Camera()
        self.camera.clear_color = BACKGROUND_COLOR
        self.camera.transform = Mat4.look_at(
            Vec3(0.0, CAMERA_HEIGHT, CAMERA_DISTANCE),
            Vec3(0.0, CUBE_HEIGHT, 0.0),
        )

        self.add_child(Ground())
        self.add_child(Cube())


class App:
    def __init__(self):
        pyxel.init(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            title="Cube 1 - scene 3D",
        )

        self.scene = Scene()

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.scene.update()

    def draw(self):
        self.scene.draw(0, 0, pyxel.width, pyxel.height)


App()
