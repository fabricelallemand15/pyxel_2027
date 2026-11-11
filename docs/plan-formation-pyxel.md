# Plan détaillé de la formation Pyxel

## Créer un mini-platformer 2D en Python pour la Nuit du Code

**Public cible :** élèves de Première et Terminale NSI  
**Environnement :** PyxelStudio dans Capytale  
**Version ciblée :** Pyxel 3.0.1  
**Format principal :** une vidéo, un article et un projet exécutable par leçon  
**Statut :** plan de conception avant production

---

## 1. Finalité de la formation

Cette formation doit permettre à un débutant en création de jeux de réaliser un petit jeu de plateforme 2D avec Pyxel, puis de le personnaliser pour participer à la Nuit du Code.

Le résultat attendu n'est pas une simple démonstration technique. L'élève doit progressivement comprendre comment passer :

1. d'une idée de jeu ;
2. à un état représenté par des objets Python ;
3. à une mise à jour image par image ;
4. à un affichage séparé de la logique ;
5. à un jeu complet avec niveau, règles, sons, musique et victoire ;
6. à un projet personnel contenu dans le format imposé par le concours.

La formation ne constitue pas une séquence scolaire avec contrôle ou notation. Elle est conçue comme un parcours de création guidé, avec des défis facultatifs et une progression vers un jeu jouable.

---

## 2. Contraintes définitives du projet

### 2.1. Format Nuit du Code

Chaque projet utilisable par un élève doit respecter la contrainte suivante :

```text
main.py
res.pyxres
```

Les deux fichiers sont placés dans le même dossier.

Le projet ne doit dépendre d'aucun autre fichier pour fonctionner :

- pas de second fichier Python ;
- pas de module personnel importé ;
- pas d'image PNG externe ;
- pas de fichier WAV ou OGG externe ;
- pas de police externe ;
- pas de fichier TMX ;
- pas de dossier `assets` nécessaire à l'exécution.

Le fichier `res.pyxres` contient les ressources du jeu :

- sprites et images ;
- tiles et tilemap ;
- bruitages ;
- musiques.

Le programme chargera la ressource après l'initialisation de Pyxel :

```python
pyxel.init(256, 256, title="Mon platformer")
pyxel.load("res.pyxres")
```

Le nom `res.pyxres` est la convention de référence du cours. Si l'interface Capytale impose un autre nom, seul le nom passé à `pyxel.load()` devra changer ; la règle d'un seul fichier `.pyxres` dans le même dossier reste inchangée.

Le règlement de la Nuit du Code impose par ailleurs une fenêtre de jeu de 128 × 128 ou de 256 × 256 pixels.

La formation retient **256 × 256 pixels** :

- un écran de 256 × 256 pixels correspond à 32 × 32 tuiles ; le niveau de référence en occupe 64 × 32 et défile à partir de la leçon 9 ;
- les textes affichés à l'écran sont en ASCII : la police intégrée ne dessine ni les accents ni la cédille, ce qui impose le mot « Chapitre » à la place de « Leçon » dans la fenêtre du jeu ;
- le décor peut comporter plusieurs plateformes étagées sans être à l'étroit ;
- les sprites de 8 × 8 pixels restent petits par rapport à la fenêtre, ce qui donne un rendu lisible.

La variante 128 × 128 est mentionnée dans les leçons comme une alternative conforme au règlement. Elle change les dimensions de l'écran, le nombre de tuiles visibles et les positions du décor.

### 2.2. POO simplifiée

La formation utilise la POO dès le début, mais sans constructions avancées.

Principes retenus :

- un type d'élément du jeu correspond à une classe ;
- chaque objet possède son état dans des attributs ;
- chaque objet possède une méthode `update()` ;
- chaque objet possède une méthode `draw()` ;
- la classe `Game` coordonne les objets ;
- les objets d'un même type sont regroupés dans une liste ;
- aucune variable globale ne représente l'état courant du jeu.

Classes attendues dans le projet final :

```python
class Level:
    ...


class Player:
    ...


class Coin:
    ...


class Enemy:
    ...


class Game:
    ...
```

Le code n'utilisera pas, dans le parcours principal :

- de décorateurs ;
- de classes abstraites ;
- d'héritage ;
- de `dataclass` ;
- de gestionnaire d'événements ;
- de système de composants ;
- de bibliothèque externe ;
- de constructions dont le fonctionnement est caché aux débutants.

Des constantes simples restent autorisées :

