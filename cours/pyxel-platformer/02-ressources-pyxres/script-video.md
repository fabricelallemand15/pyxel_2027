# Leçon 2 — Le fichier de ressources `.pyxres`

## Fiche de production

- **Formation :** Créer un mini-platformer 2D avec Pyxel
- **Public :** débutants en création de jeux, élèves de Première et Terminale NSI
- **Environnement :** PyxelStudio dans Capytale
- **Version ciblée :** Pyxel 3.0.1
- **Durée cible :** 15 à 17 minutes
- **Fichiers du projet :** `main.py` et `res.pyxres`
- **Ressource utilisée :** `res.pyxres` fourni avec la leçon
- **Titre à l’écran :** Leçon 2 — Le fichier de ressources `.pyxres`

## Intention pédagogique

Cette leçon remplace les formes géométriques de la leçon 1 par des ressources créées dans l’éditeur Pyxel.

Le fichier `res.pyxres` est fourni avec le cours, ce qui garantit que tous les élèves obtiennent le même résultat. L’éditeur de ressources reste montré pour trois raisons :

- expliquer d’où viennent les images, la tilemap et les sons ;
- permettre aux élèves de modifier le décor et les bruitages ;
- préparer la leçon 11, où le jeu sera personnalisé.

La leçon conserve la structure en classes de la leçon 1. Deux classes sont ajoutées ou modifiées :

- `Level`, qui dessine la tilemap ;
- `Player`, qui utilise maintenant une image.

## Objectifs annoncés aux élèves

À la fin de la vidéo, l’élève doit pouvoir :

1. expliquer le rôle du fichier `.pyxres` ;
2. charger les ressources avec `pyxel.load()` ;
3. afficher un sprite avec `pyxel.blt()` ;
4. dessiner le niveau avec `pyxel.bltm()` ;
5. jouer un bruitage et une musique ;
6. indiquer la taille de fenêtre imposée par la Nuit du Code.

## Préparation de l’enregistrement

### Fichiers

- `main.py` ouvert dans PyxelStudio ;
- `res.pyxres` importé dans le projet, dans le même dossier que `main.py`.

### Vérifications avant d’enregistrer

- La musique se lance au démarrage.
- Le bruitage se déclenche à chaque rebond.
- Le joueur ne montre pas de rectangle noir autour de lui.
- Les cases vides de la tilemap n’affichent pas de joueur.

### Code final

```python
import pyxel


SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
RESOURCE_FILE = "res.pyxres"

TILE_SIZE = 8
LEVEL_WIDTH = 32
LEVEL_HEIGHT = 32

PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLAYER_SPEED = 1
PLAYER_TILE_X = 0
PLAYER_TILE_Y = 0
PLAYER_START_X = 40
PLAYER_START_Y = 216

BACKGROUND_COLOR = pyxel.COLOR_DARK_BLUE
TEXT_COLOR = pyxel.COLOR_WHITE
TRANSPARENT_COLOR = 0

BOUNCE_SOUND = 1
MUSIC = 0


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
        self.dx = PLAYER_SPEED

    def update(self):
        self.x += self.dx

        if self.x <= 0:
            self.x = 0
            self.dx = abs(self.dx)
        elif self.x + self.width >= pyxel.width:
            self.x = pyxel.width - self.width
            self.dx = -abs(self.dx)

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
            title="Leçon 2 - ressources",
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

        direction = self.player.dx
        self.player.update()

        if self.player.dx != direction:
            pyxel.play(0, BOUNCE_SOUND)

    def draw(self):
        pyxel.cls(BACKGROUND_COLOR)
        self.level.draw()

        pyxel.text(
            4,
            4,
            "Leçon 2 - ressources",
            TEXT_COLOR,
        )
        pyxel.text(
            4,
            12,
            "Images, tilemap et audio",
            TEXT_COLOR,
        )

        self.player.draw()


Game()
```

## Découpage détaillé

### 00:00 — Montrer le résultat

**À l’écran :** lancer le jeu terminé. Le niveau apparaît avec un sol vert et marron, trois plateformes, neuf pièces et un personnage. La musique démarre. Le personnage se déplace et le bruitage se déclenche à chaque rebond.

**Narration :**

> Dans cette deuxième leçon, le jeu utilise de vraies ressources graphiques et sonores.
>
> Le décor n’est plus dessiné avec des rectangles : il provient d’une tilemap. Le personnage est une image. Une musique est jouée en boucle et un bruitage accompagne les rebonds.
>
> Toutes ces données sont regroupées dans un seul fichier, `res.pyxres`, placé à côté de `main.py`.

**Action :** laisser tourner quinze secondes pour que la musique et le rebond soient entendus, puis arrêter.

### 00:30 — Respecter le règlement de la Nuit du Code

**À l’écran :** afficher une diapositive :

