# Bonus Cube 2 — Nœuds, transformations et caméra

## Fiche de production

- **Formation :** Créer un mini-platformer 2D avec Pyxel — module bonus Pyxel Cube
- **Public :** élèves ayant terminé le chapitre Cube 1
- **Environnement :** PyxelStudio dans Capytale
- **Version ciblée :** Pyxel 3.0.1
- **Durée cible :** 11 à 12 minutes
- **Fichiers du projet :** `main.py` seulement, aucune ressource externe
- **Ressource utilisée :** aucune ; l’anneau et le sol sont dessinés par le code
- **Titre à l’écran :** Bonus Cube 2 — Nœuds, transformations et caméra

## Intention pédagogique

Ce chapitre installe la notion la plus utile de la 3D : la hiérarchie. Un objet peut contenir d’autres objets, et sa transformation entraîne les leurs.

Le chapitre s’organise autour de trois idées :

- une transformation est locale, donc relative au parent ;
- tourner un parent entraîne ses enfants, sans code pour eux ;
- une caméra se pilote en recalculant sa position dans le monde.

Le résultat est modeste à l’écran — quatre cubes en anneau — mais il contient la mécanique de tous les objets composés : un bras articulé, une tourelle, un véhicule avec ses roues.

## Objectifs annoncés aux élèves

À la fin de la vidéo, l’élève doit pouvoir :

1. construire un nœud parent avec plusieurs enfants ;
2. expliquer ce qu’est une transformation locale ;
3. placer des objets sur un cercle ;
4. faire tourner un groupe en tournant son parent ;
5. déplacer la caméra au clavier ;
6. borner une valeur avec `pyxel.clamp()`.

## Préparation de l’enregistrement

### Fichiers

- `main.py` du chapitre, dans le dossier `02-transformations` ;
- aucun autre fichier.

### Vérifications avant d’enregistrer

- Un anneau de quatre cubes de couleurs différentes flotte au-dessus du sol.
- L’anneau tourne sur lui-même, sans que les cubes se rapprochent du centre.
- Les flèches gauche et droite font le tour de la scène.
- Les flèches haut et bas changent la hauteur, sans descendre sous 20 ni dépasser 150.
- Le sol reste immobile.
- La touche `Q` ferme la fenêtre.

### Code final

```python
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
```

## Découpage détaillé

### 00:00 — Montrer le résultat

**À l’écran :** lancer le programme, tourner autour de l’anneau avec les flèches, monter et descendre.

**Narration :**

> Voici le chapitre deux du module bonus. Un anneau de quatre cubes tourne au-dessus du sol, et la caméra fait le tour de la scène au clavier.
>
> Ce qui compte n’est pas l’anneau, c’est la façon dont il est construit. Un objet central porte les quatre cubes, et c’est lui qui tourne. Les cubes, eux, ne bougent jamais de leur place.
>
> C’est la mécanique de tous les objets composés : une tourelle avec son canon, un véhicule avec ses roues, un personnage avec ses bras.

### 00:55 — Présenter les objectifs

**À l’écran :** afficher les trois points.

```text
1. un parent, des enfants
2. des transformations qui se composent
3. une caméra au clavier
```

**Narration :**

> Trois étapes.
>
> D’abord l’arbre : un nœud parent, quatre nœuds enfants.
>
> Ensuite les transformations : chacune est locale, et le moteur compose les niveaux.
>
> Enfin la caméra : deux nombres, un angle et une hauteur, et une position recalculée à chaque image.

### 01:40 — Un parent, des enfants

**À l’écran :** afficher la boucle de `Mobile.__init__()`.

```python
cube = Cube(CUBE_COLORS[index])
cube.transform = Mat4.from_translation(Vec3(...))
self.add_child(cube)
```

**Narration :**

> La classe `Mobile` construit ses quatre cubes dans une boucle.
>
> Trois lignes par cube. On crée le cube. On lui donne une position. On l’accroche au mobile avec `add_child()`.
>
> La troisième ligne est celle qu’on oublie. Sans elle, le cube existe, mais personne ne le met à jour ni ne le dessine : il n’est pas dans l’arbre. Une variable locale ne suffit pas.
>
> La couleur vient de la liste `CUBE_COLORS`, et chaque cube la garde dans son attribut `self.color`.

