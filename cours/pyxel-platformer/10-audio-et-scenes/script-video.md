# Leçon 10 — Audio, interface et états du jeu

## Fiche de production

- **Formation :** Créer un mini-platformer 2D avec Pyxel
- **Public :** débutants en création de jeux, élèves de Première et Terminale NSI
- **Environnement :** PyxelStudio dans Capytale
- **Version ciblée :** Pyxel 3.0.1
- **Durée cible :** 16 à 18 minutes
- **Fichiers du projet :** `main.py` et `res.pyxres`
- **Ressource utilisée :** `res.pyxres`, rechargée à chaque partie
- **Titre à l’écran :** Leçon 10 — Audio, interface et états du jeu

## Intention pédagogique

Cette leçon organise le jeu en états.

Le travail porte sur cinq points :

- quatre constantes d’état : titre, jeu, défaite, victoire ;
- un aiguillage dans `update()` et dans `draw()` ;
- une construction de partie au bon moment, dans `start_game()` ;
- un rechargement des ressources, indispensable pour recommencer ;
- une musique lancée et arrêtée avec la partie.

Le point le plus important est le rechargement : depuis la leçon 7, les tuiles de pièce sont effacées du décor à la première partie. Sans `pyxel.load()`, la deuxième partie serait vide.

## Objectifs annoncés aux élèves

À la fin de la vidéo, l’élève doit pouvoir :

1. décrire l’état d’un jeu par une constante ;
2. aiguiller `update()` et `draw()` selon cet état ;
3. construire une partie seulement quand elle commence ;
4. recharger les ressources pour recommencer ;
5. lancer puis arrêter la musique au bon moment ;
6. centrer un texte dans la fenêtre.

## Préparation de l’enregistrement

### Fichiers

- `main.py` de la leçon 10, dans le dossier `10-audio-et-scenes` ;
- `res.pyxres` recopié à côté de ce fichier.

### Vérifications avant d’enregistrer

- Le jeu s’ouvre sur l’écran titre, sans musique, sur fond bleu nuit.
- La barre d’espace lance la partie et la musique.
- Score et pièces restantes sont affichés en haut à gauche.
- La victoire s’affiche quand les dix-huit pièces sont ramassées.
- La défaite s’affiche au contact d’un ennemi.
- La musique s’arrête dans les deux cas.
- La barre d’espace ramène au titre, puis une nouvelle partie retrouve dix-huit pièces.
- La touche `Q` ferme le jeu dans tous les états.

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
            title="Leçon 10 - interface",
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

        pyxel.text(98, 96, "MINI PLATFORMER", TEXT_COLOR)
        pyxel.text(76, 120, "Gauche et droite : marcher", TEXT_COLOR)
        pyxel.text(98, 136, "Espace : sauter", TEXT_COLOR)
        pyxel.text(92, 160, "Appuyez sur Espace", TEXT_COLOR)

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

        pyxel.rect(48, 92, 160, 60, pyxel.COLOR_BLACK)
        pyxel.text(102, 104, "Partie perdue", pyxel.COLOR_RED)
        pyxel.text(108, 116, f"Score : {self.score}", TEXT_COLOR)
        pyxel.text(78, 136, "Espace : revenir au titre", TEXT_COLOR)

    def draw_win(self):
        self.draw_play()

        pyxel.rect(48, 92, 160, 60, pyxel.COLOR_BLACK)
        pyxel.text(112, 104, "Victoire", pyxel.COLOR_YELLOW)
        pyxel.text(108, 116, f"Score : {self.score}", TEXT_COLOR)
        pyxel.text(78, 136, "Espace : revenir au titre", TEXT_COLOR)

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