```python
PLAYER_SPEED = 2
PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
```

### 2.3. Environnement

Le parcours principal est conçu pour PyxelStudio dans Capytale avec Pyxel 3.0.1.

Il ne faut pas confondre cet environnement avec la copie publique historique de PyxelStudio utilisée comme référence technique secondaire. Le cours cible la version effectivement disponible dans Capytale, et les exemples devront être testés dans cet environnement avant publication.

---

## 3. Prérequis et positionnement pédagogique

### 3.1. Prérequis Python

On suppose que les élèves savent déjà :

- affecter une valeur à une variable ;
- utiliser des nombres, des chaînes et des booléens ;
- écrire des conditions ;
- utiliser des boucles `for` et `while` ;
- définir et appeler une fonction ;
- manipuler une liste ;
- importer un module avec `import`.

La POO n'est pas supposée connue. Elle est introduite progressivement dans le contexte du jeu.

### 3.2. Notions de POO à introduire

Le cours expliquera avec des exemples concrets :

- classe et objet ;
- attribut ;
- méthode ;
- constructeur `__init__()` ;
- rôle de `self` ;
- création de plusieurs objets à partir d'une même classe ;
- responsabilité d'une classe ;
- relation entre l'objet `Game` et les objets du jeu.

La POO sera toujours reliée à une question de conception :

> Qui connaît cette information ? Qui doit modifier cette information ? Qui doit dessiner cet élément ?

### 3.3. Notions de création de jeu

La formation introduira également :

- le repère de l'écran ;
- les coordonnées en pixels ;
- les coordonnées d'une tilemap ;
- la boucle de jeu ;
- la différence entre logique et affichage ;
- la simulation discrète par images successives ;
- la vitesse et la gravité ;
- les collisions entre rectangles et avec une tilemap ;
- les états d'un objet ;
- les listes d'objets ;
- la suppression d'objets inactifs ;
- les scènes d'un jeu ;
- la victoire et la défaite.

---

## 4. Jeu fil rouge : le mini-platformer

### 4.1. Concept

Le fil rouge est un mini-platformer vu de côté. Le joueur doit traverser un niveau, éviter ou vaincre des ennemis, récupérer des objets et atteindre une sortie.

Le jeu devra comporter au minimum :

- un personnage contrôlé au clavier ;
- un déplacement horizontal ;
- la gravité ;
- un saut ;
- un sol et des plateformes ;
- un niveau réalisé avec une tilemap ;
- au moins un objet à ramasser ;
- au moins un ennemi ;
- un score ou un compteur ;
- une condition de victoire ;
- une condition de défaite ;
- une musique ;
- plusieurs bruitages ;
- une animation simple ;
- un écran titre et un écran de fin.

### 4.2. Ressources de la formation

Le fichier `res.pyxres` est fourni avec les leçons. Il est produit par le script `cours/pyxel-platformer/outils/generer_ressources.py`, qui construit l'archive à partir de petites images décrites en ASCII.

Contenu livré avec la leçon 2 :

#### Image bank 0

- frames du joueur au repos : tuiles (0, 0) et (1, 0) ;
- frames du joueur en déplacement : tuiles (2, 0) et (3, 0) ;
- ennemi : tuile (4, 0) ;
- dessus du sol : tuile (0, 1) ;
- remplissage du sol : tuile (1, 1) ;
- plateforme : tuile (2, 1) ;
- pièce : tuile (3, 1) ;
- buisson : tuile (4, 1).

#### Tilemap 0

Niveau de 64 × 32 tuiles, soit 512 × 256 pixels (deux écrans de large) :

- sol à partir de la ligne 28 ;
- trois plateformes étagées aux lignes 23, 19 et 15 ;
- dix-huit pièces, trois par plateforme, neuf par moitié ; elles deviennent des objets à la leçon 7 ;
- six buissons décoratifs sur le sol.

#### Sons

- son 0 : saut ;
- son 1 : pièce ;
- son 2 : collision ;
- sons 8 à 13 : mélodie et accompagnement de la musique 0.

#### Musiques

- musique 0 : thème du niveau, deux canaux.

Les ressources seront étendues au fil des leçons :

- sortie du niveau et cases spéciales ;
- cases de bord et cases spéciales ;
- bruitage de victoire ou de défaite ;
- musique de titre.

Le script de génération sert de référence reproductible : il permet de régénérer le fichier, de corriger un dessin ou d'ajouter une tuile sans dépendre d'un éditeur graphique.

