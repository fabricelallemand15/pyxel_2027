"""Génère le fichier de ressources res.pyxres de la formation.

Le format .pyxres est une archive ZIP contenant un unique fichier TOML
nommé pyxel_resource.toml. Ce script construit ce fichier à partir de
petites images décrites en ASCII, puis vérifie le résultat en relisant
l'archive.

Utilisation :

    python cours/pyxel-platformer/outils/generer_ressources.py

Le script écrit res.pyxres à côté de lui-même et dans le dossier de la
leçon 2.
"""

from __future__ import annotations

import shutil
import tomllib
import zipfile
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
COURSE_DIR = TOOLS_DIR.parent
LESSON_DIR = COURSE_DIR / "02-ressources-pyxres"

IMAGE_SIZE = 256
TILE_SIZE = 8
NUM_IMAGES = 3
NUM_TILEMAPS = 8
TILEMAP_SIZE = 256
NUM_SOUNDS = 64
NUM_MUSICS = 8

# Palette Pyxel : 0 noir, 1 bleu nuit, 3 vert, 4 marron, 5 bleu sombre,
# 8 rouge, 9 orange, 10 jaune, 11 vert clair, 15 pêche.
TRANSPARENT = 0
NAVY = 1
GREEN = 3
BROWN = 4
RED = 8
ORANGE = 9
YELLOW = 10
LIME = 11
PEACH = 15

COLORS = {
    ".": TRANSPARENT,
    "n": NAVY,
    "g": GREEN,
    "d": BROWN,
    "r": RED,
    "o": ORANGE,
    "y": YELLOW,
    "l": LIME,
    "p": PEACH,
}

# Chaque tuile fait 8 x 8 pixels. Les coordonnées sont exprimées en tuiles.
PLAYER_IDLE_0 = (
    "..nnnn..",
    ".nrrrrn.",
    ".nppppn.",
    ".nppppn.",
    ".nrrrrn.",
    ".nrrrrn.",
    ".nnnnnn.",
    "..n..n..",
)

PLAYER_IDLE_1 = (
    "..nnnn..",
    ".nrrrrn.",
    ".nppppn.",
    ".nppppn.",
    ".nrrrrn.",
    ".nrrrrn.",
    ".nnnnnn.",
    "..n.nn..",
)

PLAYER_WALK_0 = (
    "..nnnn..",
    ".nrrrrn.",
    ".nppppn.",
    ".nppppn.",
    ".nrrrrn.",
    ".nrrrrn.",
    "..nnnn..",
    ".n....n.",
)

PLAYER_WALK_1 = (
    "..nnnn..",
    ".nrrrrn.",
    ".nppppn.",
    ".nppppn.",
    ".nrrrrn.",
    ".nrrrrn.",
    "..nnnn..",
    "..n..n..",
)

GROUND_TOP = (
    "llllllll",
    "llllllll",
    "dddddddd",
    "dddddddd",
    "ddddnddd",
    "dddddddd",
    "ddnddddd",
    "dddddddd",
)

GROUND_FILL = (
    "dddddddd",
    "ddnddddd",
    "dddddddd",
    "ddddddnd",
    "dddddddd",
    "dndddddd",
    "dddddddd",
    "dddddndd",
)

PLATFORM = (
    "oooooooo",
    "oooooooo",
    "oooooooo",
    "dddddddd",
    "oooooooo",
    "oooooooo",
    "oooooooo",
    "dddddddd",
)

ENEMY = (
    "..oooo..",
    ".orrrro.",
    "orrrrrro",
    "ornrrnro",
    "orrrrrro",
    "orrrrrro",
    ".orrrro.",
    "..oooo..",
)

COIN = (
    "..yyyy..",
    ".yyyyyy.",
    "yyyppyyy",
    "yyyppyyy",
    "yyyyyyyy",
    ".yyyyyy.",
    "..yyyy..",
    "........",
)

BUSH = (
    "........",
    "..llll..",
    ".llllll.",
    "lllgglll",
    "llllllll",
    "lggllggl",
    "........",
    "........",
)

# Nom des tuiles dans la banque 0, en coordonnées de tuiles.
TILES = {
    (0, 0): ("joueur repos 0", PLAYER_IDLE_0),
    (1, 0): ("joueur repos 1", PLAYER_IDLE_1),
    (2, 0): ("joueur marche 0", PLAYER_WALK_0),
    (3, 0): ("joueur marche 1", PLAYER_WALK_1),
    (4, 0): ("ennemi", ENEMY),
    (0, 1): ("sol, dessus", GROUND_TOP),
    (1, 1): ("sol, remplissage", GROUND_FILL),
    (2, 1): ("plateforme", PLATFORM),
    (3, 1): ("pièce", COIN),
    (4, 1): ("buisson", BUSH),
}

# Coordonnées de tuiles utilisées par la tilemap.
TILE_GROUND_TOP = (0, 1)
TILE_GROUND_FILL = (1, 1)
TILE_PLATFORM = (2, 1)
TILE_COIN = (3, 1)
TILE_BUSH = (4, 1)
# Une case vide référence une zone transparente de la banque d'images.
TILE_EMPTY = (5, 5)

