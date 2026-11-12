# Leçon 3 — Le joueur et les contrôles

## Fiche de production

- **Formation :** Créer un mini-platformer 2D avec Pyxel
- **Public :** débutants en création de jeux, élèves de Première et Terminale NSI
- **Environnement :** PyxelStudio dans Capytale
- **Version ciblée :** Pyxel 3.0.1
- **Durée cible :** 12 à 14 minutes
- **Fichiers du projet :** `main.py` et `res.pyxres`
- **Ressource utilisée :** `res.pyxres` de la leçon 2, inchangée
- **Titre à l’écran :** Leçon 3 — Le joueur et les contrôles

## Intention pédagogique

Cette leçon remplace le déplacement automatique par un déplacement commandé au clavier.

Le travail porte sur trois points :

- lire l’état d’une touche avec `pyxel.btn()` ;
- calculer un déplacement à partir de cet état ;
- maintenir la position dans les limites de l’écran avec `pyxel.clamp()`.

La leçon supprime au passage le rebond automatique et son bruitage. Elle conserve la structure en classes et la séparation entre `update()` et `draw()`.

Le décor reste décoratif : aucune collision n’est calculée. Cette limite est annoncée explicitement dans la vidéo.

## Objectifs annoncés aux élèves

À la fin de la vidéo, l’élève doit pouvoir :

1. déplacer un objet avec les flèches du clavier ;
2. expliquer la différence entre `btn()` et `btnp()` ;
3. remettre un déplacement à zéro à chaque image ;
4. limiter une position avec `pyxel.clamp()` ;
5. modifier le comportement d’une classe sans changer son dessin.

## Préparation de l’enregistrement

### Fichiers

- `main.py` de la leçon 3, dans le dossier `03-joueur` ;
- `res.pyxres` recopié à côté de ce fichier.

### Vérifications avant d’enregistrer

- Le joueur est immobile au démarrage.
- Les deux flèches déplacent le joueur de 2 pixels par image.
- Le joueur s’arrête aux deux bords de l’écran.
- Le relâchement des touches arrête immédiatement le joueur.
- La touche `Q` ferme l’application.
- La musique se lance au démarrage.

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
PLAYER_SPEED = 2
PLAYER_TILE_X = 0
PLAYER_TILE_Y = 0
PLAYER_START_X = 40
PLAYER_START_Y = 216

BACKGROUND_COLOR = pyxel.COLOR_DARK_BLUE
TEXT_COLOR = pyxel.COLOR_WHITE
TRANSPARENT_COLOR = 0

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
        self.dx = 0

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
            title="Chapitre 3 - joueur",
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
            "Chapitre 3 - joueur",
            TEXT_COLOR,
        )
        pyxel.text(
            4,
            12,
            "Gauche et droite : marcher",
            TEXT_COLOR,
        )

        self.player.draw()


Game()
```

## Découpage détaillé

### 00:00 — Montrer le résultat

**À l’écran :** lancer le jeu. Le joueur est immobile. Les flèches le déplacent, il s’arrête aux bords.

**Narration :**

> Dans cette troisième leçon, le joueur ne se déplace plus tout seul : c’est le clavier qui commande ses déplacements.
>
> Les flèches gauche et droite le font avancer ou reculer. Il ne peut pas sortir de l’écran.
>
> Le décor et les ressources ne changent pas. Seul le comportement du personnage est modifié.

**Action :** déplacer le joueur d’un bord à l’autre, puis relâcher les touches au milieu de l’écran.

### 00:40 — Présenter les objectifs

**À l’écran :** afficher la liste :

```text
1. lire l’état d’une touche
2. calculer un déplacement
3. remettre le déplacement à zéro
4. rester dans l’écran
```

**Narration :**

> Quatre étapes suffisent pour rendre le personnage contrôlable.
>
> Il faut savoir si une touche est enfoncée, en déduire un déplacement, effacer ce déplacement quand aucune touche n’est pressée, puis empêcher le personnage de quitter la fenêtre.

### 01:20 — Retirer le déplacement automatique

**À l’écran :** ouvrir `main.py` et montrer la méthode `Player.update()` de la leçon 2.

```python
def update(self):
    self.x += self.dx

    if self.x <= 0:
        self.x = 0
        self.dx = abs(self.dx)
    elif self.x + self.width >= pyxel.width:
        self.x = pyxel.width - self.width
        self.dx = -abs(self.dx)
