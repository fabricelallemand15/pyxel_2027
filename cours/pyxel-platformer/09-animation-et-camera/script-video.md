# Leçon 9 — Animation et caméra

## Fiche de production

- **Formation :** Créer un mini-platformer 2D avec Pyxel
- **Public :** débutants en création de jeux, élèves de Première et Terminale NSI
- **Environnement :** PyxelStudio dans Capytale
- **Version ciblée :** Pyxel 3.0.1
- **Durée cible :** 16 à 18 minutes
- **Fichiers du projet :** `main.py` et `res.pyxres`
- **Ressource utilisée :** `res.pyxres`, inchangée ; son niveau est simplement dessiné en entier
- **Titre à l’écran :** Leçon 9 — Animation et caméra

## Intention pédagogique

Cette leçon donne vie au personnage et au décor.

Le travail porte sur cinq points :

- les quatre images du joueur, utilisées selon son état ;
- `pyxel.frame_count` comme horloge d’animation ;
- le retournement du sprite par une largeur négative ;
- un niveau deux fois plus large que la fenêtre ;
- la caméra comme décalage de dessin.

Le point délicat est la distinction entre coordonnées du monde et coordonnées de l’écran : les objets ne bougent pas, c’est le dessin qui est décalé.

## Objectifs annoncés aux élèves

À la fin de la vidéo, l’élève doit pouvoir :

1. choisir une image selon l’état du personnage ;
2. rythmer une animation avec `pyxel.frame_count` ;
3. retourner un sprite horizontalement ;
4. dessiner un niveau plus grand que l’écran ;
5. calculer et appliquer un décalage de caméra ;
6. remettre la caméra à zéro avant de dessiner l’interface.

## Préparation de l’enregistrement

### Fichiers

- `main.py` de la leçon 9, dans le dossier `09-animation-et-camera` ;
- `res.pyxres` recopié à côté de ce fichier.

### Vérifications avant d’enregistrer

- Le joueur est au repos, image `(0, 0)`, caméra à 0 au démarrage.
- En marchant à droite ou à gauche, les deux images de marche alternent.
- Le sprite est retourné quand le joueur va vers la gauche, sans se décaler.
- Pendant un saut, l’image `(1, 0)` reste affichée.
- En poussant contre un mur, le joueur reprend l’image de repos.
- Le décor défile et le joueur reste au centre de la fenêtre.
- La caméra s’arrête à 0 et à 256 ; le joueur s’arrête à 0 et à 504.
- Le score reste fixe en haut de l’écran pendant le défilement.
- Le compteur affiche dix-huit pièces et trois ennemis.

### Code final

```python
import pyxel


SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
RESOURCE_FILE = "res.pyxres"

TILE_SIZE = 8
LEVEL_WIDTH = 64
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
PLAYER_IDLE_TILE = (0, 0)
PLAYER_JUMP_TILE = (1, 0)
PLAYER_WALK_TILES = [
    (2, 0),
    (3, 0),
]
ANIMATION_SPEED = 6
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
        self.is_facing_right = True
        self.tile = PLAYER_IDLE_TILE
        self.level = level

    def update(self):
        self.dx = 0

        if pyxel.btn(pyxel.KEY_LEFT):
            self.dx = -PLAYER_SPEED
            self.is_facing_right = False
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.dx = PLAYER_SPEED
            self.is_facing_right = True

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
            self.level.width - self.width,
        )
        self.y += self.dy

        self.is_on_ground = was_falling and self.dy == 0
        self.choose_tile()

    def draw(self):
        tile_x, tile_y = self.tile

        if self.is_facing_right:
            width = self.width
        else:
            width = -self.width

        pyxel.blt(
            self.x,
            self.y,
            0,
            tile_x * TILE_SIZE,
            tile_y * TILE_SIZE,
            width,
            self.height,
            TRANSPARENT_COLOR,
        )

    def choose_tile(self):
        if not self.is_on_ground:
            self.tile = PLAYER_JUMP_TILE
        elif self.dx != 0:
            index = pyxel.frame_count // ANIMATION_SPEED % 2
            self.tile = PLAYER_WALK_TILES[index]
        else:
            self.tile = PLAYER_IDLE_TILE


class Game:
    def __init__(self):
        pyxel.init(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            title="Leçon 9 - animation et caméra",
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
            Enemy(320, 216, 288, 440),
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

        camera_x = pyxel.clamp(
            self.player.x + self.player.width // 2 - pyxel.width // 2,
            0,
            self.level.width - pyxel.width,
        )
        pyxel.camera(camera_x, 0)

        self.level.draw()

        for coin in self.coins:
            coin.draw()

        for enemy in self.enemies:
            enemy.draw()

        self.player.draw()

        pyxel.camera()

        pyxel.text(
            4,
            4,
            "Leçon 9 - animation et caméra",
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
            f"Score : {self.score}  Pièces : {len(self.coins)}",
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
```