```text
Nuit du Code : fenêtre de 128 x 128 ou 256 x 256

Formation : 256 x 256
```

**Narration :**

> Le règlement de la Nuit du Code impose une fenêtre de jeu de 128 pixels sur 128, ou de 256 pixels sur 256.
>
> La formation utilise 256 sur 256.
>
> Cette taille laisse de la place au décor : 32 tuiles de 8 pixels, soit 256 pixels de large. Le niveau peut comporter plusieurs plateformes étagées sans devenir à l’étroit.
>
> La variante 128 sur 128 reste conforme au règlement. Elle modifie les dimensions de l’écran, le nombre de tuiles visibles et les positions du décor.

**À l’écran :** mettre en évidence les constantes :

```python
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
```

**Narration :**

> Ces deux constantes sont fixées pour toute la formation.

### 01:10 — Présenter le fichier `.pyxres`

**À l’écran :** montrer le projet dans PyxelStudio avec les deux fichiers.

**Narration :**

> Le projet contient maintenant deux fichiers.
>
> `main.py` contient tout le code Python. `res.pyxres` contient les données du jeu : les images, la tilemap, les sons et les musiques.
>
> Le fichier de ressources n’est pas un fichier Python. Il ne contient aucune instruction. Le programme ne lit pas son contenu : il lui demande simplement une image ou une tuile à des coordonnées données.

**À l’écran :** afficher le tableau :

```text
images    -> pyxel.blt()
tilemaps  -> pyxel.bltm()
sons      -> pyxel.play()
musiques  -> pyxel.playm()
```

**Narration :**

> Quatre familles de ressources, quatre fonctions.
>
> Les images servent aux personnages et aux objets. Les tilemaps servent au décor. Les sons servent aux actions courtes. Les musiques servent à l’ambiance.

**Note de montage :** renforcer cette indication par une incrustation. Ne pas afficher le contenu interne du fichier `.pyxres` dans la vidéo : ce détail est hors du périmètre de la leçon.

### 02:00 — Importer le fichier fourni

**À l’écran :** montrer l’import de `res.pyxres` dans PyxelStudio, puis son ouverture dans l’éditeur de ressources.

**Narration :**

> Le fichier `res.pyxres` est fourni avec la leçon.
>
> Il doit être placé dans le même dossier que `main.py`. Si les deux fichiers ne sont pas dans le même dossier, le programme ne trouvera pas les ressources et affichera une erreur.
>
> Selon la version de PyxelStudio, le fichier est importé dans le projet puis ouvert dans l’éditeur de ressources. Les captures de cette vidéo utilisent cette version.

**Action :** montrer rapidement l’arborescence du projet, avec `main.py` et `res.pyxres` côte à côte.

**Note de production :** si l’import de fichier n’est pas disponible dans l’interface utilisée, enregistrer une séquence alternative de deux minutes montrant la reconstruction des ressources dans l’éditeur. Le code Python reste identique.

### 02:50 — L’éditeur d’images

**À l’écran :** ouvrir l’éditeur d’images, banque 0. La souris désigne successivement les quatre positions du joueur, puis les tuiles du sol.

**Narration :**

> L’éditeur d’images travaille sur des banques de 256 pixels sur 256.
>
> Chaque tuile occupe une zone de 8 pixels sur 8. La banque est donc une grille de 32 tuiles sur 32.
>
> Les quatre premières cases de la ligne 0 contiennent le personnage : deux images au repos, deux images de marche. Les images de marche ne sont pas encore utilisées : elles serviront pour l’animation.
>
> La ligne 1 contient le décor : le dessus du sol, le remplissage du sol, une plateforme, une pièce et un buisson.

**Action :** dessiner quelques pixels dans la tuile du personnage pour montrer que la modification se répercutera dans le jeu, puis annuler avec Ctrl+Z.

**Narration :**

> Toute modification faite ici apparaît immédiatement dans le jeu. Le décor et le personnage peuvent donc être retravaillés sans toucher au code.

**À l’écran :** montrer la palette et sélectionner une couleur.

**Narration :**

> La palette contient 16 couleurs. La couleur 0 est réservée à la transparence dans les sprites. C’est pour cette raison que les contours du personnage utilisent le bleu nuit plutôt que le noir.

### 05:00 — L’éditeur de tilemap

**À l’écran :** ouvrir l’éditeur de tilemap, tilemap 0.

**Narration :**

> Une tilemap est une grille de références. Chaque case ne contient pas un dessin : elle contient la position d’une tuile dans la banque d’images.
>
> La tilemap 0 décrit notre niveau. Elle utilise 32 cases de large sur 32 cases de haut, soit 256 pixels sur 256.
>
> La ligne 28 contient le dessus du sol. Les lignes suivantes contiennent le remplissage. Le joueur se déplace à la surface, juste au-dessus de la ligne 28.

