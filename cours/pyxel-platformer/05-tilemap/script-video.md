# Leçon 5 — Le niveau et la tilemap

## Fiche de production

- **Formation :** Créer un mini-platformer 2D avec Pyxel
- **Public :** débutants en création de jeux, élèves de Première et Terminale NSI
- **Environnement :** PyxelStudio dans Capytale
- **Version ciblée :** Pyxel 3.0.1
- **Durée cible :** 14 à 16 minutes
- **Fichiers du projet :** `main.py` et `res.pyxres`
- **Ressource utilisée :** `res.pyxres`, inchangée
- **Titre à l’écran :** Leçon 5 — Le niveau et la tilemap

## Intention pédagogique

Cette leçon ouvre la tilemap et transforme le décor en donnée interrogeable.

Le travail porte sur quatre points :

- la tilemap comme grille de cases de 8 × 8 pixels ;
- la conversion entre pixels et cases ;
- la lecture d’une case avec `pget()` ;
- la reconnaissance des cases solides par une méthode dédiée.

La classe `Level` expose une question, `is_solid()`, sans l’utiliser pour arrêter le joueur. Cette séparation prépare la leçon sur les collisions.

Un affichage de contrôle montre en permanence la case située sous les pieds du joueur.

## Objectifs annoncés aux élèves

À la fin de la vidéo, l’élève doit pouvoir :

1. expliquer la différence entre pixels et cases ;
2. convertir une position en coordonnées de case ;
3. lire une case de tilemap avec `pget()` ;
4. utiliser l’objet `pyxel.tilemaps[0]` ;
5. définir la liste des tuiles solides ;
6. interroger le niveau avec une méthode.

## Préparation de l’enregistrement

### Fichiers

- `main.py` de la leçon 5, dans le dossier `05-tilemap` ;
- `res.pyxres` recopié à côté de ce fichier.

### Vérifications avant d’enregistrer

- Le joueur se déplace et saute comme dans la leçon 4.
- L’affichage indique `Case 5,28 : solide` au démarrage.
- Le numéro de case change pendant le déplacement.
- L’état affiché alterne pendant un saut.
- Le joueur traverse toujours les plateformes.

### Code final

```python
import pyxel


SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
RESOURCE_FILE = "res.pyxres"

TILE_SIZE = 8
LEVEL_WIDTH = 32
LEVEL_HEIGHT = 32
GROUND_Y = 224
SOLID_TILES = (
    (0, 1),
    (1, 1),
    (2, 1),
)

PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLAYER_SPEED = 2
GRAVITY = 1
JUMP_SPEED = -11
PLAYER_TILE_X = 0
PLAYER_TILE_Y = 0
PLAYER_START_X = 40
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

    def is_solid(self, tile_x, tile_y):
        tile = self.tilemap.pget(tile_x, tile_y)
        return tile in SOLID_TILES


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.dx = 0
        self.dy = 0
        self.is_on_ground = True

    def update(self):
        self.dx = 0

        if pyxel.btn(pyxel.KEY_LEFT):
            self.dx = -PLAYER_SPEED
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.dx = PLAYER_SPEED

        self.x += self.dx
        self.x = pyxel.clamp(
            self.x,
            0,
            pyxel.width - self.width,
        )

        if pyxel.btnp(pyxel.KEY_SPACE) and self.is_on_ground:
            self.dy = JUMP_SPEED
            pyxel.play(0, JUMP_SOUND)

        self.dy += GRAVITY
        self.y += self.dy

        if self.y + self.height >= GROUND_Y:
            self.y = GROUND_Y - self.height
            self.dy = 0
            self.is_on_ground = True
        else:
            self.is_on_ground = False

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
            title="Chapitre 5 - niveau",
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

        self.player.update()

    def draw(self):
        pyxel.cls(BACKGROUND_COLOR)
        self.level.draw()

        tile_x = self.player.x // TILE_SIZE
        tile_y = (self.player.y + self.player.height) // TILE_SIZE

        if self.level.is_solid(tile_x, tile_y):
            state = "solide"
        else:
            state = "vide"

        pyxel.text(
            4,
            4,
            "Chapitre 5 - niveau",
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
            f"Case {tile_x},{tile_y} : {state}",
            TEXT_COLOR,
        )

        self.player.draw()


Game()
```

## Découpage détaillé

### 00:00 — Montrer le résultat

**À l’écran :** lancer le jeu. Le joueur se déplace et saute. Une troisième ligne de texte affiche la case sous ses pieds.

**Narration :**

> Dans cette cinquième leçon, le décor devient une donnée que le programme peut consulter.
>
> Le jeu affiche en permanence la case située sous les pieds du joueur, et indique si cette case est solide ou vide.
>
> Le déplacement et le saut ne changent pas. Le joueur traverse toujours les plateformes : le programme sait seulement si une case est solide, il ne s’en sert pas encore pour le bloquer.

