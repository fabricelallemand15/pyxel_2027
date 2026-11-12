# Bonus Cube 3 — Un petit jeu 3D

## Fiche de production

- **Formation :** Créer un mini-platformer 2D avec Pyxel — module bonus Pyxel Cube
- **Public :** élèves ayant terminé les chapitres Cube 1 et Cube 2
- **Environnement :** PyxelStudio dans Capytale
- **Version ciblée :** Pyxel 3.0.1
- **Durée cible :** 14 à 15 minutes
- **Fichiers du projet :** `main.py` seulement, aucune ressource externe
- **Ressource utilisée :** aucune ; le sol, le joueur et les gemmes sont dessinés par le code
- **Titre à l’écran :** Bonus Cube 3 — Un petit jeu 3D

## Intention pédagogique

Ce dernier chapitre referme la boucle ouverte par le parcours 2D : un jeu complet, avec des règles, un score, une fin et un redémarrage.

La 3D n’ajoute ici qu’une chose : les positions sont des vecteurs à trois coordonnées. Tout le reste est du niveau du chapitre 8 — un état, des tests, un écran de fin — et du chapitre 11 — un HUD propre, des textes centrés, une partie rejouable.

Le chapitre se termine par un aperçu des outils non utilisés : `Collider` pour la physique, `Mesh.from_glb()` pour les modèles exportés de Blockbench. Ils sont présentés, pas pratiqués : ils demandent des fichiers externes, et le chapitre insiste sur l’autonomie d’un seul fichier.

## Objectifs annoncés aux élèves

À la fin de la vidéo, l’élève doit pouvoir :

1. déplacer un objet sur le sol avec les quatre flèches ;
2. borner un déplacement dans une arène ;
3. mesurer une distance en trois dimensions ;
4. gérer un ramassage et un score ;
5. désactiver un nœud à la victoire ;
6. faire suivre le joueur par la caméra ;
7. afficher un HUD 2D sur une scène 3D.

## Préparation de l’enregistrement

### Fichiers

- `main.py` du chapitre, dans le dossier `03-petit-jeu-3d` ;
- aucun autre fichier.

### Vérifications avant d’enregistrer

- La fenêtre s’intitule « Cube 3 - petit jeu 3D ».
- Six gemmes jaunes tournent autour du joueur.
- Les flèches déplacent le joueur, qui s’arrête à 80 unités du centre.
- La caméra garde le joueur au centre de l’image.
- Une gemme touchée disparaît et le score augmente.
- La sixième gemme déclenche le message de victoire.
- La barre d’espace relance une partie complète.
- La touche `Q` ferme la fenêtre, en jeu comme à la victoire.

### Code final

```python
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
```

## Découpage détaillé

### 00:00 — Montrer le résultat

**À l’écran :** jouer une partie entière, gagner, puis relancer avec la barre d’espace.

**Narration :**

> Voici le dernier chapitre du module bonus, et c’est un jeu.
>
> Un cube coloré se déplace aux flèches, six gemmes tournent autour de lui, un score monte à chaque ramassage, et la sixième gemme affiche la victoire. La barre d’espace relance une partie.
>
> Le jeu se joue au sol, en perspective : c’est un jeu vu de dessus, dessiné en trois dimensions. Pas de saut, pas de gravité, pas de chute.

### 00:50 — Présenter les objectifs

**À l’écran :** afficher les trois points.

```text
1. un joueur qui se déplace
2. des gemmes à ramasser
3. une caméra qui suit
```

**Narration :**

> Trois étapes.
>
> Le joueur : une position en trois coordonnées, quatre flèches, et deux bornes.
>
> Les gemmes : six objets, une distance à mesurer, un score.
>
> La caméra : elle suit le joueur, et le HUD se dessine par-dessus la scène.

### 01:40 — Une position, une transformation

**À l’écran :** afficher le constructeur de `Player`, puis `on_update()`.

```python
self.position = PLAYER_START
self.transform = Mat4.from_translation(PLAYER_START)
```

**Narration :**

> Le joueur garde deux choses : sa position, un vecteur à trois coordonnées, et sa transformation, la matrice qui la traduit pour la scène.
>
> Ce doublon est volontaire. Le vecteur s’additionne, se compare et se borne facilement. La matrice, elle, est ce que la scène comprend. On garde le vecteur comme source de vérité, et la matrice comme conséquence, recalculée à chaque image.
>
> La hauteur ne change jamais : le joueur reste à la moitié de sa taille, donc posé sur le sol.

### 02:40 — Se déplacer et rester dans l’arène

**À l’écran :** afficher la lecture des touches, puis le calcul de la position.

```python
dx = 0
if pyxel.btn(pyxel.KEY_LEFT):
    dx = -PLAYER_SPEED
elif pyxel.btn(pyxel.KEY_RIGHT):
    dx = PLAYER_SPEED
```

**Narration :**