**Action :** survoler les plateformes, les pièces et le buisson.

**Narration :**

> Les plateformes occupent les lignes 23, 19 et 15 : elles montent vers la droite. Les pièces se trouvent juste au-dessus, sur les lignes 22, 18 et 14. Trois buissons décorent le sol.
>
> Les autres cases sont vides. Une case vide référence une zone transparente de la banque d’images, ici la tuile située en bas à droite de la zone utilisée.
>
> Si une case vide référence la tuile du personnage, le personnage apparaît répété sur tout le niveau. C’est une erreur fréquente.

**Action :** placer une tuile au hasard dans une case vide, exécuter le jeu, montrer le résultat, puis annuler.

### 07:00 — L’éditeur de sons

**À l’écran :** ouvrir l’éditeur de sons, son 0.

**Narration :**

> L’éditeur de sons permet de composer des bruitages courts.
>
> Le son 0 est utilisé pour le saut : quelques notes qui montent, avec un effet de glissement. Le son 1 est utilisé pour la pièce et pour le rebond : deux notes aiguës. Le son 2 servira pour une collision : des notes graves et un effet de bruit.

**Action :** jouer chaque son, puis modifier une note du son 1 pour montrer que le résultat change.

**Narration :**

> Chaque son possède une vitesse, des notes, un timbre, un volume et un effet. Ces réglages seront détaillés lorsque plusieurs sons seront combinés.

### 08:00 — L’éditeur de musiques

**À l’écran :** ouvrir l’éditeur de musiques, musique 0.

**Narration :**

> L’éditeur de musiques assemble des sons sur quatre canaux.
>
> La musique 0 utilise deux canaux. Le canal 0 contient la mélodie : quatre sons de quatre notes. Le canal 1 contient l’accompagnement.
>
> Une musique ne contient pas de notes directement : elle contient une suite de numéros de sons. C’est ce qui permet de réutiliser un même son dans plusieurs musiques.

**Action :** lancer la lecture de la musique dans l’éditeur.

### 08:50 — Charger les ressources

**À l’écran :** revenir à `main.py`, qui contient encore le code de la leçon 1. Ajouter :

```python
RESOURCE_FILE = "res.pyxres"
```

puis, dans `Game.__init__()`, après `pyxel.init()` :

```python
pyxel.load(RESOURCE_FILE)
```

**Narration :**

> Le chargement se fait une seule fois, au démarrage.
>
> L’appel doit être placé après `pyxel.init()` et avant `pyxel.run()`. Toutes les ressources sont alors disponibles pour la suite du programme.
>
> Le nom du fichier est placé dans une constante. Si le fichier est renommé, une seule ligne est à modifier.

### 09:30 — Afficher le joueur avec `pyxel.blt()`

**À l’écran :** remplacer le corps de `Player.draw()` par :

```python
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
```

**Narration :**

> `pyxel.blt()` copie une zone d’une banque d’images vers l’écran.
>
> Les deux premiers arguments sont la position à l’écran. Le troisième est le numéro de la banque. Les deux suivants indiquent la zone à copier dans la banque, en pixels. Viennent ensuite la largeur, la hauteur et la couleur transparente.
>
> Il faut distinguer deux repères : la position à l’écran, et la position dans la banque d’images.

**À l’écran :** afficher le schéma :

```text
pyxel.blt(x, y, img, u, v, w, h, colkey)

x, y      où dessiner à l'écran
img       quelle banque d'images
u, v      quoi dessiner dans la banque
w, h      taille de la zone copiée
colkey    couleur transparente
```

**Narration :**

> La position dans la banque est calculée à partir de coordonnées de tuiles. La tuile 0, 0 correspond aux pixels 0, 0. La tuile 2, 0 correspond aux pixels 16, 0.
>
> Les constantes `PLAYER_TILE_X` et `PLAYER_TILE_Y` permettent de choisir l’image sans écrire directement des pixels.

**À l’écran :** modifier temporairement :

```python
PLAYER_TILE_X = 2
```

**Narration :**

> En changeant cette constante, le joueur utilise l’image de marche.

**Action :** remettre `PLAYER_TILE_X = 0`.

### 11:00 — La couleur transparente

**À l’écran :** supprimer temporairement le dernier argument de `pyxel.blt()` et exécuter.

**Narration :**

> Sans la couleur transparente, le sprite est dessiné avec un rectangle noir autour du personnage.
>
> La couleur 0 de la palette est déclarée transparente. Tous les pixels de cette couleur sont ignorés lors de la copie.

**Action :** restaurer l’argument.

### 11:40 — Dessiner le niveau avec `pyxel.bltm()`

**À l’écran :** ajouter la classe `Level` avant la classe `Player`.

```python
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
```

**Narration :**