### 4.3. Architecture finale visée

L'architecture finale sera contenue dans un seul fichier :

```python
import pyxel


# Constantes du jeu


class Level:
    def __init__(self):
        ...

    def update(self):
        ...

    def draw(self):
        ...


class Player:
    def __init__(self, x, y):
        ...

    def update(self):
        ...

    def draw(self):
        ...


class Coin:
    def __init__(self, x, y):
        ...

    def update(self):
        ...

    def draw(self):
        ...


class Enemy:
    def __init__(self, x, y):
        ...

    def update(self):
        ...

    def draw(self):
        ...


class Game:
    def __init__(self):
        pyxel.init(256, 256, title="Mon platformer")
        pyxel.load("res.pyxres")
        ...
        pyxel.run(self.update, self.draw)

    def update(self):
        ...

    def draw(self):
        ...


Game()
```

Cette structure est un modèle pédagogique. Les élèves pourront l'adapter, mais le cours conservera une version de référence lisible et stable.

---

## 5. Progression générale

La progression comporte quatre phases :

1. **Faire apparaître un jeu rapidement** ;
2. **Comprendre le joueur, les ressources et les collisions** ;
3. **Ajouter les objets et les règles** ;
4. **Finaliser et personnaliser un jeu pour la Nuit du Code**.

Chaque étape produit un état fonctionnel du jeu. Un élève doit pouvoir reprendre le code complet d'une étape sans avoir besoin de reconstituer plusieurs fichiers ou plusieurs modifications intermédiaires.

---

# 6. Plan détaillé des leçons

## Leçon 0 — Découvrir PyxelStudio dans Capytale

### Objectif

Prendre en main l'environnement en ligne et comprendre le format de travail à deux fichiers.

### Notions

- projet PyxelStudio ;
- éditeur de code ;
- éditeur de ressources ;
- exécution du jeu ;
- sauvegarde et téléchargement ;
- fichiers dans un même dossier.

### Pyxel utilisé

- première initialisation ;
- première fenêtre ;
- touche de sortie.

### Résultat

Un projet contenant :

```text
main.py
res.pyxres
```

Le programme affiche un message simple et peut être exécuté dans Capytale.

### Article

L'article expliquera :

- où écrire le code ;
- comment lancer le jeu ;
- comment ouvrir l'éditeur de ressources ;
- comment sauvegarder une ressource ;
- comment récupérer les deux fichiers ;
- pourquoi il ne faut pas renommer ou déplacer `res.pyxres` sans modifier `pyxel.load()`.

### Vidéo

La vidéo montrera l'interface et le résultat final avant d'expliquer les boutons.

---

## Leçon 1 — La boucle de jeu et la classe `Game`

### Objectifs

- comprendre `pyxel.init()` ;
- comprendre `pyxel.run()` ;
- distinguer `update()` et `draw()` ;
- introduire une première classe ;
- afficher un décor et un personnage simple.

### API

```python
pyxel.init()
pyxel.run()
pyxel.cls()
pyxel.rect()
pyxel.text()
pyxel.frame_count
```

### Structure

La première version contiendra uniquement :

```python
class Game:
    def __init__(self):
        ...

    def update(self):
        ...

    def draw(self):
        ...
```

### Notions Python

- définition d'une classe ;
- création d'un objet ;
- méthode ;
- `self` ;
- état conservé entre deux images.

### Défi facultatif

Faire clignoter ou déplacer un élément en utilisant `pyxel.frame_count`.

---

## Leçon 2 — Le fichier `.pyxres` dès le début

### Objectifs

- créer une image dans l'éditeur ;
- charger `res.pyxres` ;
- afficher un sprite ;
- comprendre une feuille de sprites ;
- créer une première tilemap ;
- créer un bruitage et une musique ;
- utiliser les ressources dans le programme.

### API

```python
pyxel.load()
pyxel.blt()
pyxel.bltm()
pyxel.play()
pyxel.playm()
pyxel.stop()
```

### Progression

1. Charger le fichier de ressource.
2. Afficher le personnage avec `blt()`.
3. Afficher une première bande de décor avec `bltm()`.
4. Jouer un son avec `play()`.
5. Jouer une musique avec `playm(..., loop=True)`.

### Points à expliquer

