# Leçon 11 — Préparer son jeu pour la Nuit du Code

## Fiche de production

- **Formation :** Créer un mini-platformer 2D avec Pyxel
- **Public :** débutants en création de jeux, élèves de Première et Terminale NSI
- **Environnement :** PyxelStudio dans Capytale
- **Version ciblée :** Pyxel 3.0.1
- **Durée cible :** 17 à 18 minutes
- **Fichiers du projet :** `main.py` et `res.pyxres`
- **Ressource utilisée :** `res.pyxres`, source unique des images, de la tilemap et des sons
- **Titre à l’écran :** Leçon 11 — Préparer son jeu pour la Nuit du Code

## Intention pédagogique

Cette dernière leçon ne change pas les règles du jeu. Elle prépare le rendu.

Le travail porte sur trois points :

- vérifier le jeu en jouant, avec une liste de quinze contrôles ;
- rendre le dossier autonome, en le copiant ailleurs puis en le relançant ;
- corriger deux fragilités qui gênent la personnalisation : les colonnes écrites à la main et les deux écrans de fin presque identiques.

Le message de la leçon est simple : un jeu livrable est un jeu qu’on a déplacé, renommé, relancé et terminé au moins une fois.

## Objectifs annoncés aux élèves

À la fin de la vidéo, l’élève doit pouvoir :

1. vérifier le fonctionnement complet du jeu ;
2. contrôler la présence des deux fichiers attendus ;
3. supprimer toute dépendance externe ;
4. vérifier le chargement de `res.pyxres` ;
5. équilibrer la difficulté ;
6. vérifier la condition de victoire et le redémarrage ;
7. personnaliser le niveau et les ressources.

## Préparation de l’enregistrement

### Fichiers

- `main.py` de la leçon 11, dans le dossier `11-nuit-du-code` ;
- `res.pyxres` recopié à côté de ce fichier ;
- un dossier vide, nommé par exemple `rendu`, pour la copie de vérification.

### Vérifications avant d’enregistrer

- Le jeu démarre sur l’écran titre, sans musique.
- La barre d’espace lance la partie et la musique.
- Le score et les pièces restantes restent fixes pendant le défilement.
- Les trois bruitages s’entendent.
- La victoire et la défaite sont atteignables, message centré.
- Une deuxième partie retrouve dix-huit pièces.
- Le dossier copié ailleurs fonctionne.
- La touche `Q` ferme le jeu dans tous les états.

### Code final

```python
import pyxel


SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
FONT_WIDTH = 4
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

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2
SCENE_WIN = 3


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
            TRANSPARENT_COLOR,
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
            title="Chapitre 11 - version finale",
        )

        self.scene = SCENE_TITLE
        self.score = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.scene == SCENE_TITLE:
            self.update_title()
        elif self.scene == SCENE_PLAY:
            self.update_play()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover()
        else:
            self.update_win()

    def draw(self):
        if self.scene == SCENE_TITLE:
            self.draw_title()
        elif self.scene == SCENE_PLAY:
            self.draw_play()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover()
        else:
            self.draw_win()

    def update_title(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.start_game()

    def update_play(self):
        self.player.update()

        for coin in self.coins:
            coin.update()

        for enemy in self.enemies:
            enemy.update()

        self.check_coins()

        if not self.coins:
            self.scene = SCENE_WIN
            pyxel.stop()
            return

        self.check_enemies()

    def update_gameover(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.scene = SCENE_TITLE

    def update_win(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.scene = SCENE_TITLE

    def draw_title(self):
        pyxel.cls(BACKGROUND_COLOR)

        lines = [
            ("MINI PLATFORMER", 96),
            ("Gauche et droite : marcher", 120),
            ("Espace : sauter", 136),
            ("Appuyez sur Espace", 160),
        ]

        for text, y in lines:
            pyxel.text(self.text_x(text), y, text, TEXT_COLOR)

    def draw_play(self):
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

        pyxel.text(4, 4, f"Score : {self.score}", TEXT_COLOR)
        pyxel.text(4, 12, f"Restantes : {len(self.coins)}", TEXT_COLOR)

    def draw_gameover(self):
        self.draw_play()
        self.draw_end("Partie perdue", pyxel.COLOR_RED)

    def draw_win(self):
        self.draw_play()
        self.draw_end("Victoire", pyxel.COLOR_YELLOW)

    def draw_end(self, message, color):
        pyxel.rect(48, 92, 160, 60, pyxel.COLOR_BLACK)

        score = f"Score : {self.score}"
        hint = "Espace : revenir au titre"

        pyxel.text(self.text_x(message), 104, message, color)
        pyxel.text(self.text_x(score), 116, score, TEXT_COLOR)
        pyxel.text(self.text_x(hint), 136, hint, TEXT_COLOR)

    def text_x(self, text):
        return (SCREEN_WIDTH - FONT_WIDTH * len(text)) // 2

    def start_game(self):
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
        self.scene = SCENE_PLAY

        pyxel.playm(MUSIC, loop=True)

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
                self.scene = SCENE_GAMEOVER
                pyxel.stop()
                pyxel.play(2, HIT_SOUND)


Game()
```

