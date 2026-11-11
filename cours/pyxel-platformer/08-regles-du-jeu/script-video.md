# Leçon 8 — Règles du jeu et cycle de vie des objets

## Fiche de production

- **Formation :** Créer un mini-platformer 2D avec Pyxel
- **Public :** débutants en création de jeux, élèves de Première et Terminale NSI
- **Environnement :** PyxelStudio dans Capytale
- **Version ciblée :** Pyxel 3.0.1
- **Durée cible :** 16 à 18 minutes
- **Fichiers du projet :** `main.py` et `res.pyxres`
- **Ressource utilisée :** `res.pyxres`, inchangée
- **Titre à l’écran :** Leçon 8 — Règles du jeu et cycle de vie des objets

## Intention pédagogique

Cette leçon donne des règles au jeu.

Le travail porte sur cinq points :

- le recouvrement de deux rectangles ;
- une méthode qui compare deux objets ;
- le score et le bruitage au contact d’une pièce ;
- le marquage `is_alive` et la reconstruction de la liste ;
- l’arrêt du jeu au contact d’un ennemi.

La distinction est importante : `move_player()` corrige un déplacement contre le décor, `collide()` détecte un contact entre deux objets. Les deux portent le même nom dans le langage courant, pas dans le code.

## Objectifs annoncés aux élèves

À la fin de la vidéo, l’élève doit pouvoir :

1. tester le recouvrement de deux rectangles ;
2. déclencher une action au contact ;
3. compter des points dans un attribut ;
4. marquer un objet mort avec `is_alive` ;
5. reconstruire une liste pour retirer les objets morts ;
6. arrêter le jeu avec un indicateur d’état.

## Préparation de l’enregistrement

### Fichiers

- `main.py` de la leçon 8, dans le dossier `08-regles-du-jeu` ;
- `res.pyxres` recopié à côté de ce fichier.

### Vérifications avant d’enregistrer

- L’affichage indique `Score : 0  Pièces : 9` au démarrage.
- Toucher une pièce la fait disparaître, augmente le score et joue le bruitage.
- Repasser au même endroit ne rapporte plus rien.
- Toucher un ennemi affiche `Partie perdue` et fige le jeu.
- Les flèches n’ont plus d’effet après la défaite, la touche `Q` fonctionne toujours.
- Les bords jointifs ne déclenchent aucun contact.

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
            title="Leçon 8 - règles du jeu",
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
            "Leçon 8 - règles du jeu",
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

**À l’écran :** lancer le jeu. Ramasser deux ou trois pièces, montrer le score qui monte, puis se laisser toucher par l’ennemi du sol.

**Narration :**

> Dans cette huitième leçon, le jeu reçoit ses règles.
>
> En touchant une pièce, le joueur la fait disparaître, marque un point et déclenche un bruit aigu. Le compteur se met à jour immédiatement.
>
> En touchant un ennemi, la partie s’arrête : le décor se fige et le message « Partie perdue » s’affiche avec le score final.
>
> Deux règles, deux comportements différents, et une même question à résoudre : comment savoir que deux objets se touchent ?

**Action :** montrer aussi qu’une pièce déjà ramassée ne rapporte plus rien en repassant dessus.

### 00:55 — Présenter les objectifs

**À l’écran :** afficher les quatre points :

```text
1. deux rectangles se recouvrent-ils ?
2. marquer un objet mort : is_alive
3. reconstruire la liste
4. arrêter le jeu : is_game_over
```

**Narration :**

> Quatre étapes structurent la leçon.
>
> D’abord la règle géométrique du contact. Ensuite la pièce ramassée, marquée comme morte avant d’être retirée de sa liste. Puis l’arrêt du jeu, décrit par un simple attribut.
>
> Le décor, lui, ne change pas : les collisions de la leçon 6 continuent de gérer les déplacements.

### 01:40 — Deux rectangles se recouvrent-ils ?

**À l’écran :** afficher deux rectangles à l’écran, les faire glisser l’un vers l’autre, puis écrire la méthode.

**Narration :**