- le fichier `.pyxres` n'est pas un fichier Python ;
- le programme n'a pas besoin de connaître le contenu interne du fichier ;
- les coordonnées de `blt()` désignent une zone dans une image ;
- les coordonnées de `bltm()` désignent une zone dans une tilemap ;
- une couleur peut servir de couleur transparente pour un sprite.

### Défi facultatif

Modifier l'image du joueur et remplacer le son de collecte.

---

## Leçon 3 — Le joueur et les contrôles

### Objectifs

- créer la classe `Player` ;
- stocker la position du joueur ;
- déplacer le joueur horizontalement ;
- comprendre `btn()` ;
- empêcher le joueur de sortir de l'écran ;
- faire en sorte que le joueur se dessine lui-même.

### API

```python
pyxel.btn()
pyxel.KEY_LEFT
pyxel.KEY_RIGHT
pyxel.clamp()
pyxel.blt()
```

### Architecture

La classe `Game` possède un joueur :

```python
self.player = Player(40, 80)
```

Puis elle lui délègue son comportement :

```python
self.player.update()
self.player.draw()
```

### Notions Python

- attributs d'instance ;
- paramètres du constructeur ;
- plusieurs objets et indépendance de leur état.

### Défi facultatif

Ajouter une touche pour modifier temporairement la vitesse du joueur.

---

## Leçon 4 — Gravité et saut

### Objectifs

- introduire `dy` ;
- appliquer la gravité ;
- déclencher un saut ;
- distinguer `btn()` et `btnp()` ;
- empêcher le double saut ;
- savoir si le joueur est au sol.

### API

```python
pyxel.btnp()
pyxel.KEY_SPACE
pyxel.play()
```

### État du joueur

La classe `Player` pourra contenir :

```python
self.x
self.y
self.dx
self.dy
self.is_on_ground
```

### Concepts

- position ;
- vitesse ;
- accélération ;
- mise à jour image par image ;
- action continue et action ponctuelle.

### Défi facultatif

Modifier la hauteur du saut ou la force de gravité pour changer la sensation de jeu.

---

## Leçon 5 — Le niveau et la tilemap

### Objectifs

- comprendre les cases de 8 × 8 pixels ;
- distinguer pixels et cases ;
- construire un niveau dans l'éditeur ;
- afficher la tilemap ;
- créer la classe `Level` ;
- identifier les cases solides.

### API

```python
pyxel.tilemaps[0]
pyxel.bltm()
pyxel.tilemaps[0].pget()
```

### Classe `Level`

```python
class Level:
    def __init__(self):
        self.tilemap = pyxel.tilemaps[0]

    def update(self):
        pass

    def draw(self):
        pyxel.bltm(
            0,
            0,
            self.tilemap,
            0,
            0,
            pyxel.width,
            pyxel.height,
        )
```

### Concepts

- une tilemap comme donnée du niveau ;
- une case identifiée par deux coordonnées ;
- conversion pixel/case :

```python
tile_x = x // 8
tile_y = y // 8
```

### Défi facultatif

Ajouter une deuxième zone dans la tilemap et permettre au joueur d'y accéder.

---

## Leçon 6 — Les collisions avec la tilemap

### Objectifs

- utiliser `Tilemap.collide()` ;
- comprendre le rôle de la liste des cases qui sont des murs ;
- déplacer un rectangle dans un niveau ;
- empêcher le joueur de traverser le sol et les murs ;
- gérer séparément le déplacement horizontal et vertical si nécessaire.

### API

```python
pyxel.tilemaps[0].collide()
```

### Méthode visée

Une méthode de `Level` renvoie le déplacement autorisé :

```python
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
```

`collide()` renvoie un couple `(dx, dy)` corrigé, et non une position ; `walls` reçoit la liste des tuiles de la banque d’images, ici `SOLID_TILES`. Le joueur applique ensuite ce déplacement et en déduit son état « au sol ».

### Concepts

- rectangle englobant ;
- déplacement demandé et déplacement autorisé ;
- collision comme correction du mouvement ;
- sol, plafond et murs.

### Défi facultatif

Ajouter une plateforme traversable dans un seul sens, ou une case dangereuse.

---

## Leçon 7 — Ajouter plusieurs types d'objets

### Objectifs

- créer une classe `Coin` ;
- créer une classe `Enemy` ;
- créer plusieurs instances ;
- stocker les objets dans des listes ;
- appeler `update()` et `draw()` sur chaque objet.

### Structure

Les pièces existent déjà dans la tilemap : `Level.take_coins()` les efface en mémoire avec `pset()` et renvoie leurs positions, que `Game` transforme en objets.