# Le niveau fait 64 tuiles de large sur 32 de haut : 512 x 256 pixels,
# soit deux écrans. Seule la première moitié tient dans la fenêtre.
LEVEL_WIDTH_TILES = 64
LEVEL_HEIGHT_TILES = 32
GROUND_ROW = 28

# Plateformes : (ligne, première colonne, dernière colonne).
PLATFORMS = (
    (23, 4, 10),
    (19, 13, 20),
    (15, 23, 29),
    (23, 36, 42),
    (19, 46, 52),
    (15, 56, 62),
)

# Buissons posés sur le sol.
BUSH_COLUMNS = (3, 20, 30, 38, 48, 60)

# Bruitages : notes -1 (silence) à 59 (si4).
SOUNDS = {
    0: {
        "nom": "saut",
        "notes": [31, 36, 40],
        "tones": [2],
        "volumes": [5],
        "effects": [1],
        "speed": 5,
    },
    1: {
        "nom": "pièce",
        "notes": [52, 59],
        "tones": [2],
        "volumes": [5],
        "effects": [3],
        "speed": 6,
    },
    2: {
        "nom": "collision",
        "notes": [24, 19, 12],
        "tones": [3],
        "volumes": [6],
        "effects": [3],
        "speed": 10,
    },
    8: {"notes": [48, 52, 55, 52], "tones": [2], "volumes": [4], "effects": [0], "speed": 15},
    9: {"notes": [53, 57, 55, 52], "tones": [2], "volumes": [4], "effects": [0], "speed": 15},
    10: {"notes": [55, 59, 55, 52], "tones": [2], "volumes": [4], "effects": [0], "speed": 15},
    11: {"notes": [53, 52, 48, 52], "tones": [2], "volumes": [4], "effects": [0], "speed": 15},
    12: {"notes": [24, 24, 31, 31], "tones": [0], "volumes": [5], "effects": [0], "speed": 15},
    13: {"notes": [29, 29, 31, 31], "tones": [0], "volumes": [5], "effects": [0], "speed": 15},
}

MUSICS = {
    0: {"nom": "thème du niveau", "seqs": [[8, 9, 10, 11], [12, 13]]},
}

DEFAULT_SOUND_SPEED = 30


def build_image_bank() -> list[list[int]]:
    """Construit une banque d'images de 256 x 256 pixels."""
    pixels = [[TRANSPARENT] * IMAGE_SIZE for _ in range(IMAGE_SIZE)]

    for (tile_x, tile_y), (_, rows) in TILES.items():
        for row_index, row in enumerate(rows):
            if len(row) != TILE_SIZE:
                raise ValueError(f"Largeur incorrecte : {row!r}")
            for column_index, symbol in enumerate(row):
                x = tile_x * TILE_SIZE + column_index
                y = tile_y * TILE_SIZE + row_index
                pixels[y][x] = COLORS[symbol]

    return pixels


def build_tilemap() -> list[list[tuple[int, int]]]:
    """Construit la tilemap complète (256 x 256 tuiles) du niveau."""
    tiles = [[TILE_EMPTY] * TILEMAP_SIZE for _ in range(TILEMAP_SIZE)]

    for x in range(LEVEL_WIDTH_TILES):
        tiles[GROUND_ROW][x] = TILE_GROUND_TOP
        for y in range(GROUND_ROW + 1, LEVEL_HEIGHT_TILES):
            tiles[y][x] = TILE_GROUND_FILL

    for row, first_column, last_column in PLATFORMS:
        for x in range(first_column, last_column + 1):
            tiles[row][x] = TILE_PLATFORM
        for x in range(first_column + 1, last_column, 2):
            tiles[row - 1][x] = TILE_COIN

    for x in BUSH_COLUMNS:
        tiles[GROUND_ROW - 1][x] = TILE_BUSH

    return tiles


def compress_row(values: list[int]) -> list[int]:
    """Applique la compression de fin de ligne du format .pyxres."""
    last = values[-1]
    last_different = None
    for index in range(len(values) - 1, -1, -1):
        if values[index] != last:
            last_different = index
            break
    length = 1 if last_different is None else last_different + 2
    return values[:length]


def compress_grid(rows: list[list[int]]) -> list[list[int]]:
    """Compresse les lignes, puis les lignes identiques de fin de grille."""
    flattened_rows = [tuple(row) for row in rows]
    last = flattened_rows[-1]
    last_different = None
    for index in range(len(flattened_rows) - 1, -1, -1):
        if flattened_rows[index] != last:
            last_different = index
            break
    length = 1 if last_different is None else last_different + 2

    return [compress_row(row) for row in rows[:length]]


def expand_grid(rows: list[list[int]], width: int, height: int) -> list[list[int]]:
    """Reconstruit une grille complète, comme le fait Pyxel au chargement."""
    expanded_rows = []
    for row in rows:
        last = row[-1]
        expanded_rows.append(row + [last] * (width - len(row)))

    return expanded_rows + [expanded_rows[-1][:] for _ in range(height - len(expanded_rows))]


