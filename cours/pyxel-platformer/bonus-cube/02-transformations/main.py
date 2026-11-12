import pyxel
from pyxel.cube import Camera, Mat4, Node, Shading, Vec3


SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
BACKGROUND_COLOR = pyxel.COLOR_BLACK

GROUND_SIZE = 200.0
GROUND_COLOR = pyxel.COLOR_GREEN

CUBE_SIZE = 12.0
CUBE_COLORS = [
    pyxel.COLOR_RED,
    pyxel.COLOR_ORANGE,
    pyxel.COLOR_YELLOW,
    pyxel.COLOR_LIME,
]
CUBE_RADIUS = 36.0

MOBILE_HEIGHT = 40.0
MOBILE_SPEED = 1.5

CAMERA_HEIGHT = 60.0
CAMERA_DISTANCE = 160.0
CAMERA_SPEED = 2.0
CAMERA_HEIGHT_MIN = 20.0
CAMERA_HEIGHT_MAX = 150.0


class Ground(Node):
    def on_draw(self):
        self.box(
            Mat4.from_translation(Vec3(0.0, -1.0, 0.0)),
            Vec3(GROUND_SIZE, 2.0, GROUND_SIZE),
            GROUND_COLOR,
        )


class Cube(Node):
    def __init__(self, color):
        super().__init__()
        self.color = color

    def on_draw(self):
        self.box(
            Mat4.IDENTITY,
            Vec3(CUBE_SIZE, CUBE_SIZE, CUBE_SIZE),
            self.color,
        )


class Mobile(Node):
    def __init__(self):
        super().__init__()

        count = len(CUBE_COLORS)

        for index in range(count):
            angle = index * 360.0 / count
            cube = Cube(CUBE_COLORS[index])
            cube.transform = Mat4.from_translation(
                Vec3(
                    pyxel.cos(angle) * CUBE_RADIUS,
                    0.0,
                    pyxel.sin(angle) * CUBE_RADIUS,
                ),
            )
            self.add_child(cube)

    def on_update(self):
        spin = Mat4.from_euler(
            Vec3(0.0, pyxel.frame_count * MOBILE_SPEED, 0.0),
        )
        self.transform = (
            Mat4.from_translation(Vec3(0.0, MOBILE_HEIGHT, 0.0)) * spin
        )


class Scene(Node):
    def __init__(self):
        super().__init__()

        self.shading = Shading(pyxel.colors)

        self.camera = Camera()
        self.camera.clear_color = BACKGROUND_COLOR

        self.yaw = 0.0
        self.height = CAMERA_HEIGHT
        self.update_camera()

        self.add_child(Ground())
        self.add_child(Mobile())

    def update_camera(self):
        eye = Vec3(
            pyxel.sin(self.yaw) * CAMERA_DISTANCE,
            self.height,
            pyxel.cos(self.yaw) * CAMERA_DISTANCE,
        )
        self.camera.transform = Mat4.look_at(
            eye,
            Vec3(0.0, MOBILE_HEIGHT, 0.0),
        )

    def on_update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.yaw -= CAMERA_SPEED
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.yaw += CAMERA_SPEED

        if pyxel.btn(pyxel.KEY_UP):
            self.height += CAMERA_SPEED
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.height -= CAMERA_SPEED

        self.height = pyxel.clamp(
            self.height,
            CAMERA_HEIGHT_MIN,
            CAMERA_HEIGHT_MAX,
        )
        self.update_camera()


class App:
    def __init__(self):
        pyxel.init(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            title="Cube 2 - transformations",
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
