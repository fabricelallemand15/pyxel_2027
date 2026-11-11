# Leçon 1 — La boucle de jeu et la classe `Game`

## Fiche de production

- **Formation :** Créer un mini-platformer 2D avec Pyxel
- **Public :** débutants en création de jeux, élèves de Première et Terminale NSI
- **Environnement :** PyxelStudio dans Capytale
- **Version ciblée :** Pyxel 3.0.1
- **Durée cible :** 13 à 15 minutes
- **Fichier produit :** `main.py`
- **Ressource utilisée :** aucune dans cette leçon
- **Ressource introduite dans la leçon suivante :** `res.pyxres`
- **Titre à l’écran :** Leçon 1 — La boucle de jeu et la classe `Game`

## Intention pédagogique

Cette première leçon présente le fonctionnement minimal d’une application Pyxel et introduit la POO à travers deux classes : `Game` et `Player`.

Le joueur est représenté par un rectangle qui se déplace automatiquement et rebondit sur les bords de l’écran. Les contrôles ne sont pas encore étudiés. Cette limitation permet de concentrer la leçon sur :

- la création d’une fenêtre ;
- la boucle de jeu ;
- la séparation entre mise à jour et dessin ;
- les attributs et les méthodes ;
- la relation entre `Game` et `Player`.

Les ressources graphiques et le fichier `.pyxres` seront introduits au début de la leçon 2. Le choix d’un rectangle dans cette première vidéo permet de distinguer le fonctionnement du programme de la gestion des ressources.

## Objectifs annoncés aux élèves

À la fin de la vidéo, l’élève doit pouvoir :

1. créer une fenêtre Pyxel avec `pyxel.init()` ;
2. lancer une boucle de jeu avec `pyxel.run()` ;
3. expliquer le rôle de `update()` et de `draw()` ;
4. créer une classe simple avec `__init__()` ;
5. stocker l’état d’un objet dans ses attributs ;
6. faire évoluer et dessiner un objet avec ses propres méthodes.

## Préparation de l’enregistrement

### Projet

Ouvrir PyxelStudio dans Capytale et créer un projet avec l’éditeur de code.

Le fichier de code utilisé dans la vidéo est `main.py`. Si PyxelStudio a déjà créé une ressource `res.pyxres`, la conserver dans le projet, mais ne pas la charger dans cette leçon.

### Code final

Le code affiché à la fin de la vidéo est le suivant :

```python
import pyxel


SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
GROUND_Y = 224

PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLAYER_SPEED = 1

BACKGROUND_COLOR = pyxel.COLOR_DARK_BLUE
GROUND_COLOR = pyxel.COLOR_GREEN
PLAYER_COLOR = pyxel.COLOR_YELLOW
TEXT_COLOR = pyxel.COLOR_WHITE


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
        pyxel.rect(
            self.x,
            self.y,
            self.width,
            self.height,
            PLAYER_COLOR,
        )


class Game:
    def __init__(self):
        pyxel.init(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            title="Leçon 1 - Boucle de jeu",
        )

        self.player = Player(
            20,
            GROUND_Y - PLAYER_HEIGHT,
        )

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.player.update()

    def draw(self):
        pyxel.cls(BACKGROUND_COLOR)
        pyxel.rect(
            0,
            GROUND_Y,
            pyxel.width,
            pyxel.height - GROUND_Y,
            GROUND_COLOR,
        )
        pyxel.text(
            4,
            4,
            "Leçon 1 - boucle de jeu",
            TEXT_COLOR,
        )
        pyxel.text(
            4,
            12,
            f"Image {pyxel.frame_count}",
            TEXT_COLOR,
        )

        self.player.draw()


Game()
```

## Découpage détaillé

### 00:00 — Montrer le résultat

**À l’écran :** afficher directement le jeu en fonctionnement. Le rectangle jaune se déplace au-dessus d’un sol vert. Le texte indique le numéro d’image courant.

**Narration :**

> Dans cette première leçon, nous allons créer la structure minimale d’un jeu Pyxel.
>
> La fenêtre contient un décor, un joueur représenté provisoirement par un rectangle et une boucle qui met le jeu à jour image après image.
>
> Le joueur se déplace automatiquement. Les contrôles et les images importées seront étudiés dans les prochaines leçons.

**Action :** laisser le programme fonctionner quelques secondes, puis arrêter l’exécution.

### 00:35 — Présenter les objectifs