## Découpage détaillé

### 00:00 — Montrer le résultat

**À l’écran :** lancer le jeu. Le personnage marche, s’arrête, saute, se retourne ; le décor défile quand il avance vers la droite.

**Narration :**

> Dans cette neuvième leçon, le personnage s’anime et le décor défile.
>
> Les jambes bougent quand il marche, il reprend une image fixe à l’arrêt, et une autre image pendant le saut. Quand il va vers la gauche, le sprite est retourné.
>
> Le niveau est deux fois plus large que la fenêtre : en avançant, le décor défile, et le personnage reste au centre. L’interface, elle, ne bouge pas.
>
> Les règles de la leçon précédente sont inchangées : les pièces se ramassent, les ennemis arrêtent la partie.

**Action :** traverser le niveau d’un bout à l’autre pour montrer le défilement et l’arrêt de la caméra aux deux extrémités.

### 00:55 — Présenter les objectifs

**À l’écran :** afficher les quatre points :

```text
1. quatre images, un état
2. frame_count comme horloge
3. largeur négative : sprite retourné
4. caméra : un décalage de dessin
```

**Narration :**

> Quatre étapes structurent la leçon.
>
> D’abord les quatre images du joueur, choisies selon son état. Ensuite le compteur d’images, qui rythme l’alternance. Puis le retournement du sprite, obtenu sans nouveau dessin. Enfin la caméra, qui décale le dessin pour faire défiler un niveau plus grand que l’écran.

### 01:40 — Les quatre images du joueur

**À l’écran :** ouvrir l’éditeur d’images et encadrer les quatre tuiles de la ligne 0.

**Narration :**

> Depuis la leçon 2, la banque d’images contient quatre dessins du joueur : deux au repos, deux en marche. Jusqu’ici, un seul servait.
>
> Nous les déclarons en constantes : une pour le repos, une pour le saut, et une liste pour les deux images de marche.
>
> La liste est là parce que ces deux images s’utilisent à tour de rôle : un index de zéro ou un suffit à choisir.

### 03:00 — Choisir l’image

**À l’écran :** écrire `choose_tile()` et le tableau des trois cas.

```text
pas au sol      -> image de saut
au sol, dx ≠ 0  -> image de marche
au sol, dx = 0  -> image de repos
```

**Narration :**

> La méthode `choose_tile()` examine trois cas, dans cet ordre.
>
> Si le joueur n’est pas au sol, il saute : l’image de saut s’applique, même s’il se déplace. Sinon, s’il avance, l’image de marche alterne. Sinon, il est à l’arrêt : image de repos.
>
> L’ordre compte : un joueur qui saute en avant remplit deux conditions, et c’est la première qui décide.
>
> La méthode est appelée à la fin de `update()`, une fois la position et l’état au sol connus. Appelée plus tôt, elle lirait les valeurs de l’image précédente.
>
> Un détail agréable : `dx` est le déplacement réellement autorisé par la collision. Un joueur qui pousse contre un mur a donc `dx` à zéro et reprend l’image de repos, au lieu de marcher sur place.

### 04:40 — Le temps en images

**À l’écran :** afficher le tableau du compteur, puis l’expression.

**Narration :**

