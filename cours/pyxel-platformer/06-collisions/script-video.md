# Leçon 6 — Les collisions avec la tilemap

## Fiche de production

- **Formation :** Créer un mini-platformer 2D avec Pyxel
- **Public :** débutants en création de jeux, élèves de Première et Terminale NSI
- **Environnement :** PyxelStudio dans Capytale
- **Version ciblée :** Pyxel 3.0.1
- **Durée cible :** 16 à 18 minutes
- **Fichiers du projet :** `main.py` et `res.pyxres`
- **Ressource utilisée :** `res.pyxres`, inchangée
- **Titre à l’écran :** Leçon 6 — Les collisions avec la tilemap

## Intention pédagogique

Cette leçon rend le décor solide.

Le travail porte sur cinq points :

- le joueur décrit par un rectangle englobant ;
- la distinction entre déplacement demandé et déplacement autorisé ;
- l’appel à `Tilemap.collide()` ;
- le rôle de la liste des tuiles qui font obstacle ;
- la déduction de l’état « au sol » à partir du résultat.

La méthode `is_solid()` de la leçon 5 disparaît : `collide()` fait le même travail, mais rend un déplacement utilisable. La constante `SOLID_TILES` reste, c’est elle qui décide de ce qui arrête le joueur.

Un affichage indique en permanence si le joueur est posé au sol.

## Objectifs annoncés aux élèves

À la fin de la vidéo, l’élève doit pouvoir :

1. décrire le joueur par un rectangle ;
2. expliquer la différence entre déplacement demandé et déplacement autorisé ;
3. appeler `collide()` avec ses sept arguments ;
4. fournir la liste des tuiles qui font obstacle ;
5. empêcher le joueur de traverser le sol et les plateformes ;
6. déterminer si le joueur est au sol.

## Préparation de l’enregistrement

### Fichiers

- `main.py` de la leçon 6, dans le dossier `06-collisions` ;
- `res.pyxres` recopié à côté de ce fichier.

### Vérifications avant d’enregistrer