```python
self.coins = []
for x, y in self.level.take_coins():
    self.coins.append(Coin(x, y))

self.enemies = [
    Enemy(88, 216, 88, 160),
    Enemy(104, 144, 104, 160),
]
```

Puis :

```python
for coin in self.coins:
    coin.update()

for enemy in self.enemies:
    enemy.update()
```

### Concepts

- classe et instance ;
- liste d'objets ;
- boucle de mise à jour ;
- boucle de dessin ;
- responsabilité d'un objet.

### Défi facultatif

Créer un deuxième type d'ennemi avec un comportement différent.

---

## Leçon 8 — Règles du jeu et cycle de vie des objets

### Objectifs

- détecter le contact entre le joueur et une pièce ;
- augmenter le score ;
- supprimer une pièce collectée ;
- détecter un contact avec un ennemi ;
- déclencher la défaite ;
- utiliser `is_alive` ;
- nettoyer les listes.

### API

```python
pyxel.play()
pyxel.text()
```

### Méthode de collision simple

Une méthode de `Game` teste deux objets, sans connaître leur classe :

```python
def collide(self, a, b):
    return (
        a.x < b.x + b.width
        and a.x + a.width > b.x
        and a.y < b.y + b.height
        and a.y + a.height > b.y
    )
```

Elle ne représente pas un objet de jeu ; elle décrit une opération géométrique générale. Les inégalités sont strictes : des bords jointifs ne sont pas un contact.

### Cycle de vie

Un objet reste dans sa liste jusqu'à la fin de la mise à jour, puis la liste est reconstruite :

```python
self.coins = [coin for coin in self.coins if coin.is_alive]
```

La compréhension de liste est expliquée dans l'article, avec la boucle classique équivalente.

### Défaite

`Game.is_game_over` passe à vrai au contact d'un ennemi ; `update()` sort immédiatement et le jeu se fige jusqu'au relancement du programme.

### Défi facultatif

Ajouter trois vies au lieu d'un game over immédiat.

---

## Leçon 9 — Animation et caméra

### Objectifs

- utiliser plusieurs images d'un sprite ;
- animer le joueur ;
- afficher une image différente pendant le saut ;
- retourner le sprite selon la direction ;
- faire défiler un niveau plus grand que l'écran ;
- utiliser la caméra.

### API

```python
pyxel.frame_count
pyxel.blt()
pyxel.camera()
```

### Concepts

- animation par changement de frame ;
- temps mesuré en images ;
- coordonnées du monde ;
- coordonnées de l'écran ;
- caméra comme décalage de dessin.

### Mise en œuvre retenue

- le niveau passe à 64 cases de large, soit 512 pixels : `LEVEL_WIDTH = 64` ;
- quatre tuiles du joueur : `(0, 0)` repos, `(1, 0)` saut, `(2, 0)` et `(3, 0)` marche ;
- `choose_tile()` choisit l'image en fin de `update()`, avec `pyxel.frame_count // 6 % 2` ;
- retournement par largeur négative, sans décaler `x` ;
- caméra centrée sur le joueur, bornée par `pyxel.clamp()` entre 0 et 256, remise à zéro avant l'interface ;
- le joueur est limité par `level.width`, plus par la fenêtre.

### Défi facultatif

Ajouter une animation particulière à l'ennemi ou à l'objet de sortie.

---

## Leçon 10 — Audio, interface et états du jeu

### Objectifs

- jouer la musique du niveau en boucle ;
- jouer un son lors d'un saut, d'une collecte ou d'un choc ;
- afficher un score ;
- créer un écran titre ;
- créer un écran de victoire ;
- créer un écran de game over ;
- redémarrer une partie.

### API

```python
pyxel.play()
pyxel.playm()
pyxel.stop()
pyxel.text()
pyxel.btnp()
```

### États proposés

```python
SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2
SCENE_WIN = 3
```

La classe `Game` pourra posséder :

```python
self.scene
self.score
self.lives
```

Les états ne seront pas transformés en architecture complexe. Quelques méthodes clairement nommées suffiront :

```python
def update_title(self):
    ...


def update_play(self):
    ...


def update_gameover(self):
    ...
```

### Mise en œuvre retenue