**À l’écran :** afficher une diapositive avec les quatre notions suivantes :

```text
1. initialiser Pyxel
2. mettre à jour l’état du jeu
3. dessiner l’état courant
4. organiser le programme avec des classes
```

**Narration :**

> Un jeu vidéo peut être décrit comme une succession d’images.
>
> Entre deux images, le programme modifie l’état du jeu : une position change, un compteur augmente ou une collision est détectée.
>
> Ensuite, le programme dessine l’état obtenu.
>
> Pyxel fournit cette boucle de fonctionnement. Nous allons placer notre code dans deux méthodes : `update()` pour la logique et `draw()` pour l’affichage.

### 01:15 — Présenter le projet dans PyxelStudio

**À l’écran :** montrer PyxelStudio dans Capytale, avec l’éditeur de code et la zone d’exécution.

**Narration :**

> Le cours utilise PyxelStudio dans Capytale.
>
> Le code du jeu sera écrit dans `main.py`. Le projet final utilisera également un fichier `res.pyxres` placé dans le même dossier. Ce fichier contiendra les images, la tilemap, les sons et la musique.
>
> Nous n’utiliserons pas encore cette ressource. Pour isoler la boucle de jeu, cette première version dessine uniquement des formes géométriques.

**Action :** sélectionner tout le contenu de l’éditeur et le supprimer.

### 01:55 — Importer Pyxel et définir les constantes

**À l’écran :** saisir :

```python
import pyxel
```

Puis ajouter les constantes :

```python
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
GROUND_Y = 224

PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLAYER_SPEED = 1
```

**Narration :**

> La première ligne importe le module Pyxel. Elle permet d’utiliser les fonctions et les constantes de la bibliothèque.
>
> Nous définissons ensuite les dimensions de l’écran, la hauteur du sol et les dimensions du joueur.
>
> Les deux premières valeurs fixent la taille de la fenêtre : 256 pixels sur 256. C'est l'une des deux tailles autorisées par le règlement de la Nuit du Code, avec 128 sur 128. La formation conserve 256 sur 256.
>
> Une constante est un nom donné à une valeur utilisée à plusieurs endroits. Ici, `PLAYER_WIDTH` et `PLAYER_HEIGHT` décrivent la taille du joueur. Cela évite de recopier plusieurs fois les nombres 8 dans le programme.

**À l’écran :** ajouter les couleurs :

```python
BACKGROUND_COLOR = pyxel.COLOR_DARK_BLUE
GROUND_COLOR = pyxel.COLOR_GREEN
PLAYER_COLOR = pyxel.COLOR_YELLOW
TEXT_COLOR = pyxel.COLOR_WHITE
```

**Narration :**

> Pyxel fournit des constantes pour les couleurs de sa palette. Leur nom est plus lisible qu’un nombre de couleur écrit directement dans le programme.

### 02:50 — Créer la classe `Player`

**À l’écran :** saisir :

```python
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.dx = PLAYER_SPEED
```

**Narration :**

> Le joueur est un élément du jeu. Nous le représentons donc par une classe `Player`.
>
> La méthode `__init__()` est appelée lors de la création d’un objet. Elle reçoit la position initiale `x` et `y`.
>
> Les expressions `self.x` et `self.y` sont les attributs de l’objet. Chaque joueur possède sa propre position.
>
> L’attribut `dx` représente le déplacement horizontal effectué à chaque image. Nous lui donnons la valeur `PLAYER_SPEED`.
>
> Pour l’instant, ce déplacement est automatique. La gestion du clavier sera ajoutée plus tard.

**À l’écran :** afficher une courte comparaison :

```python
Player       # la classe, le modèle
player       # un objet créé à partir de cette classe
```

**Narration :**

> `Player` est le modèle qui décrit ce qu’est un joueur. Un objet, comme `player`, sera une instance concrète de cette classe.

### 04:20 — Écrire `Player.update()`

**À l’écran :** ajouter :

```python
    def update(self):
        self.x += self.dx
```

**Narration :**

> La méthode `update()` décrit l’évolution du joueur pendant une image.
>
> Ici, on ajoute `dx` à `x`. Si `dx` vaut 1, le joueur avance d’un pixel à chaque image.
>
> Cette méthode modifie l’état de l’objet, mais elle ne dessine rien.

**À l’écran :** ajouter la gestion des bords :

