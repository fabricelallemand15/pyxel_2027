# Leçon 4 — Gravité et saut

## Fiche de production

- **Formation :** Créer un mini-platformer 2D avec Pyxel
- **Public :** débutants en création de jeux, élèves de Première et Terminale NSI
- **Environnement :** PyxelStudio dans Capytale
- **Version ciblée :** Pyxel 3.0.1
- **Durée cible :** 14 à 16 minutes
- **Fichiers du projet :** `main.py` et `res.pyxres`
- **Ressource utilisée :** `res.pyxres`, inchangée
- **Titre à l’écran :** Leçon 4 — Gravité et saut

## Intention pédagogique

Cette leçon ajoute une composante verticale au joueur.

Le travail porte sur quatre points :

- une seconde vitesse, `dy` ;
- une accélération constante vers le bas ;
- un saut déclenché par une action ponctuelle ;
- une détection simple du sol, mémorisée dans un attribut.

La leçon introduit la distinction entre position, vitesse et accélération, sans formalisme mathématique. Les plateformes restent traversables : seule la ligne du sol arrête le joueur.

## Objectifs annoncés aux élèves

À la fin de la vidéo, l’élève doit pouvoir :

1. expliquer le rôle de `dy` ;
2. appliquer une gravité à chaque image ;
3. déclencher un saut avec `pyxel.btnp()` ;
4. empêcher un saut en l’air ;
5. utiliser un attribut pour retenir si le joueur touche le sol.

## Préparation de l’enregistrement

### Fichiers

- `main.py` de la leçon 4, dans le dossier `04-gravite-et-saut` ;
- `res.pyxres` recopié à côté de ce fichier.

### Vérifications avant d’enregistrer

- Le joueur est posé sur le sol au démarrage et reste immobile.
- La barre d’espace déclenche un saut, puis le joueur revient exactement sur le sol.
- Maintenir la barre d’espace ne provoque pas de sauts successifs.
- Appuyer sur la barre d’espace en l’air ne produit aucun effet.
- Le son du saut est audible à chaque départ.
- Les flèches continuent de déplacer le joueur pendant le saut.

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
        self.width = LEVEL_WIDTH * TILE_SIZE
        self.height = LEVEL_HEIGHT * TILE_SIZE

    def draw(self):
        pyxel.bltm(
            0,
            0,
            0,
            0,
            0,
            self.width,
            self.height,
        )


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
            title="Chapitre 4 - chute et saut",
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

        pyxel.text(
            4,
            4,
            "Chapitre 4 - chute et saut",
            TEXT_COLOR,
        )
        pyxel.text(
            4,
            12,
            "Gauche et droite : marcher, Espace : sauter",
            TEXT_COLOR,
        )

        self.player.draw()


Game()
```

## Découpage détaillé

### 00:00 — Montrer le résultat

**À l’écran :** lancer le jeu. Le joueur est posé sur le sol. Les flèches le déplacent, la barre d’espace déclenche un saut, puis il retombe.

**Narration :**

> Dans cette quatrième leçon, le joueur ne se déplace plus seulement sur une ligne : il peut sauter.
>
> La gravité l’attire vers le sol en permanence. Lorsqu’il touche le sol, la barre d’espace déclenche un saut.
>
> Le saut n’est pas un déplacement instantané : le joueur monte, ralentit, s’arrête un instant en haut de sa trajectoire, puis retombe de plus en plus vite.

**Action :** effectuer trois sauts, dont un pendant un déplacement horizontal, puis laisser le joueur retomber.

### 00:45 — Présenter les objectifs

**À l’écran :** afficher les quatre points :

```text
1. une vitesse verticale : dy
2. une accélération vers le bas : la gravité
3. une action ponctuelle : le saut
4. un attribut : is_on_ground
```

**Narration :**

> Quatre éléments suffisent pour obtenir un saut crédible.
>
> Une vitesse verticale décrit le déplacement vers le haut ou vers le bas. Une accélération, la gravité, modifie cette vitesse à chaque image. Une touche déclenche le saut. Enfin, un attribut retient si le joueur touche le sol, ce qui interdit les sauts en l’air.

### 01:30 — Ajouter `dy` au joueur

**À l’écran :** montrer le constructeur de la leçon 3, puis le compléter :

```python
def __init__(self, x, y):
    self.x = x
    self.y = y
    self.width = PLAYER_WIDTH
    self.height = PLAYER_HEIGHT
    self.dx = 0
    self.dy = 0
    self.is_on_ground = True