- Le joueur démarre à gauche du niveau, posé sur le sol, et l’affichage indique `Au sol : oui`.
- Il ne traverse plus le sol, même en tombant de haut.
- Un saut sous la première plateforme est coupé par le plafond.
- Un saut en terrain dégagé monte d’environ 55 pixels.
- Un saut suivi d’un appui sur la flèche droite permet d’atterrir sur la plateforme.
- Le joueur peut marcher sur la plateforme et retombe en la quittant.
- Aucune vibration n’apparaît lorsque le joueur reste immobile sur le sol.

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
            title="Leçon 6 - collisions",
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
            "Leçon 6 - collisions",
            TEXT_COLOR,
        )
        pyxel.text(
            4,
            12,
            "Flèches : déplacer, Espace : sauter",
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
```

## Découpage détaillé

### 00:00 — Montrer le résultat

**À l’écran :** lancer le jeu. Le joueur se déplace, saute, s’arrête sur le sol et sur les plateformes. La troisième ligne de texte indique `Au sol : oui`.

**Narration :**

> Dans cette sixième leçon, le décor devient solide.
>
> Le joueur ne traverse plus le sol. Il peut sauter sous une plateforme sans la traverser, se poser dessus, en descendre, et se cogner contre son flanc.
>
> L’affichage indique en permanence s’il est posé au sol. Cette information servira à autoriser le saut.
>
> Le déplacement, la gravité et le saut gardent les mêmes valeurs que dans les leçons précédentes. Seule la façon d’appliquer le mouvement change.

**Action :** dérouler trois situations : marcher vers la gauche jusqu’au bord, sauter sous la plateforme, puis sauter et avancer pour se poser dessus.

### 00:55 — Présenter les objectifs

**À l’écran :** afficher les quatre points :

```text
1. le joueur est un rectangle
2. un déplacement demandé, un déplacement autorisé
3. collide() corrige le mouvement
4. au sol : oui ou non
```

**Narration :**

> Quatre étapes mènent à un décor solide.
>
> Le joueur est d’abord un rectangle de 8 pixels sur 8. Ensuite, un déplacement se demande avant d’être appliqué : le niveau peut le refuser ou le raccourcir. La méthode `collide()` fait cette vérification. Enfin, le résultat indique si le joueur touche le sol.

### 01:40 — Le rectangle du joueur

**À l’écran :** afficher le rectangle du personnage, puis zoomer sur ses pieds et sur la première ligne du sol.

**Narration :**

> Une collision ne se calcule pas sur un dessin : elle se calcule sur un rectangle.
>
> Le joueur occupe un rectangle de 8 pixels de large et de 8 pixels de haut. Son coin supérieur gauche est la position `x`, `y` du personnage.
>
> Le rectangle couvre les pixels de `x` à `x + width - 1`. Un joueur posé sur le sol occupe donc la ligne 27, alors que le sol commence à la ligne 28 : les pieds touchent le sol sans y entrer.
>
> C’est ce détail d’un pixel qui explique les arrêts nets que nous allons observer.

**Action :** montrer le rectangle en surimpression pendant un saut, puis le faire disparaître.

### 03:00 — Un déplacement demandé, un déplacement autorisé

**À l’écran :** afficher côte à côte les deux versions de la mise à jour :

```python
self.x += self.dx          # leçons 3 à 5
self.y += self.dy
```

```python
self.dx, self.dy = self.level.move_player(...)
self.x += self.dx
self.y += self.dy
```

**Narration :**

> Jusqu’ici, le programme calculait un déplacement et l’appliquait immédiatement. `self.x += self.dx`, puis `self.y += self.dy`.
>
> Cette fois, le déplacement passe par le niveau avant d’être appliqué.
>
> Le joueur exprime une intention : avancer de `dx` et descendre de `dy`. Le niveau examine la trajectoire et renvoie un déplacement compatible avec le décor, souvent plus court, parfois nul.
>
> La différence entre les deux valeurs est toute la collision. Demander 2 pixels et n’en obtenir aucun signifie que le personnage touche un mur.

### 04:20 — La méthode move_player()

**À l’écran :** écrire la méthode dans la classe `Level`.

**Narration :**

> La classe `Level` reçoit une méthode `move_player()`. Elle prend la position du rectangle, son déplacement demandé, et renvoie le déplacement corrigé.
>
> Elle ne modifie rien : elle interroge la tilemap et transmet le résultat. Les dimensions du joueur viennent des constantes `PLAYER_WIDTH` et `PLAYER_HEIGHT`, ce qui évite de les répéter à chaque appel.
>
> Le nom annonce le rôle : cette méthode déplace le joueur, dans les limites du décor.

### 05:40 — La signature de collide()

**À l’écran :** afficher le tableau des arguments.

```text
x, y        position du rectangle, en pixels
w, h        taille du rectangle, en pixels
dx, dy      déplacement demandé, en pixels
walls       tuiles qui font obstacle
```

**Narration :**

> `collide()` prend sept arguments et renvoie deux valeurs : un déplacement horizontal et un déplacement vertical corrigés.
>
> Les quatre premiers décrivent le rectangle. Les deux suivants décrivent le mouvement demandé. Le dernier est la liste des tuiles qui font obstacle.
>
> Cette liste contient des coordonnées de tuiles dans la banque d’images, comme celles que renvoie `pget()`, et non des positions dans la tilemap. Ce sont les mêmes valeurs que dans la leçon précédente, écrites entre crochets : `SOLID_TILES`.
>
> Attention : la méthode renvoie un déplacement, pas une position. Il faut l’affecter à `self.dx` et `self.dy`, puis ajouter le résultat à la position.

**Action :** provoquer volontairement l’erreur, appeler `move_player()` sans récupérer le résultat, montrer que le joueur traverse, puis rétablir l’affectation.

### 07:20 — Vérifier le sol et le plafond

**À l’écran :** montrer le sol puis le dessous de la première plateforme, avec les lignes de cases en surimpression.

**Narration :**

> Le même appel traite les trois directions.
>
> Quand le joueur est posé, la gravité demande une descente d’un pixel. La case sous ses pieds est solide : le déplacement vertical revient à zéro, et la position reste à 216. À chaque image, le même scénario se répète, sans flottement.
>
> Quand il saute sous une plateforme, le déplacement vers le haut est coupé : la tête du joueur reste sous la ligne 23.
>
> Quand il court contre un flanc, le déplacement horizontal est annulé : le joueur s’arrête au bord de la case.
>
> Enfin, dans le vide, aucune case solide n’est rencontrée : le déplacement est renvoyé tel quel, et la chute suit la gravité.

**Action :** montrer successivement les quatre situations, en commentant la valeur du déplacement renvoyé.

### 08:50 — Au sol : oui ou non

**À l’écran :** écrire les deux lignes dans `Player.update()`.

```python
was_falling = self.dy > 0
self.dx, self.dy = self.level.move_player(...)

self.is_on_ground = was_falling and self.dy == 0
```

**Narration :**

> Le saut n’est autorisé que si le joueur touche le sol. Cette information se lit maintenant dans le résultat de la collision.
>
> Nous retenons d’abord si le joueur était en train de tomber, avant l’appel. Puis nous demandons le déplacement autorisé.
>
> Trois cas se présentent. Si le joueur tombait et que son déplacement vertical est annulé, il vient de se poser. S’il tombait et descend encore, il est en l’air. S’il montait, il saute, donc il n’est pas au sol.
>
> La variable `was_falling` est indispensable : après l’appel, `self.dy` vaut zéro au sol. La lire après reviendrait à considérer que le joueur est toujours en l’air, et le saut ne fonctionnerait plus.

### 10:10 — Pourquoi is_solid() disparaît

**À l’écran :** montrer la classe `Level` de la leçon 5, puis celle de la leçon 6.

**Narration :**

> La méthode `is_solid()` de la leçon précédente répondait à une question sur une case précise. `collide()` répond à une question plus utile : quel déplacement est possible pour ce rectangle ?
>
> Elle consulte elle-même les cases de la trajectoire et utilise la liste des tuiles solides. Garder `is_solid()` laisserait dans la classe une méthode que plus personne n’appelle.
>
> La liste `SOLID_TILES`, en revanche, reste : c’est le seul endroit où l’on décide ce qui arrête le joueur.

### 11:00 — L’ordre des opérations

**À l’écran :** afficher la liste :

```text
1. remettre dx à zéro, lire les flèches
2. sauter si espace et si au sol
3. ajouter la gravité, puis demander le déplacement autorisé
4. appliquer, maintenir dans la fenêtre, mettre à jour is_on_ground
```

**Narration :**

> La mise à jour du joueur suit quatre étapes.
>
> Le déplacement horizontal se décide d’abord. Le saut est ensuite déclenché si la touche espace vient d’être pressée et si le joueur est au sol. La gravité s’ajoute alors à `dy`, et c’est ce déplacement complet qui est soumis au niveau. Enfin, le déplacement corrigé est appliqué, le joueur est maintenu dans la fenêtre avec `clamp()`, et l’état au sol est mis à jour.
>
> La gravité est ajoutée avant l’appel : le niveau corrige ainsi le mouvement réel de l’image, et non celui de l’image précédente.

### 12:00 — Exécuter et vérifier

**Action :** lancer le jeu et dérouler les vérifications.

**Narration :**

> Nous vérifions maintenant le comportement.
>
> Au démarrage, le joueur est posé sur le sol, à gauche du niveau, et l’affichage indique `Au sol : oui`.
>
> Vers la gauche, il s’arrête au bord de l’écran. En terrain dégagé, le saut monte d’environ 55 pixels et revient exactement à 216.
>
> Sous la première plateforme, le saut est coupé : la tête reste sous la ligne 23, puis le joueur retombe.
>
> En sautant puis en appuyant sur la flèche droite, le joueur atterrit sur la plateforme, à la position 176. Il peut y marcher, puis retomber en la quittant par la droite.
>
> Pendant un saut, l’affichage indique `Au sol : non`. Il repasse à `oui` à l’atterrissage.

### 13:20 — Erreurs fréquentes

**À l’écran :** afficher la liste :

```text
déplacement appliqué deux fois -> self.x + self.dx passé à collide()
résultat ignoré                -> self.dx, self.dy non réaffectés
murs en cases du niveau        -> liste de coordonnées de tilemap
tuile de remplissage oubliée   -> (2, 1) absente de SOLID_TILES
saut impossible                -> was_falling lu après l’appel
```

**Narration :**

> Cinq erreurs sont fréquentes.
>
> Passer `self.x + self.dx` au lieu de `self.x` décale le rectangle avant la vérification : le joueur avance du double et peut traverser une case.
>
> Appeler `move_player()` sans récupérer les deux valeurs ne corrige rien : le déplacement demandé est appliqué tel quel.
>
> Une liste de coordonnées de cases du niveau, au lieu des tuiles de la banque d’images, ne bloque jamais rien.
>
> Oublier la tuile de remplissage du sol laisse le joueur s’enfoncer dès que la case du dessus n’est plus solide.
>
> Enfin, un joueur qui ne saute plus est un joueur qui n’est jamais considéré comme posé : vérifiez l’ordre des lignes dans `update()`.

**Action :** provoquer l’erreur du déplacement appliqué deux fois, montrer le joueur qui traverse la plateforme, puis rétablir.

### 15:00 — Expérimentations et conclusion

**À l’écran :** afficher la liste :

```text
- rendre le buisson solide
- ajouter un mur au bord droit
- afficher le déplacement autorisé
- augmenter la puissance du saut
- renvoyer le joueur au départ sur une case dangereuse
```

**Narration :**

> Plusieurs essais sont instructifs.
>
> Ajouter la tuile du buisson dans la liste rend les buissons solides, sans toucher au code du joueur.
>
> Remplir la colonne de droite avec une tuile pleine crée un mur : le joueur s’arrête avant le bord, poussé par la collision et non plus par `clamp()`.
>
> Afficher `dx` à l’écran montre le déplacement réellement appliqué : il reste à zéro contre un mur et suit la gravité en chute libre.
>
> Augmenter la puissance du saut permet d’atteindre la deuxième plateforme. Un déplacement de 14 pixels est coupé comme un déplacement de 2 : la correction ne dépend pas de la vitesse.
>
> Enfin, tester la case sous les pieds du joueur permet de le renvoyer au départ : la collision corrige le mouvement, la lecture de case déclenche un effet.
>
> Dans la prochaine leçon, le niveau accueille plusieurs types d’objets : les pièces deviennent des objets à part entière, avec leur propre mise à jour et leur propre dessin.

## Consignes de montage

- Montrer le rectangle du joueur en surimpression avant de parler de collision.
- Afficher en incrustation les deux versions de la mise à jour, avant et après l’introduction de `move_player()`.
- Faire apparaître le tableau des arguments de `collide()` au moment de l’écriture de la méthode.
- Garder l’affichage `Au sol` visible pendant toute la phase de vérification.
- Conserver le même code final que l’article `article.html`.

## Vérification avant publication

- Le code compile et s’exécute avec Pyxel 3.0.1.
- La signature utilisée est bien `collide(x, y, w, h, dx, dy, walls)`.
- `walls` reçoit `SOLID_TILES`, liste de tuiles et non de cases.
- `is_solid()` n’est plus appelée nulle part.
- Le joueur ne traverse plus le sol, même avec une vitesse de chute élevée.
- Il reste à `y = 216` sur le sol et à `y = 176` sur la première plateforme.
- Un saut sous la plateforme est coupé, la tête reste sous la ligne 23.
- Un saut en terrain dégagé monte d’environ 55 pixels.
- `Au sol : non` s’affiche pendant un saut et `oui` à l’atterrissage.
- Le code affiché est identique à celui de l’article.