```python
        if self.x <= 0:
            self.x = 0
            self.dx = abs(self.dx)
        elif self.x + self.width >= pyxel.width:
            self.x = pyxel.width - self.width
            self.dx = -abs(self.dx)
```

**Narration :**

> Le joueur ne doit pas sortir de l’écran.
>
> Lorsqu’il atteint le bord gauche, nous plaçons sa position à zéro et nous rendons `dx` positif.
>
> Lorsqu’il atteint le bord droit, nous plaçons son bord droit à la largeur de l’écran et nous rendons `dx` négatif.
>
> La fonction `abs()` permet d’obtenir une valeur positive. Le signe de `dx` indique donc le sens du déplacement.

**Action :** exécuter brièvement le programme si la classe est temporairement incomplète, puis continuer sans commenter une éventuelle erreur de syntaxe intermédiaire.

### 06:10 — Écrire `Player.draw()`

**À l’écran :** ajouter :

```python
    def draw(self):
        pyxel.rect(
            self.x,
            self.y,
            self.width,
            self.height,
            PLAYER_COLOR,
        )
```

**Narration :**

> La méthode `draw()` décrit l’apparence de l’objet.
>
> Elle utilise `pyxel.rect()` pour dessiner un rectangle à la position de l’objet, avec sa largeur, sa hauteur et sa couleur.
>
> La position est lue dans les attributs `self.x` et `self.y`. La méthode ne modifie pas la position.
>
> Cette séparation entre `update()` et `draw()` sera conservée pour tous les éléments du jeu.

### 07:15 — Créer la classe `Game`

**À l’écran :** saisir :

```python
class Game:
    def __init__(self):
        pyxel.init(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            title="Leçon 1 - Boucle de jeu",
        )
```

**Narration :**

> La classe `Game` représente le jeu lui-même. Elle possède les objets et coordonne leur mise à jour et leur affichage.
>
> Dans son constructeur, nous initialisons Pyxel avec la largeur, la hauteur et le titre de la fenêtre.

**À l’écran :** ajouter la création du joueur :

```python
        self.player = Player(
            20,
            GROUND_Y - PLAYER_HEIGHT,
        )
```

**Narration :**

> Nous créons maintenant un objet `Player`.
>
> Le joueur commence à la position x égale à 20. Sa position verticale est calculée pour que son bas soit posé sur le sol.
>
> L’objet est stocké dans `self.player`. La classe `Game` pourra donc lui demander de se mettre à jour et de se dessiner.

**À l’écran :** ajouter :

```python
        pyxel.run(self.update, self.draw)
```

**Narration :**

> `pyxel.run()` lance l’application.
>
> Nous lui transmettons les deux méthodes de l’objet `Game` : `self.update` et `self.draw`.
>
> Pyxel appellera ces méthodes pendant l’exécution du jeu.

### 09:00 — Écrire `Game.update()`

**À l’écran :** ajouter :

```python
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.player.update()
```

**Narration :**

> Dans `Game.update()`, nous plaçons la logique générale du jeu.
>
> La touche Q permet de quitter l’application. `btnp()` renvoie vrai au moment où la touche est pressée. Nous l’étudierons plus précisément lorsque nous ajouterons les contrôles du joueur.
>
> Ensuite, le jeu demande au joueur de mettre à jour son propre état.
>
> `Game` coordonne ; `Player` connaît la manière dont un joueur se déplace.

### 10:00 — Écrire `Game.draw()`

**À l’écran :** ajouter :

```python
    def draw(self):
        pyxel.cls(BACKGROUND_COLOR)
        pyxel.rect(
            0,
            GROUND_Y,
            pyxel.width,
            pyxel.height - GROUND_Y,
            GROUND_COLOR,
        )
```

**Narration :**

> Dans `Game.draw()`, nous commençons par effacer l’écran avec `pyxel.cls()`.
>
> Puis nous dessinons le sol comme un grand rectangle qui commence à la hauteur `GROUND_Y`.
>
> L’écran est redessiné à chaque image. Il ne faut donc pas penser que le rectangle du joueur reste automatiquement présent : il est redessiné par `Player.draw()` à chaque appel de `draw()`.

**À l’écran :** ajouter le texte :

```python
        pyxel.text(
            4,
            4,
            "Leçon 1 - boucle de jeu",
            TEXT_COLOR,
        )
        pyxel.text(
            4,
            12,
            f"Image {pyxel.frame_count}",
            TEXT_COLOR,
        )
```

**Narration :**