> `pyxel.frame_count` est un compteur fourni par Pyxel : il vaut zéro au lancement et augmente de un à chaque image. À trente images par seconde, une seconde correspond à trente unités.
>
> L’expression divise ce compteur par six, puis garde le reste de la division par deux. Le résultat vaut zéro pendant six images, puis un pendant six images, et ainsi de suite.
>
> La division entière ralentit l’alternance, le reste la ramène à deux valeurs. Aucune variable n’est nécessaire, et deux personnages animés resteraient synchronisés.

### 06:00 — Retourner le sprite

**À l’écran :** montrer l’image du joueur, puis la même retournée.

**Narration :**

> Inutile de dessiner un personnage tourné vers la gauche : la même image suffit, à condition de la retourner.
>
> `pyxel.blt()` accepte une largeur négative : Pyxel lit alors les pixels de droite à gauche. Le dessin occupe exactement le même rectangle, seule son orientation change.
>
> La direction est retenue pendant la lecture des touches. Le personnage garde donc son orientation quand on relâche la flèche.

**Action :** montrer une valeur positive, puis négative, en insistant sur le fait que la position `x` ne change pas.

### 07:20 — Un niveau plus large que l’écran

**À l’écran :** afficher la tilemap entière dans l’éditeur, avec un cadre matérialisant la fenêtre de 256 pixels.

**Narration :**

> Le niveau du fichier de ressources mesure soixante-quatre cases de large, soit cinq cent douze pixels : deux fois la fenêtre.
>
> Jusqu’à maintenant, le programme n’en dessinait que la moitié gauche. Les pièces de la seconde moitié n’étaient même pas cherchées : neuf pièces au lieu de dix-huit.
>
> La constante `LEVEL_WIDTH` passe donc de trente-deux à soixante-quatre. Elle sert au dessin du niveau, à la limite du joueur et au balayage des pièces.
>
> Attention à la différence de vocabulaire : les objets gardent leurs coordonnées du monde. La pièce de la seconde moitié est à `x = 456`, même lorsqu’elle est hors de l’écran.

### 08:40 — La caméra

**À l’écran :** écrire le calcul de `camera_x`, puis le tableau des quatre positions.

**Narration :**

> La caméra place le centre du joueur au centre de la fenêtre : la position du joueur, plus la moitié de sa largeur, moins la moitié de l’écran.
>
> `pyxel.clamp()` empêche ensuite la caméra de sortir du niveau : jamais avant zéro, jamais après deux cent cinquante-six.
>
> `pyxel.camera(x, y)` ne déplace aucun objet : elle décale le dessin. Tout ce qui est dessiné ensuite est translaté, ce qui simule un déplacement de la vue.
>
> Le calcul est refait à chaque image, dans `draw()` : la caméra suit le joueur image par image.

**Action :** montrer les valeurs 0, 0, 176 et 256 pour les positions 8, 100, 300 et 504.

### 10:20 — Revenir à l’écran et limiter le joueur

**À l’écran :** montrer `pyxel.camera()` seul après le dessin du joueur, puis la nouvelle limite du joueur.

**Narration :**

> La caméra s’applique à tout ce qui est dessiné ensuite, y compris les textes. Il faut donc la remettre à zéro juste après le joueur : appelée sans argument, `pyxel.camera()` rétablit un décalage nul. Le score et les messages restent collés aux bords de la fenêtre.
>
> Autre conséquence du niveau agrandi : le joueur était retenu par les bords de la fenêtre. Cette limite serait devenue un mur invisible au milieu du décor. Il est maintenant retenu par les bords du niveau : zéro à gauche, cinq cent quatre à droite.
>
> La collision avec la tilemap, elle, ne change pas.

### 11:20 — Exécuter et vérifier

**Action :** lancer le jeu et dérouler les vérifications.

**Narration :**

> Nous vérifions maintenant le comportement.
>
> Au démarrage, le joueur est au repos avec la première image, la caméra vaut zéro.
>
> En marchant, les deux images alternent environ cinq fois par seconde. Vers la gauche, le sprite est retourné et les pieds restent au même endroit. À l’arrêt, l’image de repos revient ; pendant un saut, c’est la seconde image du repos qui s’affiche.
>
> En avançant vers la droite, le décor défile et le joueur reste au centre. La caméra s’arrête à zéro au début du niveau et à deux cent cinquante-six à la fin ; le joueur s’arrête à cinq cent quatre.
>
> L’interface ne bouge pas pendant le défilement, et le compteur indique dix-huit pièces.