> Un contact ne se calcule pas sur les dessins : il se calcule sur les rectangles. Chaque objet possède déjà `x`, `y`, `width` et `height`.
>
> Deux rectangles se recouvrent si quatre conditions sont vraies en même temps : le bord gauche de l’un est à gauche du bord droit de l’autre, et réciproquement. Deux conditions pour l’axe horizontal, deux pour l’axe vertical.
>
> Les inégalités sont strictes. Deux objets dont les bords se touchent exactement ne se recouvrent pas. C’est voulu : sinon, un joueur posé juste à côté d’une pièce la ramasserait.

**Action :** montrer un cas de recouvrement, un cas de bord jointif, puis un cas où les rectangles sont séparés verticalement.

### 03:40 — Une méthode pour comparer deux objets

**À l’écran :** écrire `collide(self, a, b)` dans la classe `Game`.

**Narration :**

> La méthode s’appelle `collide`, prend deux objets et renvoie vrai ou faux. Elle ne connaît ni les joueurs ni les pièces : elle lit quatre attributs, et c’est tout.
>
> C’est ce qui permet de l’utiliser partout : `self.collide(self.player, coin)` pour une pièce, `self.collide(self.player, enemy)` pour un ennemi. La même méthode, deux usages.
>
> Elle n’a pas besoin d’être une classe : ce n’est pas un élément du jeu, seulement une opération géométrique. Une méthode de `Game` suffit, et c’est là que les règles du jeu sont décidées.

### 05:00 — Ramasser une pièce

**À l’écran :** écrire `check_coins()`.

**Narration :**

> La méthode `check_coins()` parcourt la liste des pièces et teste chacune d’elles.
>
> Au contact, trois actions s’enchaînent : la pièce est marquée comme morte avec `is_alive`, le score augmente d’un point, et le bruitage de la pièce se déclenche sur le canal 1.
>
> La boucle continue sur les pièces suivantes. Si le joueur chevauche deux pièces à la fois, les deux sont ramassées dans la même image.

### 06:30 — Le cycle de vie d’un objet

**À l’écran :** afficher le tableau des quatre étapes : création, vie, mort, disparition.

**Narration :**

> Une pièce suit un cycle de vie.
>
> Elle est créée dans `__init__()`, avec `is_alive` à vrai. Elle vit : elle est mise à jour et dessinée à chaque image. Au contact, elle meurt : `is_alive` passe à faux. Enfin, elle disparaît de la liste.
>
> Pourquoi ne pas la retirer immédiatement ? Parce qu’on est en train de parcourir cette liste. Retirer un élément pendant le parcours décale les suivants, et certaines pièces ne seraient jamais testées.
>
> D’où la règle : on marque pendant le parcours, on nettoie après.

### 08:00 — Reconstruire la liste

**À l’écran :** écrire la ligne de nettoyage, puis sa version en boucle classique.

**Narration :**

> La dernière ligne de `check_coins()` reconstruit la liste en ne gardant que les pièces vivantes.
>
> La première écriture est une compréhension de liste. Elle se lit de gauche à droite : une nouvelle liste de `coin`, pour chaque `coin` de l’ancienne liste, si `coin.is_alive` est vrai.
>
> La seconde écriture fait exactement la même chose avec une boucle et `append()`. Elle est plus longue, mais elle montre les étapes. Utilisez celle que vous lisez le plus facilement.
>
> Une pièce morte n’est plus dans la liste : elle n’est plus dessinée, plus mise à jour. Le programme n’a rien d’autre à faire.

### 09:30 — La défaite

**À l’écran :** écrire `check_enemies()`, puis les deux lignes ajoutées au début de `update()`.

**Narration :**

> Le contact avec un ennemi ne retire aucun objet : il change l’état du jeu. L’attribut `is_game_over` passe à vrai, et le bruitage de collision se joue sur le canal 2.
>
> Pour arrêter la partie, `update()` commence par consulter cet attribut. S’il est vrai, `return` quitte la méthode immédiatement : le joueur, les pièces et les ennemis cessent d’être mis à jour.
>
> Le dessin continue, mais l’image ne bouge plus. La touche `Q` est testée avant, elle fonctionne donc toujours.

**Action :** montrer que les flèches n’ont plus d’effet après la défaite, et que les ennemis restent immobiles.

### 11:00 — L’écran de défaite

**À l’écran :** écrire le bloc d’affichage à la fin de `draw()`.

**Narration :**