```

**Narration :**

> Dans la leçon précédente, le joueur avançait seul et changeait de sens aux bords.
>
> Ce comportement disparaît : nous n’avons plus besoin du rebond ni du bruitage déclenché à chaque changement de direction.
>
> Dans `Game.update()`, la détection du changement de direction est donc supprimée. Il ne reste que la lecture de la touche `Q` et l’appel à la mise à jour du joueur.

**Action :** supprimer dans `Game.update()` les lignes `direction`, la comparaison et `pyxel.play(0, BOUNCE_SOUND)`, puis supprimer la constante `BOUNCE_SOUND`.

### 02:20 — Initialiser le déplacement

**À l’écran :** modifier le constructeur :

```python
def __init__(self, x, y):
    self.x = x
    self.y = y
    self.width = PLAYER_WIDTH
    self.height = PLAYER_HEIGHT
    self.dx = 0
```

**Narration :**

> Le déplacement horizontal n’est plus une constante du joueur : il dépend des touches à chaque image.
>
> L’attribut `dx` vaut donc zéro au départ. Il sera recalculé à chaque mise à jour.

**À l’écran :** modifier la constante de vitesse :

```python
PLAYER_SPEED = 2
```

**Narration :**

> La vitesse passe de 1 à 2 pixels par image. Avec un déplacement manuel, 2 pixels donnent une réaction plus franche sans rendre le personnage trop rapide.

### 03:10 — Lire les flèches

**À l’écran :** écrire la nouvelle méthode :

```python
def update(self):
    self.dx = 0

    if pyxel.btn(pyxel.KEY_LEFT):
        self.dx = -PLAYER_SPEED
    elif pyxel.btn(pyxel.KEY_RIGHT):
        self.dx = PLAYER_SPEED
```

**Narration :**

> La méthode commence par remettre `dx` à zéro.
>
> Ensuite, `pyxel.btn()` indique si une touche est enfoncée à cet instant. Si la flèche gauche est pressée, le déplacement devient négatif : le joueur ira vers la gauche.
>
> Si la flèche droite est pressée, le déplacement devient positif.
>
> Le mot-clé `elif` signifie que la deuxième condition n’est testée que si la première est fausse. Lorsque les deux flèches sont enfoncées, la gauche l’emporte.

**Action :** montrer les deux touches pressées en même temps, puis relâcher.

### 05:00 — Distinguer `btn()` et `btnp()`

**À l’écran :** afficher la comparaison :

```text
btn()   vrai pendant tout l’appui     -> déplacement continu
btnp()  vrai seulement à l’appui      -> action ponctuelle
```

**Narration :**

> `pyxel.btnp()` a été utilisé dans les leçons précédentes pour quitter le jeu avec la touche `Q`. Il renvoie vrai uniquement pendant l’image où la touche est enfoncée.
>
> `pyxel.btn()` renvoie vrai tant que la touche reste enfoncée.
>
> Pour un déplacement, il faut la seconde fonction. Avec `btnp()`, le joueur avancerait d’un seul pas par appui et s’arrêterait.

**Action :** remplacer temporairement `btn()` par `btnp()`, exécuter, montrer le déplacement saccadé, puis revenir à `btn()`.

### 06:20 — Appliquer le déplacement

**À l’écran :** compléter la méthode :

```python
self.x += self.dx
```

**Narration :**

> Une fois le déplacement calculé, il suffit de l’ajouter à la position horizontale.
>
> Le signe de `dx` donne le sens : négatif vers la gauche, positif vers la droite, nul quand aucune touche n’est pressée.
>
> C’est la remise à zéro du début de méthode qui rend cette dernière propriété vraie : sans elle, le dernier déplacement resterait actif après le relâchement.

### 07:20 — Rester dans l’écran

**À l’écran :** ajouter :

```python
self.x = pyxel.clamp(
    self.x,
    0,
    pyxel.width - self.width,
)
```

**Narration :**

> `pyxel.clamp()` ramène une valeur dans un intervalle.
>
> Ici, la position doit rester entre zéro et la largeur de l’écran moins la largeur du joueur. Cette seconde borne correspond au moment où le bord droit du personnage touche le bord droit de la fenêtre.
>
> Cette seule ligne remplace les tests écrits dans la leçon précédente. La règle est décrite une seule fois, au même endroit.

**Action :** déplacer le joueur jusqu’aux deux bords pour montrer l’arrêt.

### 08:40 — Simplifier `Game.update()`

**À l’écran :** montrer la méthode finale :

```python
def update(self):
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

    self.player.update()