> Les flèches gauche et droite remplissent un déplacement horizontal, les flèches haut et bas un déplacement en profondeur.
>
> `pyxel.btn()` teste si une touche est enfoncée : le déplacement est continu tant qu’on appuie. `pyxel.btnp()` aurait détecté un seul appui, ce qui ne convient pas pour marcher.
>
> La position est ensuite bornée par `pyxel.clamp()`, entre moins 80 et 80 sur les deux axes. L’arène fait donc 160 unités de côté, alors que le sol en mesure 200 : le joueur s’arrête avant le bord, sur une surface toujours visible.

**Action :** pousser le joueur contre le bord, montrer l’arrêt net, puis revenir au centre.

**Narration :**

> Une précision : deux flèches enfoncées ensemble donnent une diagonale un peu plus rapide qu’un déplacement droit. Pour un jeu de ramassage, c’est acceptable. Si cela gêne, il faut normaliser le vecteur de déplacement.

### 04:20 — Des gemmes qui tournent

**À l’écran :** afficher la classe `Gem`.

```python
def on_update(self):
    spin = Mat4.from_euler(Vec3(0.0, pyxel.frame_count * 2.0, 0.0))
    self.transform = Mat4.from_translation(self.position) * spin

def on_draw(self):
    if not self.is_taken:
        self.box(Mat4.IDENTITY, Vec3(GEM_SIZE, GEM_SIZE, GEM_SIZE), GEM_COLOR)
```

**Narration :**

> Une gemme est un petit cube jaune de dix unités, qui tourne sur lui-même deux degrés par image.
>
> Elle connaît deux choses : sa position, fixée à la construction, et un indicateur `is_taken`, qui vaut faux au départ.
>
> Le dessin est conditionnel : une gemme ramassée reste dans l’arbre, mais n’est plus dessinée. C’est plus simple que de la retirer, et cela évite de modifier l’arbre pendant son propre parcours.
>
> Les six positions sont dans la liste `GEM_POSITIONS`, réparties en cercle autour du centre, à 12 unités du sol.

### 05:50 — Ramasser une gemme

**À l’écran :** afficher la boucle de `Scene.on_update()`.

```python
distance = self.player.position.distance_to(gem.position)

if distance < GEM_RADIUS:
    gem.is_taken = True
    self.score += 1
```

**Narration :**

> La règle tient en trois lignes.
>
> `distance_to()` renvoie la longueur du segment entre deux points de l’espace. Si elle est inférieure au rayon de ramassage, la gemme est prise et le score augmente d’un point.
>
> La mesure se fait en trois dimensions, et cela compte : le joueur occupe la hauteur 8, les gemmes la hauteur 12. Sur le plan du sol, la portée réelle est un peu inférieure à 14 unités, et l’on ramasse la gemme en passant près d’elle. Un rayon de 14 pour des objets de 16 et 10 unités donne une règle indulgente, adaptée à un jeu de ramassage.

**Action :** ramasser les six gemmes à l’écran, lentement, en montrant le score qui monte.

### 07:10 — Gagner, figer, rejouer

**À l’écran :** afficher la fin de `Scene.on_update()`, puis `start_game()`.

```python
if self.score == len(self.gems):
    self.is_won = True
    self.player.active = False
```

**Narration :**

> Quand le score atteint le nombre de gemmes, la scène passe en victoire, et le joueur est désactivé.
>
> `active` est une propriété de tout nœud : quand elle vaut faux, le nœud et ses descendants ne sont plus mis à jour. Le joueur reste visible, mais il ne répond plus aux flèches : le cube s’immobilise sur l’image de victoire. Une ligne pour figer, une ligne pour réactiver.
>
> `start_game()` fait le reste : elle retire les anciennes gemmes avec `remove_child()`, en recrée six, remet le joueur au centre, le réactive, et remet le score et l’état de victoire à zéro.
>
> Trois remises à zéro qu’on oublie facilement : `active`, `is_won` et le score. Sans elles, le joueur reste immobile après un redémarrage, ou l’écran de victoire reste affiché.

**Action :** provoquer les trois oublis, un par un, puis revenir à la version correcte.

### 09:00 — Une caméra qui suit

**À l’écran :** afficher `update_camera()` et l’appel dans `App.draw()`.

```python
target = self.player.position
eye = Vec3(target.x, target.y + CAMERA_HEIGHT, target.z + CAMERA_DISTANCE)
self.camera.transform = Mat4.look_at(eye, target)
```

**Narration :**

> La caméra ne tourne plus autour d’un objet fixe : elle suit le joueur.
>
> Le point visé est le joueur lui-même. L’œil se place 70 unités plus haut et 90 unités plus loin sur l’axe `z`. L’angle de vue ne change jamais : le décor garde son orientation, et le joueur humain ne perd pas ses repères.
>
> L’appel se fait dans `App.draw()`, juste avant de dessiner la scène. L’ordre compte : la caméra se règle sur la position que la mise à jour vient de calculer, sans retard d’une image. Placée dans la mise à jour de la scène, elle aurait une image de retard, car les enfants d’un nœud sont mis à jour après lui.