**Action :** déplacer le joueur au-dessus du sol, puis au-dessus d’une pièce, et montrer les deux états affichés.

### 00:50 — Présenter les objectifs

**À l’écran :** afficher les quatre points :

```text
1. une grille de cases de 8 x 8 pixels
2. des pixels vers les cases
3. lire une case : pget()
4. quelles cases sont solides
```

**Narration :**

> Quatre étapes mènent à cette lecture du niveau.
>
> Le décor est une grille de cases. Une position exprimée en pixels doit être convertie en numéro de case. Une case se lit avec `pget()`. Enfin, une liste indique quelles tuiles arrêtent le joueur.

### 01:40 — Observer la tilemap

**À l’écran :** ouvrir l’éditeur de tilemap et survoler le niveau.

**Narration :**

> La tilemap mesure 32 cases de large et 32 cases de haut. Chaque case fait 8 pixels : le niveau couvre donc 256 pixels sur 256, exactement la fenêtre.
>
> La ligne 28 contient le dessus du sol. Les lignes suivantes contiennent le remplissage. Les plateformes occupent les lignes 23, 19 et 15.
>
> Une case ne contient pas un dessin : elle contient les coordonnées d’une tuile de la banque d’images. La case (5, 28), par exemple, contient la tuile du dessus du sol.

### 03:00 — Passer des pixels aux cases

**À l’écran :** afficher la conversion :

```python
tile_x = x // TILE_SIZE
tile_y = y // TILE_SIZE
```

**Narration :**

> Le joueur est positionné en pixels. La tilemap se lit en cases. Il faut donc convertir.
>
> La division entière par la taille d’une case donne le numéro de la case. Une position de 40 pixels correspond à la case 5, car 40 divisé par 8 donne 5.
>
> Une position de 47 pixels correspond encore à la case 5 : toutes les positions d’une même case renvoient le même numéro.
>
> La même conversion s’applique verticalement. La coordonnée 224 correspond à la case 28, la ligne du sol.

**À l’écran :** afficher le tableau :

```text
40 // 8 = 5     47 // 8 = 5     48 // 8 = 6
224 // 8 = 28
```

**Narration :**

> Nous utilisons la constante `TILE_SIZE` plutôt que le nombre 8. Si la taille des tuiles changeait, une seule constante serait à modifier.

### 04:40 — Utiliser l’objet tilemap

**À l’écran :** modifier `Level.__init__()` :

```python
self.tilemap = pyxel.tilemaps[0]
```

**Narration :**

> Jusqu’ici, le dessin du niveau utilisait le numéro 0 pour désigner la tilemap.
>
> `pyxel.tilemaps[0]` désigne la première tilemap chargée depuis le fichier de ressources. C’est un objet, et non un simple numéro.
>
> La classe `Level` le conserve dans un attribut : elle pourra le dessiner et l’interroger.

**À l’écran :** modifier le dessin :

```python
pyxel.bltm(
    0,
    0,
    self.tilemap,
    0,
    0,
    self.width,
    self.height,
)
```

**Narration :**

> `pyxel.bltm()` accepte un numéro ou un objet. Avec l’objet, le niveau est décrit à partir de ses propres données.

### 06:00 — Lire une case

**À l’écran :** ajouter une méthode :

```python
def is_solid(self, tile_x, tile_y):
    tile = self.tilemap.pget(tile_x, tile_y)
    return tile in SOLID_TILES
```

**Narration :**

> `pget()` lit le contenu d’une case. Elle renvoie les coordonnées de la tuile, par exemple `(0, 1)` pour le dessus du sol.
>
> L’ordre des paramètres est celui de toutes les coordonnées de Pyxel : l’horizontale d’abord, la verticale ensuite. Et ces coordonnées sont des cases, pas des pixels.
>
> La seconde ligne compare la tuile lue à la liste des tuiles solides. L’opérateur `in` renvoie vrai si la valeur figure dans la liste.

### 07:20 — Définir les tuiles solides

**À l’écran :** ajouter la constante :

```python
SOLID_TILES = (
    (0, 1),
    (1, 1),
    (2, 1),
)
```

**Narration :**

> Trois tuiles arrêtent le joueur : le dessus du sol, le remplissage du sol et la plateforme.
>
> La pièce et le buisson n’en font pas partie : ils se ramassent ou décorent, ils ne s’escaladent pas.
>
> La case vide, elle, correspond à la tuile située en bas à droite de la zone utilisée de la banque d’images.

**À l’écran :** afficher le tableau :

```text
(0, 1) dessus du sol   solide
(1, 1) remplissage     solide
(2, 1) plateforme      solide
(3, 1) piece           traversable
(4, 1) buisson         traversable
```

**Narration :**

> Ajouter une tuile solide ne demande aucune modification de la méthode : il suffit d’ajouter un couple dans la constante.

