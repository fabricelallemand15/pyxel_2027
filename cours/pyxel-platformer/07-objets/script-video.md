# Leçon 7 — Ajouter plusieurs types d’objets

## Fiche de production

- **Formation :** Créer un mini-platformer 2D avec Pyxel
- **Public :** débutants en création de jeux, élèves de Première et Terminale NSI
- **Environnement :** PyxelStudio dans Capytale
- **Version ciblée :** Pyxel 3.0.1
- **Durée cible :** 16 à 18 minutes
- **Fichiers du projet :** `main.py` et `res.pyxres`
- **Ressource utilisée :** `res.pyxres`, avec la nouvelle tuile d’ennemi `(4, 0)`
- **Titre à l’écran :** Leçon 7 — Ajouter plusieurs types d’objets

## Intention pédagogique

Cette leçon fait entrer les objets du jeu dans le programme.

Le travail porte sur cinq points :

- une classe par type d’objet, avec `update()` et `draw()` ;
- plusieurs instances d’une même classe ;
- une liste pour les ranger ;
- des boucles pour les mettre à jour et les dessiner ;
- la lecture de la tilemap comme source de données.

Les neuf pièces du niveau sont déjà dessinées dans la tilemap. Le programme les retire du décor et les remplace par des objets : une tuile ne peut pas être ramassée, un objet le pourra.

Deux ennemis font les cent pas, sans encore réagir au joueur.

## Objectifs annoncés aux élèves

À la fin de la vidéo, l’élève doit pouvoir :

1. écrire une classe qui décrit un objet du jeu ;
2. créer plusieurs instances de cette classe ;
3. lire une tilemap pour placer des objets ;
4. ranger des objets dans une liste ;
5. appeler `update()` et `draw()` sur chaque objet ;
6. distinguer le décor, fait de tuiles, des objets, faits d’instances.

## Préparation de l’enregistrement

### Fichiers

- `main.py` de la leçon 7, dans le dossier `07-objets` ;
- `res.pyxres` recopié à côté de ce fichier ; il contient la tuile d’ennemi.

### Vérifications avant d’enregistrer

- L’affichage indique `Restantes : 9  Ennemis : 2` au démarrage.
- Les neuf pièces sont posées sur les trois plateformes, à la place des tuiles du décor.
- Aucune pièce n’est dessinée par la tilemap.
- L’ennemi du sol va et vient entre 88 et 160.
- L’ennemi de la plateforme reste sur la ligne 19.
- Le joueur se déplace, saute et s’arrête sur le décor comme dans la leçon 6.
- Rien ne se passe au contact d’une pièce ou d’un ennemi.

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


class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE

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
            title="Chapitre 7 - plusieurs objets",
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

        pyxel.playm(MUSIC, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.player.update()

        for coin in self.coins:
            coin.update()

        for enemy in self.enemies:
            enemy.update()

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
            "Chapitre 7 - plusieurs objets",
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
            f"Restantes : {len(self.coins)}  Ennemis : {len(self.enemies)}",
            TEXT_COLOR,
        )