## Découpage détaillé

### 00:00 — Montrer le résultat

**À l’écran :** lancer le jeu. Écran titre, partie complète, victoire, retour au titre, nouvelle partie, défaite.

**Narration :**

> Voici le jeu à la fin de la formation. Il s’ouvre sur un écran titre, il se joue, il se gagne, il se perd, et il recommence autant de fois qu’on veut.
>
> Le jeu ne change pas dans cette leçon. Ce qui change, c’est ce qu’on en fait : le vérifier, le déplacer, et le préparer pour être modifié par quelqu’un d’autre, ou par soi-même dans une semaine.
>
> Le jour du rendu, un jeu qui ne démarre pas ne compte pas, quelle que soit la qualité du code.

**Action :** copier le dossier sous un autre nom, puis lancer le jeu depuis la copie.

### 00:50 — Présenter les objectifs

**À l’écran :** afficher les trois points :

```text
1. vérifier le jeu en jouant
2. rendre le dossier autonome
3. faciliter la personnalisation
```

**Narration :**

> Trois étapes.
>
> D’abord une liste de quinze contrôles, faits en jouant et non en relisant le code.
>
> Ensuite le dossier : deux fichiers, aucun autre, et une copie qui fonctionne ailleurs.
>
> Enfin deux retouches de code qui préparent la personnalisation : les colonnes de texte calculées, et un seul dessin pour les deux écrans de fin.

### 01:40 — La liste de vérification

**À l’écran :** jouer en cochant les points, affichés en incrustation au fur et à mesure.

**Narration :**

> Nous commençons par jouer, en cochant.
>
> Le jeu se lance sans erreur. Le dossier contient deux fichiers : `main.py` et `res.pyxres`.
>
> Le joueur se déplace, il saute, il ne traverse pas les plateformes. Les ennemis vont et viennent de façon visible. Les pièces se ramassent, le compteur descend, le score monte.
>
> Les bruitages sont associés aux événements : un son pour le saut, un pour la pièce, un pour la collision.
>
> La victoire s’obtient en ramassant les dix-huit pièces. La défaite arrive au contact d’un ennemi. Dans les deux cas, la musique s’arrête, et la barre d’espace ramène au titre.
>
> Une nouvelle partie retrouve dix-huit pièces et un score nul. C’est le contrôle le plus souvent oublié : beaucoup de jeux ne se jouent qu’une fois.

**Action :** enchaîner deux parties sans relancer le programme.

### 04:30 — Le dossier de deux fichiers

**À l’écran :** montrer le dossier, le copier sous un autre nom, lancer depuis la copie.

**Narration :**

> Le dossier du projet contient exactement deux fichiers.
>
> Le programme ne connaît que le nom `res.pyxres`, sans chemin. Il cherche donc le fichier dans le dossier courant. Le dossier peut être renommé, déplacé ou déposé dans Capytale, tant que les deux fichiers restent ensemble.
>
> La vérification décisive tient en une manipulation : copier le dossier ailleurs, le renommer, puis lancer le jeu depuis ce nouvel emplacement.
>
> Si le jeu fonctionne dans son dossier d’origine et échoue une fois copié, c’est qu’un fichier externe manque : un second fichier Python, une image, un son ou une police. Le dossier de rendu n’en contient aucun.