> `pyxel.text()` affiche deux informations : le nom de la leçon et le numéro de l’image courant.
>
> `pyxel.frame_count` est un compteur fourni par Pyxel. Il augmente au fil de l’exécution et permet notamment de créer des animations.

**À l’écran :** terminer `draw()` avec :

```python
        self.player.draw()
```

**Narration :**

> Pour finir, `Game` demande au joueur de se dessiner.
>
> La méthode `Game.draw()` ne connaît pas les détails du dessin du joueur. Elle lui délègue cette responsabilité.

### 11:45 — Créer le premier objet `Game`

**À l’écran :** placer tout en bas du fichier :

```python
Game()
```

**Narration :**

> Les classes décrivent des modèles, mais elles ne créent pas automatiquement d’objet.
>
> La dernière ligne crée un objet `Game`. Son constructeur initialise Pyxel, crée le joueur et lance la boucle de jeu.
>
> Sans cette ligne, le fichier contiendrait seulement des définitions et aucune fenêtre ne s’ouvrirait.

### 12:15 — Exécuter et vérifier

**Action :** lancer le programme dans PyxelStudio.

**Résultat attendu :**

- une fenêtre de 256 par 256 pixels ;
- un fond bleu foncé ;
- un sol vert ;
- un carré jaune qui se déplace et rebondit ;
- le numéro d’image qui augmente ;
- la touche Q qui ferme le programme.

**Narration :**

> Le programme fonctionne maintenant avec une boucle de jeu complète.
>
> À chaque image, `Game.update()` met à jour le joueur. Puis `Game.draw()` efface l’écran, dessine le décor, affiche le texte et demande au joueur de se dessiner.
>
> La prochaine leçon remplacera progressivement les formes géométriques par des éléments créés dans le fichier `res.pyxres`.

### 12:55 — Erreurs fréquentes

**À l’écran :** afficher la liste suivante :

```text
NameError        : nom mal écrit ou classe utilisée avant sa définition
IndentationError : indentation incorrecte dans une classe ou une méthode
AttributeError   : oubli de self ou attribut mal nommé
Fenêtre absente  : oubli de Game()
```

**Narration :**

> Quatre erreurs sont fréquentes dans ce premier programme.
>
> Une erreur `NameError` indique souvent qu’un nom est mal écrit.
>
> Une erreur `IndentationError` concerne l’alignement du code. Le contenu d’une classe ou d’une méthode doit être indenté.
>
> Une erreur `AttributeError` apparaît lorsqu’un attribut est mal nommé ou lorsque `self` a été oublié.
>
> Enfin, si aucune fenêtre ne s’ouvre, vérifier que la dernière ligne `Game()` est présente.

### 13:45 — Défi facultatif et conclusion

**À l’écran :** afficher :

```text
Défi : modifier le déplacement automatique du joueur.

- changer sa vitesse ;
- changer sa couleur ;
- changer la hauteur du sol ;
- ajouter un second joueur immobile.
```

**Narration :**

> Pour terminer, vous pouvez modifier une constante, changer la couleur du joueur ou ajouter un second objet.
>
> Si vous ajoutez un second joueur, il devra être créé comme un nouvel objet `Player`.
>
> Dans la prochaine leçon, nous utiliserons l’éditeur de ressources et le fichier `res.pyxres` pour importer des images, une tilemap, des sons et une musique.

## Consignes de montage

- Utiliser une capture de l’écran complet uniquement lors de la présentation de PyxelStudio.
- Utiliser un cadrage rapproché de l’éditeur lors de la saisie des classes.
- Afficher les mots `update`, `draw`, `self.player` et `pyxel.run()` dans le zoom de code lorsque ces éléments sont expliqués.
- Ne pas ajouter de musique de fond à la vidéo : la musique Pyxel sera introduite dans la leçon 2.
- Conserver le même code final dans la vidéo et dans l’article.
- Ne pas afficher de ressource graphique externe dans cette leçon.

## Vérification avant publication

- Le code final s’exécute avec Pyxel 3.0.1.
- Le programme fonctionne dans PyxelStudio dans Capytale.
- La touche Q quitte bien l’application.
- Le joueur ne dépasse pas les bords de l’écran.
- Le joueur reste posé sur le sol.
- Le numéro d’image est visible.
- Le code présenté dans la vidéo est identique au code de l’article `.qmd`.
- La vidéo ne suppose pas que la POO ou le fichier `.pyxres` ont déjà été étudiés.