```

**Narration :**

> Le joueur possède déjà `dx`, sa vitesse horizontale. Nous ajoutons `dy`, sa vitesse verticale, et `is_on_ground`, qui indique s’il touche le sol.
>
> Au départ, le joueur est posé sur le sol : sa vitesse verticale est nulle et l’attribut vaut vrai.

**À l’écran :** ajouter les constantes :

```python
GRAVITY = 1
JUMP_SPEED = -11
GROUND_Y = 224
```

**Narration :**

> Trois constantes accompagnent ces attributs.
>
> `GRAVITY` vaut 1 : la vitesse verticale augmente d’un pixel par image. `JUMP_SPEED` vaut moins 11 : le signe négatif indique un déplacement vers le haut. `GROUND_Y` vaut 224, la coordonnée du dessus du sol.

**À l’écran :** montrer la position de départ :

```python
PLAYER_START_Y = GROUND_Y - PLAYER_HEIGHT
```

**Narration :**

> La position de départ est maintenant calculée à partir du sol. Le joueur commence donc exactement posé, sans nombre écrit deux fois.

### 03:00 — Appliquer la gravité

**À l’écran :** ajouter à la fin de `Player.update()` :

```python
self.dy += GRAVITY
self.y += self.dy
```

**Narration :**

> La gravité ne modifie pas la position du joueur : elle modifie sa vitesse verticale.
>
> À chaque image, `dy` augmente de 1, puis la position est mise à jour avec cette vitesse. Le joueur tombe donc de plus en plus vite : 1 pixel à la première image, 2 à la suivante, 3 ensuite.

**À l’écran :** afficher le tableau de progression :

```text
image 1 : dy = 1  -> y + 1
image 2 : dy = 2  -> y + 2
image 3 : dy = 3  -> y + 3
```

**Narration :**

> On retrouve la distinction entre position, vitesse et accélération.
>
> La position indique où se trouve l’objet. La vitesse indique de combien il se déplace à chaque image. L’accélération indique de combien la vitesse change à chaque image.
>
> La gravité est une accélération : elle agit sur la vitesse, et la vitesse agit sur la position.

**Action :** exécuter le jeu quelques secondes : le joueur tombe et sort de l’écran.

**Narration :**

> Le joueur tombe, mais rien ne l’arrête : il traverse le bas de l’écran. Il manque le test de contact avec le sol.

### 04:40 — Détecter le sol

**À l’écran :** ajouter après la mise à jour de la position :

```python
if self.y + self.height >= GROUND_Y:
    self.y = GROUND_Y - self.height
    self.dy = 0
    self.is_on_ground = True
else:
    self.is_on_ground = False
```

**Narration :**

> Le bas du joueur se trouve à la position `y` plus sa hauteur.
>
> Tant que cette valeur reste inférieure à la coordonnée du sol, le joueur est au-dessus. Dès qu’elle l’atteint ou la dépasse, le joueur est replacé exactement sur le sol.
>
> Sa vitesse verticale est remise à zéro. Sans cette remise à zéro, la vitesse continuerait d’augmenter pendant que le joueur est posé, et la chute reprendrait brutalement dès qu’il quitte le sol.

**Action :** exécuter de nouveau : le joueur reste posé sur le sol.

**Narration :**

> L’attribut `is_on_ground` retient le résultat du test. Il vaut vrai quand le joueur touche le sol, faux lorsqu’il est en l’air.

### 06:20 — Déclencher le saut

**À l’écran :** insérer avant la gravité :

```python
if pyxel.btnp(pyxel.KEY_SPACE) and self.is_on_ground:
    self.dy = JUMP_SPEED
    pyxel.play(0, JUMP_SOUND)
```

**Narration :**

> Le saut consiste à donner au joueur une vitesse verticale négative.
>
> Avec moins 11, le joueur monte vite au départ, puis de moins en moins vite, parce que la gravité réduit cette vitesse à chaque image. Il finit par s’arrêter en haut de sa trajectoire, puis retombe.
>
> La condition contient deux parties. La première vérifie que la barre d’espace vient d’être pressée. La seconde vérifie que le joueur est au sol.

**À l’écran :** afficher la condition en incrustation :

```text
pyxel.btnp(KEY_SPACE) and is_on_ground
        action ponctuelle      état du joueur