### 02:40 — Une transformation locale

**À l’écran :** afficher le calcul du cercle, puis le cube seul, puis le mobile avec ses enfants.

```python
angle = index * 360.0 / count
Vec3(pyxel.cos(angle) * CUBE_RADIUS, 0.0, pyxel.sin(angle) * CUBE_RADIUS)
```

**Narration :**

> Les positions forment un cercle de rayon 36. Pour quatre cubes, les angles valent zéro, quatre-vingt-dix, cent-quatre-vingts et deux-cent-soixante-dix degrés. Le premier cube se place donc à 36 sur l’axe `x`, le deuxième à 36 sur l’axe `z`, le troisième à moins 36, et le dernier à moins 36 sur `z`.
>
> Attention : `pyxel.cos()` et `pyxel.sin()` travaillent en degrés. Ceux du module `math` travaillent en radians. Confondre les deux écrase l’anneau vers le centre.
>
> Et voici le point important. Aucun de ces cubes ne contient la valeur 40. Leur transformation ne parle que d’un cercle dans le plan du sol, à hauteur zéro.
>
> C’est le mobile qui vaut 40 : `MOBILE_HEIGHT`. La transformation d’un enfant est locale, relative à son parent. Pour connaître la position réelle dans le monde, on lit `world_transform`, qui compose tous les niveaux depuis la racine.

**Action :** mettre `MOBILE_HEIGHT` à zéro, montrer l’anneau posé sur le sol, puis revenir à 40.

### 04:20 — Tourner le parent

**À l’écran :** afficher `Mobile.on_update()`.

```python
spin = Mat4.from_euler(
    Vec3(0.0, pyxel.frame_count * MOBILE_SPEED, 0.0),
)
self.transform = (
    Mat4.from_translation(Vec3(0.0, MOBILE_HEIGHT, 0.0)) * spin
)
```

**Narration :**

> La mise à jour du mobile ressemble à celle du cube du chapitre précédent.
>
> Une rotation autour de l’axe `y`, calculée à partir du numéro d’image, puis une translation vers la hauteur du mobile.
>
> Et c’est tout. Les quatre enfants n’ont aucune ligne de code de mouvement : leur transformation ne change jamais. C’est le parent qui les entraîne, et l’anneau tourne autour de son propre axe.
>
> À un degré et demi par image, et trente images par seconde, l’anneau fait un tour en huit secondes.

**Action :** commenter la ligne de rotation du mobile, et montrer que les cubes tournent alors sur eux-mêmes si on déplace la même rotation dans `Cube`.

**Narration :**

> La preuve par l’expérience : déplacez cette rotation dans la mise à jour de chaque cube, et les cubes tourneront sur eux-mêmes sans former d’anneau. La différence entre les deux versions est toute la leçon.

### 05:50 — Une caméra au clavier

**À l’écran :** afficher `update_camera()`.

```python
eye = Vec3(
    pyxel.sin(self.yaw) * CAMERA_DISTANCE,
    self.height,
    pyxel.cos(self.yaw) * CAMERA_DISTANCE,
)
self.camera.transform = Mat4.look_at(eye, Vec3(0.0, MOBILE_HEIGHT, 0.0))
```

**Narration :**

> La scène garde deux nombres : un angle, `yaw`, et une hauteur, `height`.
>
> La position de l’œil se calcule à partir de ces deux nombres. À angle zéro, l’œil est devant la scène, à 160 unités. En augmentant l’angle, l’œil glisse sur un cercle de rayon 160 autour du mobile : on voit la scène de côté, puis de derrière.
>
> Le point visé ne change jamais : c’est le centre de l’anneau. C’est ce qui donne l’impression de tourner autour de l’objet plutôt que de le traverser.

**Action :** afficher les quatre flèches dans `Scene.on_update()`, puis `pyxel.clamp()`.