**Action :** pousser contre un mur pour montrer le retour à l’image de repos.

### 13:00 — Erreurs fréquentes

**À l’écran :** afficher la liste :

```text
interface qui défile   -> pyxel.camera() oublié avant les textes
caméra dans le vide    -> clamp() absent
joueur collé au bord   -> moitié de largeur oubliée
niveau coupé           -> LEVEL_WIDTH resté à 32
sprite décalé          -> x modifié avec la largeur négative
animation figée        -> choose_tile() appelée trop tôt
```

**Narration :**

> Six erreurs sont fréquentes.
>
> Sans remise à zéro, l’interface défile avec le décor et le score sort de l’écran.
>
> Sans `clamp()`, la caméra devient négative au début du niveau ou dépasse la fin : une bande de fond apparaît sur le bord.
>
> Utiliser la position du joueur sans ajouter la moitié de sa largeur le colle au bord gauche de l’écran.
>
> Oublier de passer `LEVEL_WIDTH` à soixante-quatre laisse une limite invisible au milieu du décor, et le programme ne trouve que neuf pièces.
>
> Décaler `x` en même temps que la largeur négative fait sauter le personnage d’une tuile à chaque changement de direction.
>
> Enfin, appeler `choose_tile()` avant la mise à jour de `dx` et de l’état au sol donne une animation en retard, ou figée.

**Action :** provoquer l’erreur de la caméra non remise à zéro, montrer l’interface qui sort de l’écran, puis rétablir.

### 15:00 — Expérimentations et conclusion

**À l’écran :** afficher la liste :

```text
- animation plus rapide
- trois images de marche
- animer l’ennemi
- afficher la valeur de la caméra
- caméra avec inertie
- défilement vertical
```

**Narration :**

> Plusieurs essais sont instructifs.
>
> Réduire `ANIMATION_SPEED` à trois accélère l’animation ; l’augmenter la ralentit.
>
> Ajouter une troisième image de marche ne suffit pas : l’index reste calculé avec un reste de division par deux. Il faut utiliser la longueur de la liste.
>
> Pour animer l’ennemi, dessinez un second dessin dans la banque d’images, puis alternez entre deux colonnes voisines.
>
> Afficher la valeur de la caméra aide à comprendre le défilement : elle vaut zéro dans la première moitié, puis augmente jusqu’à deux cent cinquante-six.
>
> Conserver la caméra dans un attribut et la rapprocher progressivement de sa cible donne un défilement plus doux, avec de l’inertie.
>
> Enfin, la caméra accepte deux valeurs : avec un niveau plus haut que l’écran, la même formule appliquée à `y` fait défiler le décor verticalement.
>
> Dans la prochaine leçon, le jeu reçoit son interface complète : écran titre, écran de fin, musique et compteur.

## Consignes de montage

- Montrer les quatre tuiles de la banque d’images avant de parler d’animation.
- Afficher en incrustation le tableau du compteur d’images au moment de l’expression.
- Comparer visuellement le sprite normal et le sprite retourné, en gardant le rectangle visible.
- Montrer la tilemap entière avec le cadre de la fenêtre avant d’introduire la caméra.
- Garder l’interface visible pendant toute la phase de défilement.
- Conserver le même code final que l’article `article.html`.

## Vérification avant publication

- Le code compile et s’exécute avec Pyxel 3.0.1.
- Les quatre tuiles du joueur sont utilisées : repos, saut, deux images de marche.
- Le sprite est retourné par une largeur négative, sans décalage de `x`.
- `LEVEL_WIDTH` vaut 64 et le niveau mesure 512 pixels de large.
- La caméra est limitée entre 0 et 256, et remise à zéro avant les textes.
- Le joueur est limité entre 0 et 504.
- Les dix-huit pièces et les trois ennemis sont présents.
- Les règles de la leçon 8 fonctionnent à l’identique.
- Le code affiché est identique à celui de l’article.