```

**Narration :**

> La seconde partie interdit les sauts en l’air : lorsqu’il est en plein saut, `is_on_ground` vaut faux et une nouvelle pression n’a aucun effet.

### 07:40 — `btnp()` ou `btn()` pour sauter

**Action :** remplacer temporairement `btnp()` par `btn()`, exécuter, maintenir la barre d’espace.

**Narration :**

> Si nous utilisons `pyxel.btn()` à la place de `pyxel.btnp()`, le saut se déclenche à chaque image où le joueur touche le sol.
>
> En maintenant la barre d’espace, le joueur rebondit sans arrêt dès qu’il reprend contact avec le sol.

**Action :** rétablir `btnp()`.

**Narration :**

> Un saut est une action ponctuelle : `pyxel.btnp()` est la fonction adaptée.
>
> Les flèches, elles, restent lues avec `pyxel.btn()`, car le déplacement doit être continu.

### 08:50 — Jouer le son du saut

**À l’écran :** ajouter la constante :

```python
JUMP_SOUND = 0
```

**Narration :**

> Le son numéro 0 du fichier de ressources est celui du saut.
>
> Le son est joué au moment du déclenchement, dans la méthode du joueur. Le joueur connaît la règle qui provoque le saut : il peut donc jouer lui-même le bruitage.

### 09:40 — Exécuter et vérifier

**Action :** lancer le jeu et dérouler les vérifications.

**Narration :**

> Nous vérifions maintenant le comportement complet.
>
> Au démarrage, le joueur est posé sur le sol et reste immobile.
>
> Une pression sur la barre d’espace déclenche un saut d’environ 55 pixels de haut, puis le joueur revient exactement sur le sol.
>
> Maintenir la touche ne provoque pas de saut supplémentaire. Appuyer en l’air ne produit rien.
>
> Les flèches continuent de déplacer le joueur pendant le saut.
>
> Les plateformes sont toujours traversées : elles ne sont pas encore solides. Elles le deviendront avec les collisions.

### 11:00 — Erreurs fréquentes

**À l’écran :** afficher la liste :

```text
sauts en série        -> btn() au lieu de btnp()
sauts multiples       -> is_on_ground oublié
chute infinie         -> test du sol absent
joueur flottant       -> GROUND_Y incohérent avec la tilemap
```

**Narration :**

> Quatre erreurs sont fréquentes.
>
> Des sauts en série indiquent que `btn()` a été utilisé à la place de `btnp()`.
>
> Des sauts multiples en l’air indiquent que la condition `is_on_ground` a été oubliée.
>
> Une chute infinie signifie que le test de contact avec le sol est absent, ou placé avant la mise à jour de la position.
>
> Enfin, un joueur qui flotte ou s’enfonce dans le sol vient d’une constante `GROUND_Y` qui ne correspond pas au dessin de la tilemap.

**Action :** montrer l’erreur de chute infinie en supprimant temporairement le test du sol, puis rétablir.

### 12:40 — Expérimentations et conclusion

**À l’écran :** afficher la liste :

```text
- changer JUMP_SPEED
- changer GRAVITY
- ajouter la flèche haut
- afficher dy à l’écran
```

**Narration :**

> Plusieurs réglages sont intéressants à essayer.
>
> Diminuer la valeur absolue de `JUMP_SPEED` raccourcit le saut ; l’augmenter le rend plus ample.
>
> Augmenter `GRAVITY` rend la chute plus rapide et le saut plus sec.
>
> La flèche du haut peut aussi déclencher le saut, à condition de rester sur une action ponctuelle.
>
> Enfin, afficher `dy` à l’écran permet de voir la vitesse verticale changer image par image.
>
> Dans la prochaine leçon, le décor devient un véritable niveau à parcourir, en préparation des collisions.

## Consignes de montage

- Afficher en incrustation la condition de saut avec ses deux parties.
- Montrer le tableau de progression de `dy` pendant l’explication de la gravité.
- Laisser le son du saut audible sans le renforcer au montage.
- Montrer chaque erreur en l’exécutant vraiment, puis rétablir le code avant de continuer.
- Conserver le même code final que l’article `article.html`.

## Vérification avant publication

- Le code compile et s’exécute avec Pyxel 3.0.1.
- Le joueur est posé à la position 216 au démarrage.
- Le saut atteint environ 55 pixels au-dessus du sol.
- Le joueur revient exactement à la position 216.
- Maintenir la barre d’espace ne produit qu’un saut.
- Une pression en l’air ne produit aucun saut.
- Le son du saut est joué une fois par saut.
- Les flèches restent actives pendant le saut.
- Le code affiché est identique à celui de l’article.