Game()
```

## Découpage détaillé

### 00:00 — Montrer le résultat

**À l’écran :** lancer le jeu. Le joueur se déplace. Neuf pièces surplombent les plateformes, deux ennemis circulent, le compteur affiche neuf et deux.

**Narration :**

> Dans cette septième leçon, le niveau se peuple.
>
> Neuf pièces sont posées sur les trois plateformes, et deux ennemis font les cent pas : l’un sur le sol, l’autre sur la plateforme du milieu.
>
> L’affichage indique le nombre d’objets présents. Le joueur se déplace et saute exactement comme dans la leçon précédente.
>
> Rien ne se passe encore lorsqu’il touche une pièce ou un ennemi. Cette leçon installe les objets ; la suivante leur donnera des règles.

**Action :** traverser le niveau, frôler une pièce et un ennemi, puis montrer les deux ennemis qui rebondissent sur leurs bornes.

### 00:50 — Présenter les objectifs

**À l’écran :** afficher les quatre points :

```text
1. une classe par type d’objet
2. des instances dans une liste
3. deux boucles : update() et draw()
4. les pièces viennent de la tilemap
```

**Narration :**

> Quatre étapes structurent cette leçon.
>
> Une classe décrit un type d’objet : ici la pièce et l’ennemi. Plusieurs instances de ces classes sont créées, puis rangées dans des listes. Deux boucles appellent `update()` et `draw()` sur chaque objet. Enfin, les pièces ne sont pas placées à la main : elles sont lues dans la tilemap du niveau.

### 01:40 — Une classe pour la pièce

**À l’écran :** écrire la classe `Coin` avec ses quatre attributs, puis montrer trois instances côte à côte.

**Narration :**

> Une pièce se décrit par quatre nombres : sa position et sa taille.
>
> La classe `Coin` les range dans un objet, et y ajoute deux méthodes. `draw()` affiche la tuile de la pièce. `update()` ne fait rien, et c’est volontaire : une pièce ne se déplace pas.
>
> La méthode existe quand même, pour que tous les objets du jeu se manipulent de la même façon. Le jour où une pièce doit clignoter, il suffira de remplir cette méthode.
>
> La largeur et la hauteur ne sont pas des paramètres : une pièce occupe toujours une tuile, donc `TILE_SIZE` suffit.

### 03:00 — Du décor à l’objet

**À l’écran :** afficher la tilemap dans l’éditeur, encadrer les neuf cases de pièce, puis montrer le même écran après l’appel à `take_coins()`.

**Narration :**

> Les neuf pièces sont déjà dessinées dans la tilemap. Une tuile, pourtant, ne peut pas être ramassée : c’est une case du décor, pas un objet.
>
> La méthode `take_coins()` de la classe `Level` fait la conversion. Elle parcourt la tilemap, repère les tuiles de pièce, les remplace par une tuile transparente et note leurs positions en pixels.
>
> L’effacement est indispensable. Sans lui, chaque pièce existerait deux fois : la tuile du décor et l’objet posé dessus. Les deux se ressemblent, mais seule la seconde pourra disparaître.
>
> Attention, l’effacement a lieu en mémoire : le fichier `res.pyxres` n’est pas modifié, et relancer le programme recharge les pièces du décor.

### 05:00 — Le parcours de la tilemap

**À l’écran :** afficher la double boucle et le tableau des positions obtenues.

**Narration :**

> Deux boucles imbriquées parcourent le niveau : les lignes de haut en bas, puis les colonnes de gauche à droite. Trente-deux fois trente-deux, soit mille vingt-quatre lectures.
>
> Pour chaque case lue, le programme compare son contenu à `COIN_TILE`, la tuile de la pièce. S’il y a correspondance, `pset()` remplace la case, et `append()` ajoute la position en pixels.
>
> La position se calcule avec `TILE_SIZE` : la ligne 22 donne 176 pixels de haut, la colonne 5 donne 40 pixels de large.
>
> L’ordre de la liste suit l’ordre de lecture : les pièces de la plateforme haute arrivent en premier, puis celles du milieu, puis celles du bas.

### 06:20 — Construire la liste des pièces

**À l’écran :** écrire les trois lignes dans `Game.__init__()`.

**Narration :**

> La classe `Game` récupère ces positions et construit la liste des pièces.
>
> La liste démarre vide, puis chaque couple de coordonnées devient un objet `Coin`. La liste ne contient pas des nombres : elle contient des objets, chacun avec sa position et ses méthodes.
>
> Cette construction a lieu une seule fois, dans `__init__()`. La placer dans `update()` ou dans `draw()` recréerait neuf pièces soixante fois par seconde.

### 07:20 — Les ennemis

**À l’écran :** écrire la classe `Enemy`, puis la liste des deux ennemis.

**Narration :**

> Les ennemis ne viennent pas du décor : ils sont posés à la main, comme le joueur. Onze lignes suffisent.
>
> La classe `Enemy` reprend la position et la taille, et ajoute une vitesse et deux bornes. À chaque image, l’ennemi avance de `dx`. En atteignant une borne, il est replacé dessus et repart dans l’autre sens.
>
> Les bornes de l’ennemi posé sur la plateforme sont choisies à l’intérieur de la plateforme, pour qu’il ne marche pas dans le vide. Un ennemi n’utilise pas encore `collide()` : c’est un choix de simplicité, et la leçon suivante n’en a pas besoin.
>
> La position verticale suit la règle habituelle : la plateforme occupe la ligne 19, son dessus est à 152, donc l’ennemi est posé à 144.

### 09:00 — Les boucles de mise à jour et de dessin

**À l’écran :** écrire les quatre boucles, dans `update()` puis dans `draw()`.

**Narration :**

> Le jeu n’appelle plus chaque objet par son nom : il parcourt les listes.
>
> Une première boucle met à jour les pièces, une deuxième les ennemis. Les mêmes boucles appellent le dessin, dans l’ordre d’empilement voulu.
>
> La variable de boucle change de nom à chaque tour : `coin` désigne successivement chacun des neuf objets. C’est le même mécanisme que pour parcourir une liste de nombres.
>
> L’intérêt apparaît tout de suite : ajouter une dixième pièce ne demande aucune ligne de plus dans `update()` ni dans `draw()`.

### 10:20 — L’ordre du dessin

**À l’écran :** montrer la méthode `draw()` en surlignant les couches.

**Narration :**

> Ce qui est dessiné en dernier recouvre le reste.
>
> Le fond d’abord, puis le niveau et sa tilemap, ensuite les pièces, les ennemis et le joueur. Les textes arrivent en dernier : ils restent lisibles au-dessus du décor.
>
> Le joueur passe ainsi devant une pièce qu’il frôle. Un ennemi, en revanche, masque une pièce pendant un instant : il est dessiné après elle.

### 11:00 — Exécuter et vérifier

**Action :** lancer le jeu et dérouler les vérifications.

**Narration :**

> Nous vérifions maintenant le comportement.
>
> Au démarrage, le compteur indique neuf pièces et deux ennemis. Les pièces occupent exactement les cases où le décor les dessinait : la tuile a été remplacée par un objet, et le niveau paraît identique.
>
> L’ennemi du sol va et vient entre 88 et 160. Celui de la plateforme reste sur sa ligne, entre 104 et 160 : il ne tombe pas et ne quitte pas la plateforme.
>
> Le joueur se déplace, saute et s’arrête sur le décor comme dans la leçon précédente : les collisions n’ont pas changé.
>
> En frôlant une pièce, il ne se passe rien. En touchant un ennemi, rien non plus.

### 12:40 — Erreurs fréquentes

**À l’écran :** afficher la liste :

```text
objets recréés à chaque image -> listes construites dans update()
tuiles non effacées          -> pset() oublié dans take_coins()
ennemis immobiles            -> boucles update() absentes
tuiles passées à blt()       -> oubli de la multiplication par TILE_SIZE
liste modifiée pendant le parcours -> remove() dans la boucle
```

**Narration :**

> Cinq erreurs sont fréquentes.
>
> Construire les listes dans `update()` ou dans `draw()` recrée les objets à chaque image : les ennemis repartent de leur position initiale.
>
> Oublier `pset()` laisse la tuile sous l’objet : la pièce semblera réapparaître après avoir été ramassée.
>
> Écrire les listes sans les boucles d’appel donne des ennemis immobiles.
>
> Passer `COIN_TILE` directement à `blt()` affiche une zone de la banque d’images, pas la pièce : `blt()` attend des pixels.
>
> Enfin, retirer un élément d’une liste dans la boucle qui la parcourt fait sauter l’élément suivant. La leçon suivante montre la bonne méthode.

**Action :** provoquer l’erreur du `pset()` oublié, montrer une pièce fantôme, puis rétablir.

### 14:40 — Expérimentations et conclusion

**À l’écran :** afficher la liste :

```text
- ajouter une pièce avec pset()
- ajouter un troisième ennemi
- augmenter la vitesse des ennemis
- faire clignoter les pièces
- afficher len(self.coins)
```

**Narration :**

> Plusieurs essais sont instructifs.
>
> Ajouter une tuile de pièce dans la tilemap, ou l’écrire avec `pset()`, fait apparaître une dixième pièce sans modifier une ligne du jeu.
>
> Un troisième ennemi sur la plateforme haute patrouille à la verticale 112 : la plateforme occupe la ligne 15, son dessus est à 120.
>
> Doubler la vitesse rend les allées et retours plus vifs. Au-delà d’une tuile par image, les bornes doivent être testées avec `<` et `>`, ce que le code fait déjà.
>
> Remplir la méthode `update()` de `Coin` permet de faire clignoter les pièces : l’interface commune sert enfin à quelque chose.
>
> `len()` donne le nombre d’éléments d’une liste. Ce compteur suivra automatiquement les pièces ramassées.
>
> Dans la prochaine leçon, le jeu gagne ses règles : ramasser une pièce, marquer des points, perdre au contact d’un ennemi et retirer proprement les objets des listes.

## Consignes de montage

- Montrer la tilemap avec les neuf cases de pièce avant d’expliquer `take_coins()`.
- Afficher en incrustation le tableau case vers pixels pour deux ou trois pièces.
- Faire apparaître la différence entre une tuile du décor et un objet au moment de l’effacement.
- Garder le compteur d’objets visible pendant toute la phase de vérification.
- Conserver le même code final que l’article `article.qmd`.

## Vérification avant publication

- Le code compile et s’exécute avec Pyxel 3.0.1.
- `res.pyxres` contient la tuile d’ennemi `(4, 0)` et reste identique dans tous les dossiers de leçon.
- Les neuf pièces sont créées aux positions attendues, et aucune tuile de pièce ne subsiste dans la tilemap.
- Les deux ennemis restent dans leurs bornes et ne quittent pas leur support.
- Les boucles appellent `update()` et `draw()` sur chaque objet.
- Le joueur se comporte comme dans la leçon 6.
- Le code affiché est identique à celui de l’article.