Game()
```

## Découpage détaillé

### 00:00 — Montrer le résultat

**À l’écran :** lancer le jeu. Écran titre, appui sur espace, partie, victoire ou défaite, retour au titre, nouvelle partie.

**Narration :**

> Dans cette dixième leçon, le jeu prend la forme d’un vrai jeu.
>
> Il s’ouvre sur un écran titre. La barre d’espace lance la partie et la musique. Le score et le nombre de pièces restantes s’affichent en haut à gauche.
>
> Quand toutes les pièces sont ramassées, un écran de victoire apparaît. Au contact d’un ennemi, c’est l’écran de défaite. Dans les deux cas, la musique s’arrête et la barre d’espace ramène au titre.
>
> Le jeu lui-même n’a pas changé : même niveau, mêmes collisions, même caméra. C’est l’organisation du programme qui change.

**Action :** enchaîner deux parties pour montrer que tout est reconstruit à chaque fois.

### 00:55 — Présenter les objectifs

**À l’écran :** afficher les quatre points :

```text
1. quatre états, une constante
2. un aiguillage dans update et draw
3. une partie construite au bon moment
4. recharger les ressources pour recommencer
```

**Narration :**

> Quatre étapes structurent la leçon.
>
> D’abord les états, puis l’aiguillage qui choisit la méthode à exécuter. Ensuite la construction d’une partie au moment où elle commence. Enfin le rechargement des ressources, sans lequel on ne peut pas recommencer.
>
> L’audio suit le même mouvement : la musique démarre avec la partie et s’arrête à la fin.

### 01:40 — Un état, c’est un nombre

**À l’écran :** écrire les quatre constantes et `self.scene`.

**Narration :**

> Quatre constantes décrivent les quatre situations possibles : le titre, le jeu, la défaite et la victoire.
>
> L’attribut `scene` en contient une seule à la fois. Le jeu ne peut donc pas être à la fois en défaite et en victoire.
>
> Des booléens feraient le même travail en apparence, mais autoriseraient des combinaisons impossibles : deux attributs vrais en même temps, sans que rien ne l’empêche. Un état unique supprime le problème.

### 03:00 — Aiguiller la mise à jour et le dessin

**À l’écran :** écrire les deux aiguillages, puis faire apparaître les quatre méthodes correspondantes.

**Narration :**

> La boucle de jeu ne change pas : ce sont les méthodes appelées qui changent.
>
> Si l’état vaut titre, on met à jour le titre. S’il vaut jeu, on met à jour la partie, et ainsi de suite. Le dessin suit exactement le même aiguillage.
>
> Quatre petites méthodes se lisent mieux qu’une longue suite de conditions. `update_play()` ne sait rien de l’écran titre ; `update_title()` ne sait rien des ennemis.
>
> La touche Q est testée avant l’aiguillage : elle fonctionne donc dans tous les états.

### 04:30 — L’écran titre et la construction de la partie

**À l’écran :** montrer `__init__()` réduit à l’essentiel, puis `start_game()`.

**Narration :**

> Au lancement, le programme ne crée que l’état et le score. Ni niveau, ni joueur, ni pièce : la partie n’existe pas encore.
>
> La construction est confiée à `start_game()`, appelée quand la barre d’espace est pressée sur l’écran titre.
>
> Cette méthode construit le niveau, le joueur, les pièces, les ennemis, remet le score à zéro et passe l’état à jeu.
>
> Construire tout cela au démarrage obligerait à le réinitialiser à chaque tentative. Ici, chaque partie repart d’objets neufs.

### 06:00 — Recharger les ressources

**À l’écran :** montrer la première ligne de `start_game()`, puis la tilemap avant et après `take_coins()`.

**Narration :**

> La première ligne de `start_game()` est la plus importante : `pyxel.load()`.
>
> Depuis la leçon 7, `take_coins()` remplace les tuiles de pièce par des tuiles vides. Après une partie, le décor ne contient plus aucune pièce.
>
> Recharger les ressources relit le fichier et rétablit la tilemap d’origine : les dix-huit pièces reviennent, et la méthode peut les transformer en objets.
>
> Sans cette ligne, la deuxième partie démarrerait avec un décor vide, une liste de pièces vide et une victoire immédiate.

**Action :** commenter la ligne, relancer une partie, montrer la victoire immédiate, puis rétablir.

### 07:30 — La musique

**À l’écran :** montrer `pyxel.playm()` dans `start_game()`, puis `pyxel.stop()` dans les deux fins.

**Narration :**

> La musique démarre avec la partie, en boucle, et non au lancement du programme : l’écran titre reste silencieux.
>
> À la fin d’une partie, `pyxel.stop()` sans argument coupe tous les canaux. Plus de musique derrière l’écran de défaite.
>
> Les bruitages continuent d’utiliser les canaux zéro, un et deux ; la musique occupe les siens, et Pyxel mélange le tout.

### 08:30 — La victoire

**À l’écran :** écrire le test de victoire, en insistant sur le `return`.

**Narration :**

> La victoire se teste juste après le ramassage : une liste de pièces vide signifie que les dix-huit pièces ont été prises.
>
> Le `return` est essentiel. Sans lui, la vérification des ennemis s’exécuterait encore : un ennemi touché dans la même image remplacerait la victoire par la défaite.
>
> L’ordre des tests raconte donc une règle du jeu : la dernière pièce ramassée gagne, même si un ennemi est tout proche.

### 09:40 — L’interface et le centrage

**À l’écran :** afficher les deux lignes du score, puis le tableau des largeurs.

```text
un caractère : 4 pixels de large
colonne = (256 - 4 × nombre de caractères) // 2
```

**Narration :**

> En jeu, deux lignes suffisent : le score et le nombre de pièces restantes. Elles sont dessinées après la remise à zéro de la caméra, donc elles restent fixes pendant le défilement.
>
> Le libellé évite l’accent : la police intégrée de Pyxel ne contient que l’ASCII, et une lettre accentuée n’est pas dessinée. « Pièces » s’afficherait « Pices ». Les textes choisis pour l’interface s’en passent donc : « Restantes », « Victoire », « Gauche et droite : marcher ».
>
> Le titre de la fenêtre, lui, garde ses accents : il n’est pas dessiné par la police du jeu.
>
> Sur les écrans de titre et de fin, les textes sont centrés. Dans la police de Pyxel, un caractère mesure quatre pixels de large : un texte de n caractères occupe quatre n pixels, et commence à la colonne 256 moins cette largeur, divisé par deux.
>
> Par exemple, « MINI PLATFORMER » compte quinze caractères, soit soixante pixels, et commence à la colonne 98.
>
> Ces colonnes sont écrites en dur dans le code : la police ne change pas, et le calcul est fait une fois pour toutes.

### 11:00 — Les écrans de fin

**À l’écran :** écrire `draw_gameover()`, puis montrer la différence avec `draw_win()`.

**Narration :**

> L’écran de défaite commence par dessiner la scène de jeu : le décor reste visible, figé, derrière le message.
>
> Un rectangle noir isole le texte, puis trois lignes suffisent : le message, le score final, et la consigne pour revenir au titre.
>
> L’écran de victoire est identique, à deux détails près : le message « Victoire » remplace « Partie perdue » et passe en jaune.
>
> Appeler `draw_play()` depuis ces deux méthodes évite de recopier le dessin du niveau et des objets.
>
> La barre d’espace ramène au titre. Aucun objet n’est détruit : la partie suivante reconstruit tout, et l’ancienne est simplement oubliée.

### 12:00 — Exécuter et vérifier

**Action :** lancer le jeu et dérouler les vérifications.

**Narration :**

> Nous vérifions maintenant le comportement.
>
> Au lancement, l’écran titre s’affiche sans musique. La barre d’espace lance la partie : la musique démarre, le compteur indique zéro point et dix-huit pièces.
>
> Pendant la partie, le score et les pièces restantes restent fixes en haut à gauche, même quand le décor défile.
>
> En ramassant la dernière pièce, l’écran de victoire apparaît et la musique s’arrête. Au contact d’un ennemi, c’est l’écran de défaite.
>
> La barre d’espace ramène au titre dans les deux cas. Une nouvelle partie retrouve dix-huit pièces et un score à zéro : les ressources ont bien été rechargées.
>
> La touche Q ferme le jeu, quel que soit l’écran.

### 13:40 — Erreurs fréquentes

**À l’écran :** afficher la liste :

```text
deuxième partie vide -> pyxel.load() absent
jeu sans écran titre -> objets créés dans __init__()
musique qui continue -> pyxel.stop() oublié
défaite qui écrase la victoire -> return absent
état non traité -> aiguillage incomplet
ciel noir -> clé de transparence absente de bltm
```

**Narration :**

> Cinq erreurs sont fréquentes.
>
> Sans rechargement, la deuxième partie n’a plus de pièce : la liste est vide et la victoire s’affiche aussitôt.
>
> Construire les objets dans `__init__()` supprime l’écran titre, puisque la scène de jeu existe dès la première image.
>
> Sans `pyxel.stop()`, la musique continue derrière l’écran de défaite et pendant la saisie du titre.
>
> Sans le `return` après le test de victoire, la vérification des ennemis peut remplacer la victoire par la défaite.
>
> Enfin, ajouter un état sans compléter les deux aiguillages fait tomber cet état dans la dernière branche, avec le mauvais dessin.
>
> Une sixième erreur concerne le décor : le niveau couvre toute la fenêtre, et ses cases vides contiennent la couleur zéro. Sans clé de transparence passée à `bltm()`, ces cases sont recopiées en noir et le ciel disparaît. La couleur zéro est déjà la transparence des sprites depuis la leçon 2 ; le décor suit maintenant la même règle.

**Action :** retirer `pyxel.load()`, montrer la deuxième partie vide, puis rétablir.

### 15:40 — Expérimentations et conclusion

**À l’écran :** afficher la liste :

```text
- musique d’accueil
- trois vies
- temps limité
- écran de pause
- meilleur score
- transition en fondu
```

**Narration :**

> Plusieurs essais sont intéressants.
>
> Jouer la musique sur l’écran titre demande simplement un appel dans `update_title()` ; une musique différente demanderait d’en composer une seconde dans l’éditeur.
>
> Un compteur de vies remplace la défaite immédiate : le joueur revient au départ et la partie ne s’arrête qu’à zéro.
>
> Un temps limité s’appuie sur `pyxel.frame_count` divisé par trente, et déclenche la défaite quand il atteint zéro.
>
> Une pause est un cinquième état : la scène reste figée derrière un message.
>
> Un meilleur score se conserve dans un attribut, affiché sur l’écran titre ; le garder entre deux lancements demanderait d’écrire dans un fichier.
>
> Enfin, `pyxel.dither()` dessine en semi-transparence et permet un fondu.
>
> La dernière leçon prépare la Nuit du Code : choix du sujet, travail à deux, gestion du temps et vérifications avant le rendu.

## Consignes de montage

- Montrer l’enchaînement titre, partie, fin, titre dans une seule séquence, sans coupure.
- Afficher en incrustation les quatre constantes d’état au moment de l’aiguillage.
- Montrer la tilemap avant et après `take_coins()` avant de parler du rechargement.
- Montrer explicitement la deuxième partie sans `pyxel.load()`, puis avec.
- Garder l’interface visible pendant toute la phase de vérification.
- Conserver le même code final que l’article `article.html`.

## Vérification avant publication

- Le code compile et s’exécute avec Pyxel 3.0.1.
- Le jeu démarre sur l’écran titre, sans objet créé.
- `start_game()` recharge les ressources et reconstruit tous les objets.
- Les quatre états sont traités dans `update()` et dans `draw()`.
- La musique démarre avec la partie et s’arrête dans les deux fins.
- Le test de victoire précède celui des ennemis, avec un `return`.
- Les textes sont centrés selon la règle des 4 pixels par caractère.
- Les textes dessinés par `pyxel.text()` ne contiennent pas d’accent.
- Le décor laisse voir le fond grâce à la clé de transparence de `bltm()`.
- Une deuxième partie retrouve dix-huit pièces et un score nul.
- Le code affiché est identique à celui de l’article.