```python
self.height = pyxel.clamp(self.height, CAMERA_HEIGHT_MIN, CAMERA_HEIGHT_MAX)
```

**Narration :**

> Les flèches gauche et droite modifient l’angle, les flèches haut et bas la hauteur.
>
> Puis `pyxel.clamp()` ramène la hauteur entre 20 et 150. Sans cette borne, une seconde d’appui suffit à sortir de la scène, et la caméra passe sous le sol.
>
> Tous les calculs de position sont regroupés dans `update_camera()`. Une seule méthode décrit le point de vue, et il n’y a qu’un endroit à corriger quand la formule change.

### 07:30 — Erreurs fréquentes

**À l’écran :** provoquer quatre erreurs, une par une.

```text
add_child() oublié : aucun cube
rotation sur les enfants : pas d’anneau
caméra sur le mobile : mouvements cumulés
clamp() oublié : la caméra sort
```

**Narration :**

> Quatre erreurs.
>
> Un `add_child()` oublié et le cube n’existe pas dans l’arbre : aucune erreur, aucun cube, juste rien.
>
> Une rotation écrite sur les enfants plutôt que sur le parent : les cubes tournent sur eux-mêmes, et l’anneau n’existe pas.
>
> Une caméra placée sur le mobile : elle tourne avec lui, et le mouvement du clavier se cumule à la rotation de l’anneau. Une caméra se pose sur la scène, pas sur l’objet observé.
>
> Et l’oubli de `clamp()` : la caméra descend sous le sol, et la scène disparaît.

### 08:40 — Personnaliser

**À l’écran :** afficher le tableau des réglages, puis ajouter un second anneau plus bas qui tourne en sens inverse.

```text
CUBE_COLORS : nombre de cubes
CUBE_RADIUS, MOBILE_HEIGHT
MOBILE_SPEED, CUBE_SIZE
CAMERA_DISTANCE, CAMERA_SPEED
```

**Narration :**

> Chaque réglage a sa constante.
>
> Ajouter un cinquième cube dans `CUBE_COLORS` suffit : les angles sont recalculés à partir du nombre de couleurs. Le rayon, la hauteur et la vitesse se règlent chacun de leur côté.
>
> L’exercice du chapitre : un second anneau, plus large, plus bas, qui tourne en sens inverse. Une seconde instance de `Mobile`, un rayon différent, un signe moins devant `MOBILE_SPEED`. Vous verrez que chaque sous-arbre vit sa propre vie dans la même scène.

### 09:50 — À retenir

**À l’écran :** afficher les quatre phrases, puis la scène finale en mouvement.

```text
transform est locale
le parent entraîne ses enfants
sin et cos en degrés
la caméra appartient à la scène
```

**Narration :**

> Quatre phrases.
>
> La transformation d’un nœud est locale : elle le place par rapport à son parent.
>
> Un parent entraîne ses enfants : tourner le parent suffit à faire tourner le groupe.
>
> `pyxel.sin()` et `pyxel.cos()` attendent des degrés.
>
> Et la caméra appartient à la scène, jamais à l’objet observé.
>
> Le chapitre suivant transforme cette scène en jeu : un cube piloté aux flèches, six gemmes à ramasser, un score, et une caméra qui suit le joueur.

## Consignes de montage

- Montrer l’anneau en mouvement avant toute explication de code.
- Afficher les positions calculées pour les quatre angles, en incrustation, quand on explique le cercle.
- Montrer une fois l’expérience ratée : la rotation placée sur les enfants.
- Faire varier la hauteur de la caméra en direct, jusqu’aux bornes, pour montrer `clamp()`.
- Faire l’exercice du second anneau en direct.
- Conserver le même code final que l’article `article.qmd`.

## Vérification avant publication

- Le code compile et s’exécute avec Pyxel 3.0.1.
- Quatre cubes de couleurs différentes forment un anneau qui tourne.
- Les flèches font tourner la caméra et changer sa hauteur, dans les bornes annoncées.
- Le sol reste immobile.
- La touche `Q` ferme la fenêtre.
- Aucun texte affiché ne contient d’accent.
- Le code affiché est identique à celui de l’article.