- quatre constantes d'état : `SCENE_TITLE = 0`, `SCENE_PLAY = 1`, `SCENE_GAMEOVER = 2`, `SCENE_WIN = 3` ;
- `update()` et `draw()` commencent par tester la touche `Q`, puis aiguillent par `if`/`elif` vers `update_title()`/`draw_title()`, `update_play()`/`draw_play()`, `update_gameover()`/`draw_gameover()` et `update_win()`/`draw_win()` ;
- `__init__()` ne crée aucun objet de jeu : il initialise `self.scene` et `self.score`, puis appelle `pyxel.run()` ;
- `start_game()`, appelée par la barre d'espace depuis le titre ou les écrans de fin, recharge `res.pyxres` avec `pyxel.load()`, construit le niveau, le joueur, les pièces et trois ennemis, remet le score à zéro, passe à `SCENE_PLAY` et lance `pyxel.playm(0, loop=True)` ;
- le rechargement est indispensable : `take_coins()` efface les tuiles de pièce, donc une deuxième partie sans `pyxel.load()` serait vide ;
- `update_play()` teste la victoire avant les ennemis, avec `return`, pour que la dernière pièce l'emporte sur un contact simultané ;
- `pyxel.stop()` coupe la musique à la victoire comme à la défaite ;
- interface en deux lignes seulement, « Score : n » et « Restantes : n », dessinées après la remise à zéro de la caméra ;
- textes dessinés sans accent ni cédille, la police intégrée de Pyxel ne contenant que l’ASCII (§7.10 de `cours/AGENTS.md`) ;
- `bltm()` reçoit la couleur 0 comme clé de transparence, pour que les cases vides laissent voir le fond ;
- écrans de titre et de fin centrés avec la règle des 4 pixels par caractère, colonne `(256 - 4 * len(texte)) // 2` ;
- `draw_gameover()` et `draw_win()` réutilisent `draw_play()` pour garder le décor figé derrière le message ;
- une seule musique dans la ressource : le défi « une musique par écran » reste une expérimentation, faute de seconde piste.

### Défi facultatif

Créer une musique différente pour l'écran titre et l'écran de victoire.

---

## Leçon 11 — Préparer son jeu pour la Nuit du Code

### Objectifs

- vérifier le fonctionnement complet du jeu ;
- contrôler la présence des deux fichiers attendus ;
- supprimer toute dépendance externe ;
- vérifier le chargement de `res.pyxres` ;
- équilibrer la difficulté ;
- ajouter une condition de victoire claire ;
- rendre le jeu rejouable ;
- personnaliser le niveau et les ressources.

### Checklist fonctionnelle

- Le jeu se lance sans erreur.
- `main.py` est le seul fichier Python nécessaire.
- `res.pyxres` est le seul fichier de ressources nécessaire.
- Le jeu fonctionne si les deux fichiers sont placés ensemble dans un nouveau dossier.
- Le joueur peut se déplacer.
- Le joueur peut sauter.
- Les collisions avec le niveau fonctionnent.
- Les ennemis ont un comportement visible.
- Les objets à ramasser fonctionnent.
- Le score est mis à jour.
- Les bruitages sont associés aux événements.
- La musique peut être arrêtée ou remplacée entre les scènes.
- Une victoire est possible.
- Une défaite est possible.
- Une nouvelle partie peut être lancée.

### Personnalisation

Les élèves pourront choisir au moins deux extensions :

- modifier le niveau ;
- ajouter une plateforme ;
- ajouter un ennemi ;
- ajouter une pièce spéciale ;
- ajouter des vies ;
- ajouter un compte à rebours ;
- créer une zone secrète ;
- ajouter un bonus temporaire ;
- créer une nouvelle animation ;
- modifier l'ambiance sonore.

Il ne s'agit pas d'une évaluation. La checklist sert uniquement à aider l'élève à obtenir un jeu réellement jouable.

### Mise en œuvre retenue

- le programme de cette leçon est celui de la leçon 10 : les règles du jeu ne changent pas ;
- deux retouches finales préparent la personnalisation : les colonnes de texte sont calculées, et les deux écrans de fin partagent une méthode ;
- `FONT_WIDTH = 4` et `Game.text_x(texte)` renvoient `(SCREEN_WIDTH - FONT_WIDTH * len(texte)) // 2`, ce qui remplace les colonnes écrites à la main ;
- l'écran titre devient une liste de couples `(texte, hauteur)` parcourue par une boucle ;
- `draw_end(message, color)` est appelé par `draw_gameover()` et `draw_win()` : les deux écrans ne diffèrent que par deux valeurs ;
- le bruitage de défaite est joué après `pyxel.stop()`, sinon l'arrêt de la musique l'interrompt ;
- le dossier livrable se vérifie en le copiant sous un autre nom, puis en le relançant depuis la copie ;
- la difficulté se règle avec quatre constantes : `PLAYER_SPEED`, `JUMP_SPEED`, `GRAVITY`, `ENEMY_SPEED` ;
- l'article contient la liste des quinze contrôles et le tableau des dix personnalisations, avec le point d'intervention de chacune ;
- la dernière page de l'article clôt la formation et renvoie au module bonus Pyxel Cube.