> Le niveau est dessiné par une nouvelle classe, `Level`.
>
> `pyxel.bltm()` copie une zone de tilemap vers l’écran. Les arguments sont comparables à ceux de `blt()` : position à l’écran, numéro de tilemap, position dans la tilemap, puis largeur et hauteur.
>
> Le niveau étant aussi grand que l’écran, la position et la taille couvrent 256 pixels.

**À l’écran :** créer le niveau dans `Game.__init__()` :

```python
self.level = Level()
```

puis l’appeler dans `Game.draw()`, après `pyxel.cls()` :

```python
self.level.draw()
```

**Narration :**

> La classe `Level` suit la même organisation que `Player` : un constructeur qui prépare les données, puis une méthode `draw()`.
>
> Elle ne possède pas encore de méthode `update()`, car le décor est immobile. Cette méthode apparaîtra avec le défilement.

**Action :** exécuter. Le décor apparaît, le joueur reste dessiné par un rectangle.

### 13:00 — Jouer un son et une musique

**À l’écran :** ajouter les constantes :

```python
BOUNCE_SOUND = 1
MUSIC = 0
```

puis, dans `Game.__init__()`, avant `pyxel.run()` :

```python
pyxel.playm(MUSIC, loop=True)
```

**Narration :**

> La musique est lancée au démarrage et rejouée en boucle.
>
> Le paramètre `loop` indique que la musique reprend à la fin.

**À l’écran :** ajouter dans `Game.update()` :

```python
direction = self.player.dx
self.player.update()

if self.player.dx != direction:
    pyxel.play(0, BOUNCE_SOUND)
```

**Narration :**

> Pour le bruitage, le jeu observe la direction du joueur avant et après la mise à jour.
>
> Le joueur change de sens uniquement lorsqu’il atteint un bord. La comparaison suffit donc à détecter un rebond.
>
> `pyxel.play()` reçoit le numéro de canal puis le numéro de son. Le canal 0 est utilisé. Les quatre canaux permettent de jouer plusieurs sons simultanément : ils serviront pour le saut et les collisions.

**Action :** exécuter et laisser entendre deux rebonds.

### 14:20 — Vérification et erreurs fréquentes

**À l’écran :** afficher la liste :

```text
Failed to open file 'res.pyxres'  -> fichier absent ou mal nommé
rectangle noir autour du sprite   -> couleur transparente oubliée
joueur répété dans le décor       -> case vide de la tilemap incorrecte
aucun son                         -> ressources non chargées ou mauvais numéro
```

**Narration :**

> Quatre erreurs sont fréquentes.
>
> Si le message indique que le fichier est introuvable, vérifier son nom et son emplacement : il doit être dans le même dossier que `main.py`.
>
> Si un rectangle noir entoure le personnage, la couleur transparente a été oubliée.
>
> Si le personnage apparaît répété dans le décor, une case vide de la tilemap référence une tuile dessinée.
>
> Si aucun son n’est entendu, vérifier que le chargement a bien eu lieu et que le numéro du son est correct.

**Action :** montrer rapidement l’erreur de fichier introuvable en renommant temporairement le fichier de ressources.

### 15:10 — Expérimentations et conclusion

**À l’écran :** afficher la liste :

```text
- utiliser l'image de marche du joueur
- afficher une pièce isolée
- changer le bruitage du rebond
- déplacer une plateforme dans l'éditeur de tilemap
```

**Narration :**

> Trois modifications sont simples à essayer.
>
> Changer la constante `PLAYER_TILE_X` sélectionne une autre image du joueur.
>
> Changer la constante `BOUNCE_SOUND` sélectionne un autre bruitage.
>
> Déplacer une plateforme dans l’éditeur de tilemap modifie le décor sans modifier le code.
>
> La prochaine leçon remplace le déplacement automatique par les contrôles du clavier.

## Consignes de montage

- Ne pas montrer le contenu interne du fichier `.pyxres` : le format n’est pas au programme de la leçon.
- Montrer la palette Pyxel lors de l’explication de la couleur transparente.
- Afficher le schéma des paramètres de `blt()` et de `bltm()` en incrustation.
- Laisser la musique audible pendant les phases de saisie de code, à volume réduit.
- Utiliser un cadrage rapproché de l’éditeur de ressources.
- Conserver le même code final que l’article `.qmd`.

## Vérification avant publication

- Le jeu s’exécute avec Pyxel 3.0.1.
- La fenêtre mesure 256 × 256 pixels.
- Le fichier `res.pyxres` est bien détecté depuis le dossier de `main.py`.
- Le sprite du joueur est dessiné sans rectangle noir.
- La tilemap affiche uniquement le décor prévu.
- La musique est audible en boucle.
- Le bruitage est déclenché à chaque rebond.
- La touche `Q` quitte l’application.
- Le code affiché est identique à celui de l’article.