```

**Narration :**

> La classe `Game` reste courte. Elle vérifie la touche qui quitte le jeu et confie le reste au joueur.
>
> Le clavier est donc lu dans `Player.update()`. Cette répartition convient à un petit jeu : chaque élément décrit son propre comportement.
>
> Un programme plus important séparerait la lecture du clavier et le déplacement. Cette séparation n’est pas nécessaire ici.

### 09:30 — Exécuter et vérifier

**Action :** lancer le jeu et dérouler les vérifications suivantes.

**Narration :**

> Nous vérifions maintenant le comportement complet.
>
> Au démarrage, le joueur est immobile.
>
> La flèche droite le déplace régulièrement vers la droite ; la flèche gauche vers la gauche.
>
> Le relâchement l’arrête immédiatement, sans glissement.
>
> Aux bords, il s’arrête sans sortir de la fenêtre.
>
> Les plateformes n’arrêtent pas encore le personnage : aucune collision n’est calculée. Cette étape viendra plus tard.

### 10:40 — Erreurs fréquentes

**À l’écran :** afficher la liste :

```text
déplacement saccadé      -> btnp() au lieu de btn()
glissement après appui   -> self.dx = 0 oublié
sortie de l’écran        -> pyxel.clamp() absent ou mal ordonné
erreur de nom             -> pyxel.KEY_LEFT écrit autrement
```

**Narration :**

> Quatre problèmes sont fréquents.
>
> Un déplacement saccadé vient presque toujours de `btnp()` utilisé à la place de `btn()`.
>
> Un joueur qui continue d’avancer après le relâchement indique que `dx` n’a pas été remis à zéro au début de `update()`.
>
> Un personnage qui quitte l’écran indique que `pyxel.clamp()` est absent, ou placé avant la mise à jour de la position.
>
> Enfin, les constantes de touches s’écrivent en majuscules : `KEY_LEFT` et `KEY_RIGHT`.

**Action :** montrer l’erreur du glissement en supprimant temporairement la remise à zéro, puis rétablir.

### 12:00 — Expérimentations et conclusion

**À l’écran :** afficher la liste :

```text
- changer PLAYER_SPEED
- ajouter les touches A et D
- changer PLAYER_START_X
- retirer pyxel.clamp() pour observer son rôle
```

**Narration :**

> Trois modifications sont simples à essayer.
>
> Changer `PLAYER_SPEED` modifie la vitesse du personnage.
>
> Ajouter les touches `A` et `D` demande de compléter les deux conditions avec `or`.
>
> Changer `PLAYER_START_X` déplace le point de départ, sans toucher au reste du programme.
>
> Dans la prochaine leçon, le joueur reçoit une composante verticale : la gravité l’attire vers le sol et une touche déclenche un saut.

## Consignes de montage

- Afficher les noms `btn`, `btnp`, `dx` et `clamp` dans le zoom de code au moment où ils sont expliqués.
- Montrer en incrustation la comparaison entre `btn()` et `btnp()`.
- Laisser la musique audible à volume réduit pendant les phases de saisie.
- Montrer chaque vérification en exécutant réellement le jeu, sans accélérer la séquence.
- Conserver le même code final que l’article `article.qmd`.

## Vérification avant publication

- Le code compile et s’exécute avec Pyxel 3.0.1.
- La fenêtre mesure 256 × 256 pixels.
- Le joueur est immobile tant qu’aucune flèche n’est pressée.
- Chaque flèche produit un déplacement de 2 pixels par image.
- Les deux flèches enfoncées donnent la priorité à la gauche.
- Le joueur s’arrête entre 0 et 248 pixels.
- La touche `Q` quitte l’application.
- Le code affiché est identique à celui de l’article.