### 10:20 — Le HUD par-dessus la 3D

**À l’écran :** afficher `App.draw()` en entier.

```python
score = f"Score : {self.scene.score}"
pyxel.text(4, 4, score, TEXT_COLOR)
```

**Narration :**

> Le score s’écrit avec `pyxel.text()`, exactement comme dans le parcours 2D.
>
> Il est dessiné après la scène : ce qui est écrit ensuite se retrouve au-dessus. L’ordre inverse cacherait le texte derrière l’image 3D.
>
> L’écran de victoire reprend les habitudes du chapitre 11 : un rectangle noir pour effacer le décor, trois textes, et des colonnes calculées par `text_x()`. La police reste la police interne, en ASCII, donc sans accents, et la largeur d’un caractère vaut quatre pixels.
>
> Trois lignes : « Victoire », le score, et le rappel de la barre d’espace.

### 11:50 — Erreurs fréquentes

**À l’écran :** provoquer quatre erreurs, une par une.

```text
add_child() oublié : aucune gemme
clamp() oublié : le joueur sort
caméra non mise à jour : elle reste immobile
textes dessinés avant la scène : ils disparaissent
```

**Narration :**

> Quatre erreurs.
>
> Un `add_child()` oublié : les gemmes n’existent pas dans l’arbre, et l’écran reste désespérément vide.
>
> `clamp()` oublié : le joueur quitte l’arène et marche sur le vide.
>
> La caméra non mise à jour : le joueur sort du cadre, puis disparaît.
>
> Les textes dessinés avant la scène : ils sont recouverts par l’image 3D, et l’on croit que le HUD ne fonctionne pas.

### 13:00 — Aller plus loin

**À l’écran :** afficher les trois outils non utilisés.

```text
Collider : physique
Mesh.from_glb() : modèles Blockbench
sphere(), plane(), boxb() : autres primitives
```

**Narration :**

> Trois outils de Pyxel Cube n’ont pas servi dans ce jeu, et ils sont faits pour la suite.
>
> `Collider` ajoute à un nœud une forme de collision, une masse, une gravité et un rebond. Une masse nulle rend un objet immobile : c’est ainsi qu’on déclare un sol. Avec la gravité, un jeu de plateforme 3D devient possible, mais la physique demande plus de réglage que la règle de distance de ce chapitre.
>
> `Mesh.from_glb()` charge un modèle exporté par Blockbench, l’éditeur conseillé par Pyxel. Attention : le dossier `assets` doit accompagner le `main.py`, et le projet n’est plus un fichier unique.
>
> Enfin, `sphere()`, `plane()` et `boxb()` complètent la boîte. Trois primitives et une caméra bien placée suffisent souvent à donner du caractère à un jeu.
>
> L’ordre d’apprentissage reste le même : d’abord un jeu qui fonctionne avec des boîtes, ensuite des modèles.

### 13:50 — À retenir

**À l’écran :** afficher les quatre phrases, puis le jeu en mouvement.

```text
Vec3 pour la position
clamp() pour l’arène
distance_to() pour le ramassage
active = False pour figer
```

**Narration :**

> Quatre phrases.
>
> Un `Vec3` garde la position, une translation la transmet à la scène.
>
> `pyxel.clamp()` garde le joueur dans l’arène.
>
> `distance_to()` mesure un écart en trois dimensions, ce qui suffit pour un ramassage.
>
> Et `active = False` fige un nœud sans le faire disparaître, ce qui donne un écran de victoire propre.
>
> Le module bonus s’arrête ici. Vous savez écrire une scène, organiser des nœuds, placer une caméra et faire un petit jeu en trois dimensions. La suite tient dans une phrase : prenez le jeu que vous aimez, et refaites-le avec vos idées.

## Consignes de montage

- Jouer une partie complète avant toute explication de code.
- Afficher le score en incrustation pendant les ramassages.
- Montrer l’arrêt net au bord de l’arène, côté `x` puis côté `z`.
- Provoquer les trois oublis de remise à zéro, sans couper, puis corriger.
- Montrer une fois le HUD dessiné avant la scène, pour rendre l’ordre visible.
- Terminer sur le jeu en mouvement, pas sur le code.
- Conserver le même code final que l’article `article.qmd`.

## Vérification avant publication

- Le code compile et s’exécute avec Pyxel 3.0.1.
- Six gemmes sont visibles, le score démarre à zéro.
- Le joueur s’arrête à 80 unités du centre sur les deux axes.
- La caméra garde le joueur au centre de l’image.
- La victoire s’obtient avec six gemmes, et la barre d’espace relance une partie complète.
- La touche `Q` ferme la fenêtre dans tous les états.
- Aucun texte affiché ne contient d’accent.
- Le code affiché est identique à celui de l’article.