---

# 7. Module bonus : Pyxel Cube et la 3D

Ce module est placé après le parcours 2D. Il ne constitue pas une étape nécessaire pour participer à la Nuit du Code avec le mini-platformer.

Pyxel Cube utilise une organisation différente de la POO 2D simplifiée :

- les objets 3D sont des `Node` ;
- les comportements sont généralement placés dans `on_update()` et `on_draw()` ;
- les objets sont organisés dans un arbre de nœuds ;
- l'héritage depuis `Node` fait partie de l'API.

Cette différence sera explicitement signalée. Les règles `update()` et `draw()` du parcours 2D ne seront pas artificiellement imposées à l'API Cube.

## Cube 1 — Première scène 3D

### Objectifs

- importer `pyxel.cube` ;
- créer une scène ;
- créer une caméra ;
- dessiner un cube ;
- comprendre les coordonnées `x`, `y`, `z` ;
- faire tourner un objet.

### API

```python
from pyxel.cube import Camera, Mat4, Node, Shading, Vec3
```

### Ressources

La première scène utilisera uniquement des formes primitives générées par le code. Aucun fichier `.glb` ne sera nécessaire.

## Cube 2 — Objets, scène et transformations

### Objectifs

- créer plusieurs nœuds ;
- ajouter des enfants à une scène ;
- positionner les objets avec `Vec3` ;
- appliquer des transformations avec `Mat4` ;
- déplacer une caméra ;
- utiliser les entrées clavier.

### Concepts

- scène ;
- nœud ;
- position ;
- rotation ;
- transformation ;
- arbre de scène.

## Cube 3 — Vers un petit jeu 3D

### Objectifs possibles

- déplacement dans un espace 3D ;
- objets à ramasser ;
- caméra contrôlable ;
- collision simple ;
- découverte de `Collider` ;
- présentation des modèles `.glb` ;
- ouverture vers Blockbench.

Les quaternions, les meshes complexes, les animations importées et la physique complète seront réservés à des fiches avancées éventuelles.

---

# 8. Format éditorial de chaque leçon

Chaque leçon produite devra contenir les mêmes éléments.

## 8.1. Vidéo

Durée indicative : 8 à 20 minutes selon la difficulté.

Structure recommandée :

1. montrer le résultat final de la leçon ;
2. annoncer le problème à résoudre ;
3. rappeler les notions nécessaires ;
4. modifier le code ou expliquer les modifications ;
5. lancer le jeu ;
6. montrer une erreur fréquente si elle est utile ;
7. proposer un défi facultatif ;
8. annoncer la prochaine étape.

La vidéo ne devra pas simplement lire l'article. Elle montrera les décisions de programmation et le comportement du jeu.

## 8.2. Article

Les articles sont écrits en HTML, sans chaîne de production Quarto. Chaque page est autonome et importe la feuille de style commune `cours/pyxel-platformer/styles/article.css`.

Structure d'une page :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>…</title>
  <link rel="stylesheet" href="../styles/article.css">
</head>
<body>
  <article class="lesson">
    <header class="lesson-header">…</header>
    <nav class="lesson-toc">…</nav>
    …
  </article>
</body>
</html>
```

Les encadrés utilisent des classes explicites :

| Classe | Usage |
| --- | --- |
| `callout callout-note` | information complémentaire |
| `callout callout-tip` | conseil ou méthode |
| `callout callout-warning` | erreur fréquente ou piège |
| `callout callout-important` | règle à ne pas modifier |

Un encadré se présente ainsi :

```html
<aside class="callout callout-note">
  <p class="callout-title">Titre de l'encadré</p>
  <p>Texte de l'encadré.</p>