**Action :** montrer le message `Failed to open file 'res.pyxres'` en lançant depuis le mauvais dossier, puis revenir au bon.

### 06:00 — Une colonne calculée

**À l’écran :** écrire `FONT_WIDTH` puis `text_x()`.

```python
    def text_x(self, text):
        return (SCREEN_WIDTH - FONT_WIDTH * len(text)) // 2
```

**Narration :**

> La leçon 10 écrivait les colonnes à la main. Le résultat était juste, mais fragile : renommer « MINI PLATFORMER » décalait la ligne.
>
> La méthode `text_x()` refait le calcul à chaque dessin. Un caractère mesure quatre pixels de large : la méthode multiplie la longueur du texte par quatre, retire ce total à la largeur de l’écran, et divise par deux.
>
> Le centrage suit désormais le texte. Sur l’écran de fin, le score reste au milieu du cadre avec un comme avec deux chiffres.
>
> Les appels deviennent plus courts : `self.text_x("Victoire")` remplace une colonne écrite en dur.

### 08:00 — L’écran titre en une liste

**À l’écran :** remplacer les quatre appels par la liste et la boucle.

```python
        lines = [
            ("MINI PLATFORMER", 96),
            ("Gauche et droite : marcher", 120),
            ("Espace : sauter", 136),
            ("Appuyez sur Espace", 160),
        ]

        for text, y in lines:
            pyxel.text(self.text_x(text), y, text, TEXT_COLOR)
```

**Narration :**

> Chaque ligne de l’écran titre est un couple : le texte, puis sa hauteur.
>
> La boucle dessine les quatre lignes de la même façon. Pour ajouter un titre, un sous-titre ou un crédit, il suffit d’un couple de plus dans la liste.
>
> Nous avons déjà parcouru des couples : c’est le même geste que pour les positions des pièces, avec `for x, y in self.level.take_coins()`.

### 09:30 — Un seul dessin de fin

**À l’écran :** remplacer les deux méthodes par `draw_gameover()`, `draw_win()` et `draw_end()`.

**Narration :**

> Les deux écrans de fin ne différaient que par deux valeurs : le message et sa couleur. Elles deviennent les paramètres de `draw_end()`.
>
> L’intérêt n’est pas d’écrire moins de lignes, mais de n’avoir qu’un endroit à modifier. Changer la taille du cadre, déplacer le score ou reformuler la consigne se fait une fois, et les deux écrans suivent.
>
> C’est la même idée que la méthode `draw_play()` réutilisée par les deux fins : un seul dessin de décor, un seul dessin de message.

### 10:40 — Le bruitage de la défaite

**À l’écran :** montrer `check_enemies()` et commenter l’ordre des appels.

```python
                self.scene = SCENE_GAMEOVER
                pyxel.stop()
                pyxel.play(2, HIT_SOUND)
```

**Narration :**

> À la défaite, l’ordre compte. `pyxel.stop()` coupe tous les canaux, y compris celui du bruitage. Le son est donc joué après l’arrêt de la musique, sinon il serait interrompu dans la même image.
>
> Le canal deux reste libre : la musique occupe les canaux zéro et un, le saut le canal zéro, la pièce le canal un.

**Action :** jouer une défaite, montrer le son entendu malgré l’arrêt de la musique.

### 11:40 — Équilibrer la difficulté

**À l’écran :** le tableau des quatre constantes.

```text
PLAYER_SPEED = 2
JUMP_SPEED = -11
GRAVITY = 1
ENEMY_SPEED = 1
```

**Narration :**

> Quatre constantes règlent la difficulté.
>
> La vitesse du joueur décide de la traversée du niveau. La vitesse de saut et la gravité décident de la hauteur atteinte. La vitesse des ennemis décide de la difficulté à les éviter.
>
> Le saut et la gravité se touchent. Avec moins onze, le joueur monte d’environ cinquante-cinq pixels. Avec moins neuf, il ne monte plus que de trente-six : la première rangée de plateformes, à quarante pixels au-dessus du sol, devient inaccessible.
>
> Après chaque changement, une partie complète jusqu’à la dernière pièce. C’est le seul juge.