def toml_array(values: list[int]) -> str:
    return "[" + ", ".join(str(value) for value in values) + "]"


def toml_grid(rows: list[list[int]]) -> str:
    lines = ["["]
    for row in rows:
        lines.append(f"  {toml_array(row)},")
    lines.append("]")
    return "\n".join(lines)


def flatten_tilemap(tiles: list[list[tuple[int, int]]]) -> list[list[int]]:
    """Transforme les tuiles en couples d'entiers, comme dans le fichier."""
    return [[value for tile in row for value in tile] for row in tiles]


def build_toml(image_data: list[list[int]], tilemap_rows: list[list[int]]) -> str:
    parts = ["format_version = 1"]

    for bank_index in range(NUM_IMAGES):
        rows = image_data if bank_index == 0 else [[TRANSPARENT] * IMAGE_SIZE]
        parts.append(
            "[[images]]\n"
            f"width = {IMAGE_SIZE}\n"
            f"height = {IMAGE_SIZE}\n"
            f"data = {toml_grid(compress_grid(rows))}"
        )

    for bank_index in range(NUM_TILEMAPS):
        rows = tilemap_rows if bank_index == 0 else [[0] * (LEVEL_WIDTH_TILES * 2)]
        parts.append(
            "[[tilemaps]]\n"
            f"width = {TILEMAP_SIZE}\n"
            f"height = {TILEMAP_SIZE}\n"
            "imgsrc = 0\n"
            f"data = {toml_grid(compress_grid(rows))}"
        )

    for sound_index in range(NUM_SOUNDS):
        sound = SOUNDS.get(sound_index, {})
        parts.append(
            "[[sounds]]\n"
            f"notes = {toml_array(sound.get('notes', []))}\n"
            f"tones = {toml_array(sound.get('tones', []))}\n"
            f"volumes = {toml_array(sound.get('volumes', []))}\n"
            f"effects = {toml_array(sound.get('effects', []))}\n"
            f"speed = {sound.get('speed', DEFAULT_SOUND_SPEED)}"
        )

    for music_index in range(NUM_MUSICS):
        music = MUSICS.get(music_index, {})
        seqs = music.get("seqs", [])
        seqs_text = "[" + ", ".join(toml_array(seq) for seq in seqs) + "]"
        parts.append(f"[[musics]]\nseqs = {seqs_text}")

    return "\n\n".join(parts) + "\n"


def check_resource(
    path: Path,
    image_data: list[list[int]],
    tilemap_data: list[list[tuple[int, int]]],
) -> None:
    """Relit l'archive et vérifie quelques pixels et tuiles."""
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if names != ["pyxel_resource.toml"]:
            raise ValueError(f"Contenu inattendu : {names}")
        content = tomllib.loads(archive.read("pyxel_resource.toml").decode("utf-8"))

    if content["format_version"] != 1:
        raise ValueError("Version de format inattendue")
    if len(content["images"]) != NUM_IMAGES:
        raise ValueError("Nombre de banques d'images inattendu")
    if len(content["tilemaps"]) != NUM_TILEMAPS:
        raise ValueError("Nombre de tilemaps inattendu")
    if len(content["sounds"]) != NUM_SOUNDS:
        raise ValueError("Nombre de sons inattendu")
    if len(content["musics"]) != NUM_MUSICS:
        raise ValueError("Nombre de musiques inattendu")

    image = content["images"][0]
    restored = expand_grid(image["data"], image["width"], image["height"])
    if restored != image_data:
        raise ValueError("La banque d'images restaurée diffère de l'original")

    tilemap = content["tilemaps"][0]
    pairs = expand_grid(tilemap["data"], tilemap["width"] * 2, tilemap["height"])
    restored_tiles = [
        [(row[index], row[index + 1]) for index in range(0, TILEMAP_SIZE * 2, 2)]
        for row in pairs
    ]
    if restored_tiles != tilemap_data:
        raise ValueError("La tilemap restaurée diffère de l'original")

    if content["sounds"][1]["notes"] != SOUNDS[1]["notes"]:
        raise ValueError("Le son de pièce est incorrect")
    if content["musics"][0]["seqs"] != MUSICS[0]["seqs"]:
        raise ValueError("La musique est incorrecte")


def main() -> None:
    image_data = build_image_bank()
    tilemap_data = build_tilemap()
    toml_text = build_toml(image_data, flatten_tilemap(tilemap_data))

    output_path = TOOLS_DIR / "res.pyxres"
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("pyxel_resource.toml", toml_text.encode("utf-8"))

    check_resource(output_path, image_data, tilemap_data)

    LESSON_DIR.mkdir(parents=True, exist_ok=True)
    lesson_path = LESSON_DIR / "res.pyxres"
    shutil.copyfile(output_path, lesson_path)

    print(f"Écrit : {output_path} ({output_path.stat().st_size} octets)")
    print(f"Copié : {lesson_path} ({lesson_path.stat().st_size} octets)")


if __name__ == "__main__":
    main()