### 08:20 — Une méthode qui répond à une question

**À l’écran :** montrer la méthode complète.

```python
def is_solid(self, tile_x, tile_y):
    tile = self.tilemap.pget(tile_x, tile_y)
    return tile in SOLID_TILES
```

**Narration :**

> Cette méthode ne déplace rien et ne corrige rien. Elle répond vrai ou faux.
>
> Cette forme est volontaire : la même question servira pour le sol, les murs et les plafonds. La manière de réagir à la réponse sera écrite dans la leçon suivante.

### 09:10 — Afficher un contrôle

**À l’écran :** ajouter dans `Game.draw()` :

```python
tile_x = self.player.x // TILE_SIZE
tile_y = (self.player.y + self.player.height) // TILE_SIZE
```

**Narration :**

> Pour rendre ce travail visible, nous calculons la case située sous les pieds du joueur.
>
> Le bas du joueur se trouve à sa position verticale plus sa hauteur. C’est cette valeur qui donne la case du sol, et non le haut du personnage.

**À l’écran :** compléter :

```python
if self.level.is_solid(tile_x, tile_y):
    state = "solide"
else:
    state = "vide"

pyxel.text(
    4,
    20,
    f"Case {tile_x},{tile_y} : {state}",
    TEXT_COLOR,
)
```

**Narration :**

> Le jeu interroge le niveau, puis affiche le résultat sous les deux premières lignes de texte.
>
> Au repos, le joueur est posé sur le sol : la case est 5, 28 et l’état affiché est solide.

### 10:20 — Exécuter et vérifier

**Action :** lancer le jeu et dérouler les vérifications.

**Narration :**

> Nous vérifions maintenant le comportement.
>
> Au démarrage, l’affichage indique la case 5, 28 et l’état solide.
>
> En avançant vers la droite, le numéro de case augmente ; vers la gauche, il diminue.
>
> Pendant un saut, le numéro de case diminue. Lorsque le joueur passe devant une plateforme, l’état affiché devient solide, alors qu’il n’est pas arrêté : la collision n’est pas encore traitée.
>
> Au-dessus d’une pièce, l’état affiché reste vide.

### 11:30 — Erreurs fréquentes

**À l’écran :** afficher la liste :

```text
case toujours vide          -> pixels passés à pget() sans conversion
case au-dessus du sol       -> mauvais y (haut du joueur)
tuile solide oubliée        -> SOLID_TILES incomplète
pièce devenue solide        -> (3, 1) ajoutée par erreur
```

**Narration :**

> Quatre erreurs sont fréquentes.
>
> Une case toujours vide vient de coordonnées en pixels passées directement à `pget()`.
>
> Une case lue au-dessus du sol vient de l’utilisation de la position du haut du joueur au lieu du bas.
>
> Un joueur qui semble traverser le sol alors que la case est solide indique une liste incomplète.
>
> Enfin, ajouter la tuile de la pièce dans la liste des tuiles solides transforme un objet à ramasser en mur.

**Action :** montrer l’erreur de conversion en retirant la division, puis rétablir.

### 12:50 — Expérimentations et conclusion

**À l’écran :** afficher la liste :

```text
- rendre le buisson solide
- dessiner un repère sur les cases solides
- effacer une case avec pset()
- afficher la case du bord droit du joueur
```

**Narration :**

> Plusieurs essais sont instructifs.
>
> Ajouter le buisson dans la liste des tuiles solides ne change rien au déplacement, mais modifie l’affichage : la constante est bien la seule source de vérité.
>
> Dessiner un petit repère sur chaque case solide permet de vérifier la liste d’un seul coup d’œil.
>
> `pset()` remplace le contenu d’une case : la tuile disparaît du dessin, sans modifier la position du joueur.
>
> Dans la prochaine leçon, cette lecture du niveau sert enfin à quelque chose : le joueur s’arrête sur les plateformes.

## Consignes de montage

- Montrer la tilemap dans l’éditeur avant de parler de cases.
- Afficher en incrustation la conversion pixels vers cases avec deux ou trois exemples.
- Faire apparaître le tableau des tuiles solides au moment où `SOLID_TILES` est écrit.
- Garder l’affichage du contrôle visible pendant toute la phase de vérification.
- Conserver le même code final que l’article `article.qmd`.

## Vérification avant publication

- Le code compile et s’exécute avec Pyxel 3.0.1.
- `pyxel.tilemaps[0]` est bien stocké dans `Level` et passé à `pyxel.bltm()`.
- `pget()` est appelé avec des coordonnées de cases.
- Les tuiles (0, 1), (1, 1) et (2, 1) sont reconnues comme solides.
- La pièce et le buisson sont reconnus comme traversables.
- L’affichage indique `Case 5,28 : solide` au démarrage.
- Le déplacement et le saut sont identiques à la leçon 4.
- Le code affiché est identique à celui de l’article.