### 13:20 — Personnaliser le jeu

**À l’écran :** afficher le tableau des dix idées et de leur point d’intervention.

```text
niveau, plateforme, ennemi, pièce spéciale
vies, compte à rebours, zone secrète
bonus temporaire, animation, ambiance sonore
```

**Narration :**

> Le jeu de référence n’est pas un modèle à livrer tel quel : il sert de point de départ.
>
> Chaque idée a son point d’intervention. Le niveau et les plateformes passent par la tilemap, ou par `pset()` comme dans la leçon sept. Un ennemi de plus est une ligne dans la liste de `start_game()`. Une pièce spéciale est une classe sur le modèle de `Coin`. Des vies tiennent dans un attribut, testé dans `check_enemies()`. Un compte à rebours s’appuie sur `pyxel.frame_count` divisé par trente. Un bonus temporaire est un attribut de `Player`. Une nouvelle animation demande des tuiles et une ligne dans `choose_tile()`. L’ambiance sonore se règle dans les éditeurs de sons et de musiques.
>
> La recommandation est la même pour tous : deux extensions menées jusqu’au bout valent mieux que dix idées à moitié faites. Une modification terminée se voit en jouant ; une modification inachevée se voit au mauvais moment.

### 15:30 — Erreurs fréquentes

**À l’écran :** afficher la liste :

```text
Failed to open file 'res.pyxres' -> mauvais dossier
jeu qui marche copié -> fichier externe oublié
texte décalé -> colonne écrite à la main
bruitage muet -> son joué avant pyxel.stop()
accents manquants -> police ASCII
deuxième partie vide -> pyxel.load() absent
```

**Narration :**

> Six erreurs reviennent au moment du rendu.
>
> Le message « Failed to open file » signifie que le programme est lancé depuis un autre dossier, ou que le fichier a été renommé.
>
> Un jeu qui marche dans son dossier et échoue une fois copié traîne une dépendance externe.
>
> Un texte décalé vient d’une colonne écrite à la main.
>
> Un bruitage muet est un son joué avant l’arrêt de la musique.
>
> Un accent manquant vient de la police intégrée, qui ne contient que l’ASCII.
>
> Une deuxième partie vide vient d’un `pyxel.load()` oublié au début de `start_game()`.

### 16:40 — Conclusion de la formation

**À l’écran :** revenir au jeu, puis afficher le sommaire des onze leçons.

**Narration :**

> La formation s’arrête ici pour le jeu 2D. Vous savez maintenant afficher une fenêtre, charger une ressource, déplacer un joueur, gérer un décor, des objets, des règles, une caméra, des états et du son.
>
> Le module bonus ouvre la troisième dimension avec Pyxel Cube : une scène, un objet, une caméra, et un petit jeu pour finir.
>
> Avant de vous lancer, deux réflexes : garder une copie du jeu de référence, et vérifier le dossier en le copiant ailleurs. Le reste est une question d’idées.

## Consignes de montage

- Jouer une partie complète avant toute explication de code.
- Afficher la liste de vérification en incrustation, point par point, pendant la partie.
- Montrer la copie du dossier et le lancement depuis la copie, sans coupure.
- Montrer une fois le message d’erreur du fichier de ressources manquant.
- Afficher `text_x()` puis, en comparaison, les colonnes écrites à la main de la leçon 10.
- Afficher les deux écrans de fin côte à côte pour montrer le code commun.
- Garder le tableau des quatre constantes visible pendant l’explication de la difficulté.
- Conserver le même code final que l’article `article.qmd`.

## Vérification avant publication

- Le code compile et s’exécute avec Pyxel 3.0.1.
- Le dossier ne contient que `main.py` et `res.pyxres`.
- Le jeu lancé depuis une copie du dossier fonctionne.
- Les textes restent centrés, y compris le score final à deux chiffres.
- Les deux écrans de fin passent par `draw_end()`.
- Le bruitage de défaite est audible après l’arrêt de la musique.
- Les textes dessinés par `pyxel.text()` ne contiennent pas d’accent.
- Une deuxième partie retrouve dix-huit pièces.
- Le code affiché est identique à celui de l’article.