> Trois lignes suffisent : un rectangle noir pour isoler le message, puis deux textes.
>
> Un caractère mesure quatre pixels de large. « Partie perdue » en compte treize, soit cinquante-deux pixels : le texte commence donc à la colonne 102 pour être centré dans une fenêtre de 256.
>
> Ce bloc est à la fin de `draw()` : il recouvre le décor, les ennemis et le joueur.

### 12:00 — Exécuter et vérifier

**Action :** lancer le jeu et dérouler les vérifications.

**Narration :**

> Nous vérifions maintenant le comportement.
>
> Au démarrage, le compteur indique zéro point et neuf pièces. En touchant une pièce, le score passe à un et il reste huit pièces ; le bruitage se fait entendre.
>
> En repassant au même endroit, rien ne se passe : la pièce n’existe plus.
>
> Les pièces de la plateforme du milieu sont gardées par un ennemi. Pour les prendre, il faut observer son trajet et sauter par-dessus : c’est le premier vrai défi du jeu.
>
> Au contact d’un ennemi, tout s’arrête, le message s’affiche avec le score final. Les flèches ne répondent plus, les ennemis sont figés, la touche `Q` ferme toujours l’application.

### 13:40 — Erreurs fréquentes

**À l’écran :** afficher la liste :

```text
score qui grimpe  -> liste non reconstruite
contact trop large -> inégalités non strictes
partie qui continue -> return manquant dans update()
mauvais collide()  -> décor au lieu des objets
un seul ennemi testé -> vérification hors boucle
```

**Narration :**

> Cinq erreurs sont fréquentes.
>
> Sans reconstruction de liste, la pièce reste présente et le score augmente à chaque image tant que le joueur la chevauche.
>
> Remplacer les inégalités strictes par des inégalités larges déclare un contact dès que les bords se touchent : le joueur ramasse les pièces au-dessus de sa tête.
>
> Sans le `return`, l’écran de défaite s’affiche mais la partie continue derrière.
>
> Utiliser la collision du décor, `move_player()`, au lieu de `collide()` ne produit aucun effet : elle corrige un déplacement, elle ne détecte pas un contact.
>
> Enfin, une vérification écrite hors de la boucle ne teste que le premier ennemi de la liste.

**Action :** provoquer l’erreur des inégalités larges, montrer une pièce ramassée à distance, puis rétablir.

### 15:40 — Expérimentations et conclusion

**À l’écran :** afficher la liste :

```text
- trois vies
- une pièce qui vaut cinq points
- gagner quand toutes les pièces sont prises
- recharger les ressources pour recommencer
- une invulnérabilité temporaire
```

**Narration :**

> Plusieurs essais sont instructifs.
>
> Un compteur de vies remplace la défaite immédiate : le joueur est replacé au départ et la partie ne s’arrête qu’à la troisième rencontre.
>
> Une pièce peut valoir cinq points, ou porter sa propre valeur dans un attribut.
>
> Tester si la liste des pièces est vide permet de gagner : il faut alors distinguer victoire et défaite, avec deux attributs ou un message différent.
>
> Pour recommencer, il faut recharger les ressources, puisque les tuiles de pièce ont été effacées du décor. C’est le sujet des états du jeu, traité plus loin.
>
> Enfin, `pyxel.frame_count` sert d’horloge pour une invulnérabilité temporaire après un contact.
>
> Dans la prochaine leçon, le personnage s’anime avec ses quatre images, et la caméra suit le joueur.

## Consignes de montage

- Montrer deux rectangles qui se rapprochent avant d’écrire la formule.
- Afficher en incrustation le tableau des quatre comparaisons au moment de la méthode.
- Montrer explicitement le cas des bords jointifs, qui ne déclenche rien.
- Garder le compteur visible pendant toute la phase de vérification.
- Conserver le même code final que l’article `article.html`.

## Vérification avant publication

- Le code compile et s’exécute avec Pyxel 3.0.1.
- Les inégalités de `collide()` sont strictes.
- Une pièce ramassée quitte la liste et ne rapporte qu’un point.
- Les sons utilisent les canaux 0, 1 et 2.
- Après la défaite, `update()` sort immédiatement et la touche `Q` reste active.
- Le message de défaite est centré et lisible sur le décor.
- Les collisions du décor sont inchangées depuis la leçon 6.
- Le code affiché est identique à celui de l’article.