</aside>
```

Chaque article comprendra :

1. le résultat attendu ;
2. les objectifs ;
3. les prérequis ;
4. le vocabulaire nouveau ;
5. une explication de la notion ;
6. le code complet de `main.py` ;
7. le fichier `res.pyxres` correspondant ;
8. les étapes pour tester ;
9. les erreurs fréquentes ;
10. un défi facultatif ;
11. un lien vers la leçon suivante.

Les explications doivent privilégier des phrases courtes et des exemples directement modifiables. Le code affiché dans l'article doit être identique à celui de `main.py`.

## 8.3. Code source

Chaque état de la formation sera exécutable indépendamment :

```text
01_boucle/
  main.py
  res.pyxres

02_ressources/
  main.py
  res.pyxres

03_joueur/
  main.py
  res.pyxres
```

Le dossier de travail peut contenir les articles et les vidéos, mais le projet jouable de chaque étape ne contiendra que les deux fichiers prévus.

---

# 9. Organisation des fichiers dans le repository

L'organisation effectivement utilisée pendant la production est la suivante :

```text
cours/
  pyxel-platformer/
    styles/
      article.css
    outils/
      generer_ressources.py
      res.pyxres
    01-boucle-et-game/
      article.html
      script-video.md
      main.py
    02-ressources-pyxres/
      article.html
      script-video.md
      main.py
      res.pyxres
    03-joueur/
      article.html
      script-video.md
      main.py
      res.pyxres
    ...
    bonus-cube/
      ...
```

Règles appliquées :

- chaque dossier de leçon est autonome : `main.py` et, à partir de la leçon 2, `res.pyxres` peuvent être copiés dans PyxelStudio tels quels ;
- `article.html` contient l'article en HTML, avec une feuille de style commune `styles/article.css` ;
- `script-video.md` contient le script de la vidéo ;
- le fichier de ressources de référence est généré dans `outils/`, puis copié dans le dossier de la leçon ;
- les noms de dossiers pourront être adaptés au support final, mais la règle des deux fichiers du projet 2D reste constante ;
- les consignes de production, les conventions de code et les vérifications à exécuter sont décrites dans `cours/AGENTS.md`.

---

# 10. Fonctionnalités volontairement laissées de côté

Pour conserver une progression accessible, les fonctionnalités suivantes ne font pas partie du tronc commun :

- MML avancé ;
- sons PCM externes ;
- création de tons personnalisés ;
- polices externes ;
- images hors écran ;
- transformations graphiques avancées ;
- import TMX depuis Tiled ;
- bruit de Perlin ;
- palette personnalisée avancée ;
- création d'un `.pyxapp` ;
- publication HTML détaillée ;
- API avancée de données brutes ;
- physique 3D complète ;
- animation de modèles 3D complexes.

Ces thèmes pourront faire l'objet de fiches complémentaires après la formation principale.

---

# 11. Critères de réussite de la formation

La formation sera considérée comme aboutie si un élève débutant peut :

- lancer un projet Pyxel dans Capytale ;
- comprendre la boucle `update()` / `draw()` ;
- expliquer le rôle d'une classe et d'un objet ;
- créer un élément du jeu avec ses propres attributs, `update()` et `draw()` ;
- utiliser une ressource `.pyxres` ;
- construire une tilemap ;
- déplacer un joueur et le faire sauter ;
- gérer des collisions ;
- créer plusieurs ennemis ou objets ;
- associer des sons aux actions ;
- créer un écran de victoire et un écran de défaite ;
- personnaliser le jeu ;
- fournir un projet composé de `main.py` et `res.pyxres`.

Il n'y aura pas de note ni de contrôle final. La réussite se mesure par la capacité à créer et à modifier un jeu fonctionnel.

---

# 12. Points à verrouiller avant la production

Avant d'écrire les premières leçons, il faudra confirmer dans l'instance Capytale utilisée :

1. le nom exact attendu pour le fichier de ressources ;
2. la procédure d'ouverture et de sauvegarde de `res.pyxres` ;
3. la procédure de récupération des deux fichiers ;
4. le fonctionnement de `pyxel.load()` dans un projet téléchargé ;
5. la disponibilité de `Tilemap.collide()` dans Pyxel 3.0.1 ;
6. la disponibilité de `pyxel.cube` dans l'instance Capytale ;
7. la taille d'écran recommandée pour le mini-platformer ;
8. la durée souhaitée pour chaque vidéo et chaque article.

Ces vérifications ne changent pas l'architecture pédagogique du cours. Elles permettront de produire des consignes exactement adaptées à l'environnement utilisé par les élèves.
