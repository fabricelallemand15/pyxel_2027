# Bonus Cube 1 — Une première scène 3D

## Fiche de production

- **Formation :** Créer un mini-platformer 2D avec Pyxel — module bonus Pyxel Cube
- **Public :** élèves ayant terminé le parcours 2D, à l’aise avec les classes
- **Environnement :** PyxelStudio dans Capytale
- **Version ciblée :** Pyxel 3.0.1
- **Durée cible :** 10 à 11 minutes
- **Fichiers du projet :** `main.py` seulement, aucune ressource externe
- **Ressource utilisée :** aucune ; le sol et le cube sont dessinés par le code
- **Titre à l’écran :** Bonus Cube 1 — Une première scène 3D

## Intention pédagogique

Ce premier chapitre du module bonus change de moteur, pas de méthode : on garde les classes, les constantes nommées et la boucle de jeu.

Le chapitre introduit quatre objets mentaux :

- un nœud, qui se met à jour et se dessine tout seul ;
- une transformation, qui place et oriente un objet ;
- une caméra, qui projette la scène ;
- un arbre, qui contient tout le reste.

Le résultat tient en une fenêtre, un sol et un cube qui tourne. C’est volontairement court : en 3D, le programme minimal est déjà long, et il vaut mieux le comprendre entièrement que le décorer.

## Objectifs annoncés aux élèves

À la fin de la vidéo, l’élève doit pouvoir :

1. importer les classes de `pyxel.cube` ;
2. écrire une scène sous forme de sous-classe de `Node` ;
3. placer une caméra avec `Mat4.look_at()` ;
4. dessiner une boîte colorée ;
5. situer un objet avec ses trois coordonnées ;
6. faire tourner un objet ;
7. relier la scène à la fenêtre.

## Préparation de l’enregistrement

### Fichiers

- `main.py` du chapitre, dans le dossier `01-premiere-scene` ;
- aucun autre fichier : ni image, ni son, ni `res.pyxres`.

### Vérifications avant d’enregistrer

- Pyxel 3.0.1 est installé, et `from pyxel.cube import Camera` ne provoque pas d’erreur.
- La fenêtre mesure 256 sur 256 et s’intitule « Cube 1 - scene 3D ».
- Le sol est immobile, le cube tourne régulièrement.
- Le cube repose sur le sol, sans flottement ni enfoncement.
- Les faces du cube ont des teintes différentes.
- La touche `Q` ferme la fenêtre.

### Code final

```python
import pyxel
from pyxel.cube import Camera, Mat4, Node, Shading, Vec3


SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
BACKGROUND_COLOR = pyxel.COLOR_BLACK

GROUND_SIZE = 200.0
GROUND_COLOR = pyxel.COLOR_GREEN

CUBE_SIZE = 32.0
CUBE_COLOR = pyxel.COLOR_CYAN
CUBE_HEIGHT = 16.0
CUBE_SPEED = 1.0

CAMERA_HEIGHT = 60.0
CAMERA_DISTANCE = 140.0


class Ground(Node):
    def on_draw(self):
        self.box(
            Mat4.from_translation(Vec3(0.0, -1.0, 0.0)),
            Vec3(GROUND_SIZE, 2.0, GROUND_SIZE),
            GROUND_COLOR,
        )


class Cube(Node):
    def on_update(self):
        spin = Mat4.from_euler(
            Vec3(0.0, pyxel.frame_count * CUBE_SPEED, 0.0),
        )
        self.transform = (
            Mat4.from_translation(Vec3(0.0, CUBE_HEIGHT, 0.0)) * spin
        )

    def on_draw(self):
        self.box(
            Mat4.IDENTITY,
            Vec3(CUBE_SIZE, CUBE_SIZE, CUBE_SIZE),
            CUBE_COLOR,
        )


class Scene(Node):
    def __init__(self):
        super().__init__()

        self.shading = Shading(pyxel.colors)

        self.camera = Camera()
        self.camera.clear_color = BACKGROUND_COLOR
        self.camera.transform = Mat4.look_at(
            Vec3(0.0, CAMERA_HEIGHT, CAMERA_DISTANCE),
            Vec3(0.0, CUBE_HEIGHT, 0.0),
        )

        self.add_child(Ground())
        self.add_child(Cube())


class App:
    def __init__(self):
        pyxel.init(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            title="Cube 1 - scene 3D",
        )

        self.scene = Scene()

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.scene.update()

    def draw(self):
        self.scene.draw(0, 0, pyxel.width, pyxel.height)


App()
```

## Découpage détaillé

### 00:00 — Montrer le résultat

**À l’écran :** lancer le programme, laisser tourner le cube dix secondes, puis fermer avec `Q`.

**Narration :**

> Voici le premier programme du module bonus. Une fenêtre, un sol, et un cube qui tourne.
>
> C’est peu, et c’est exactement ce qu’il faut pour commencer. Ce cube contient les quatre pièces de toute scène 3D : un objet, une transformation, une caméra, et un dessin.
>
> Le reste du module ne fera qu’ajouter des objets et des mouvements à cette base.

**Action :** montrer une fois la scène sous un autre angle en modifiant la position de la caméra, puis revenir à la version du chapitre.

### 00:45 — Présenter les objectifs

**À l’écran :** afficher les trois points.

```text
1. importer pyxel.cube
2. écrire une scène
3. placer une caméra et tourner un cube
```

**Narration :**

> Trois étapes.
>
> D’abord les imports : la 3D vit dans un module séparé, `pyxel.cube`, livré avec Pyxel depuis la version 3.0.
>
> Ensuite la scène : une classe qui contient un sol, un cube, et la caméra.
>
> Enfin le dessin et la rotation : un appel à `box()` par objet, et un angle calculé à partir du numéro d’image.

### 01:30 — Le repère : x, y, z

**À l’écran :** afficher le tableau des trois axes, puis le cube seul dans la fenêtre.

```text
x : vers la droite
y : vers le haut
z : vers vous, hors de l’écran
```

**Narration :**

> Avant le code, une convention. En 3D, il y a trois axes.
>
> `x` va vers la droite, `y` vers le haut. Ce sont les deux axes du parcours 2D, à une différence près : en 2D, `y` descendait. En 3D, `y` monte.
>
> `z` sort de l’écran, vers vous. La caméra regarde vers les `z` négatifs : c’est pour cela que la scène est dessinée devant elle, et non derrière.
>
> Les unités sont libres. Une longueur de 32 vaut 32 unités de monde. C’est la caméra qui décide de la place que cela occupe à l’écran.

**Action :** déplacer le cube à `x = 40`, montrer qu’il sort du cadre, puis revenir à zéro.

### 03:00 — Importer Pyxel Cube

**À l’écran :** afficher les deux lignes d’import et les commenter une par une.

```python
import pyxel
from pyxel.cube import Camera, Mat4, Node, Shading, Vec3
```

**Narration :**

> Deux lignes d’import.
>
> `pyxel` comme d’habitude : la fenêtre, les touches, le temps.
>
> Puis cinq classes du module 3D. `Node` est un nœud de l’arbre de scène. `Camera` est le point de vue. `Vec3` est un vecteur à trois coordonnées, utilisé pour les positions et les tailles. `Mat4` est une matrice de transformation, utilisée pour placer et orienter. `Shading` est la table de luminosité qui donne du relief aux faces.
>
> Si l’import provoque une erreur indiquant que le module n’existe pas, la version de Pyxel est antérieure à 3.0. Ce module est récent : il faut la version 3.0.1 pour tout le module bonus.

### 03:40 — Le sol et le cube

**À l’écran :** afficher la classe `Ground`, puis la classe `Cube`.

```python
class Ground(Node):
    def on_draw(self):
        self.box(
            Mat4.from_translation(Vec3(0.0, -1.0, 0.0)),
            Vec3(GROUND_SIZE, 2.0, GROUND_SIZE),
            GROUND_COLOR,
        )
```

**Narration :**

> Une scène est un arbre de nœuds. Chaque objet est une sous-classe de `Node`, et redéfinit les méthodes dont il a besoin.
>
> Le sol redéfinit `on_draw()` seulement : il ne bouge pas, il n’a rien à mettre à jour.
>
> `box()` dessine une boîte pleine. Trois arguments : un placement, trois longueurs d’arête, une couleur.
>
> Le sol mesure 200 unités de côté et 2 d’épaisseur. Il est placé à `y = -1` : sa face supérieure tombe donc exactement sur zéro. C’est le repère de toute la scène.

**Action :** montrer le cube seul, puis le cube avec le sol, pour rendre visible l’alignement à zéro.

**Narration :**

> Le cube mesure 32 unités de côté. Son centre est à `y = 16`, c’est-à-dire la moitié de sa hauteur.
>
> Seize plus seize, trente-deux : la face inférieure du cube touche elle aussi zéro, et le cube paraît posé sur le sol. Un centre laissé à zéro l’enfoncerait à moitié.

### 05:20 — La caméra

**À l’écran :** afficher la classe `Scene` en entier.

```python
self.camera = Camera()
self.camera.clear_color = BACKGROUND_COLOR
self.camera.transform = Mat4.look_at(
    Vec3(0.0, CAMERA_HEIGHT, CAMERA_DISTANCE),
    Vec3(0.0, CUBE_HEIGHT, 0.0),
)
```

**Narration :**

> La scène est la racine de l’arbre. Elle porte trois choses.
>
> D’abord la lumière : `Shading(pyxel.colors)` construit une table de huit niveaux de luminosité pour chaque couleur de la palette. Sans elle, les six faces du cube auraient la même teinte, et le cube ressemblerait à un carré.
>
> Ensuite la caméra. Elle appartient à la scène, pas au cube. `draw()` l’utilise pour tout le sous-arbre.
>
> `clear_color` demande à remplir la fenêtre de noir avant de dessiner.
>
> `Mat4.look_at()` prend deux positions : celle de l’œil, et celle du point visé. L’œil est ici à 60 unités de haut et 140 unités devant la scène ; le point visé est le centre du cube.
>
> Les réglages par défaut suffisent : champ de vision de 60 degrés, objets visibles entre un dixième d’unité et mille unités.

**Action :** modifier `CAMERA_HEIGHT` à 200, montrer la vue de dessus, puis revenir à 60.

### 06:50 — La rotation

**À l’écran :** afficher `Cube.on_update()`.

```python
spin = Mat4.from_euler(
    Vec3(0.0, pyxel.frame_count * CUBE_SPEED, 0.0),
)
self.transform = (
    Mat4.from_translation(Vec3(0.0, CUBE_HEIGHT, 0.0)) * spin
)
```

**Narration :**

> Le cube a cette fois deux méthodes : il se dessine, et il se met à jour.
>
> `Mat4.from_euler()` construit une rotation à partir de trois angles, en degrés. Seul l’angle `y` change : le cube tourne sur lui-même comme une toupie.
>
> L’angle vaut le numéro d’image multiplié par un degré. À trente images par seconde, cela fait trente degrés par seconde, donc un tour complet en douze secondes.
>
> Puis la translation : translation fois rotation. La rotation d’abord, la translation ensuite. Si vous inversez les deux termes, le cube tourne autour du centre du monde au lieu de tourner sur place, et il décrit un grand cercle.
>
> Remarquez que la position est recalculée entièrement à chaque image. On n’ajoute jamais un degré à l’angle précédent : une addition répétée finit par dériver.

**Action :** montrer `CUBE_SPEED` à 5, puis à 0, puis revenir à 1.

### 08:10 — La fenêtre et la boucle

**À l’écran :** afficher la classe `App`.

**Narration :**

> La classe `App` ne fait que relier la scène à Pyxel.
>
> `pyxel.init()` ouvre une fenêtre de 256 sur 256 avec un titre. `pyxel.run()` prend la main et appelle `update()` puis `draw()` à chaque image.
>
> `update()` traite la touche `Q`, puis appelle `update()` sur la scène : la scène parcourt son arbre et exécute les mises à jour.
>
> `draw()` appelle `draw()` sur la scène, avec la zone de dessin complète. La scène parcourt à nouveau son arbre, cette fois pour dessiner, avec la caméra trouvée sur la racine.
>
> Deux appels, et tout l’arbre vit. Les chapitres suivants n’ajouteront que des nœuds.

### 09:00 — Erreurs fréquentes

**À l’écran :** provoquer trois erreurs, une par une, et les corriger.

```text
aucune caméra : rien ne s’affiche
update() oublié : le cube est figé
centre à y = 0 : le cube est enterré
```

**Narration :**

> Trois erreurs reviennent tout le temps.
>
> Si aucune caméra n’est créée sur la scène, le dessin ne peut pas projeter la scène, et la fenêtre reste noire.
>
> Si `self.scene.update()` manque dans `App.update()`, l’image est parfaite mais figée : le cube ne tourne pas.
>
> Si le centre du cube est laissé à zéro, la moitié du cube passe sous le sol. Le centre d’un objet posé sur un sol à zéro vaut la moitié de sa hauteur.
>
> Une quatrième erreur, plus discrète : passer `self.transform` à `box()` au lieu de `Mat4.IDENTITY`. Le placement serait alors appliqué deux fois, et le cube se retrouverait à deux fois sa position.

### 09:50 — Personnaliser

**À l’écran :** afficher le tableau des réglages, puis appliquer deux modifications.

```text
CUBE_SIZE, CUBE_COLOR, CUBE_SPEED
CAMERA_HEIGHT, CAMERA_DISTANCE
GROUND_SIZE
```

**Narration :**

> Chaque réglage a sa constante.
>
> La taille du cube, sa couleur, sa vitesse de rotation. La hauteur et la distance de la caméra. La taille du sol.
>
> Deux exercices pour finir. Le premier : placer le cube à `x = 40`, et décaler le point visé par la caméra de la même valeur, pour qu’il reste au centre de l’image.
>
> Le second : ajouter un second cube, plus petit, à côté du premier. La caméra est déjà partagée, puisqu’elle appartient à la scène.

**Action :** faire l’exercice du second cube à l’écran, en trois lignes.

### 10:40 — À retenir

**À l’écran :** afficher les quatre phrases, puis la scène finale.

```text
un nœud se met à jour et se dessine
la scène porte la caméra
translation puis rotation
deux appels font vivre l’arbre
```

**Narration :**

> Quatre phrases à retenir.
>
> Un nœud se met à jour et se dessine : on ne l’appelle jamais directement, c’est la scène qui parcourt son arbre.
>
> La scène porte la caméra : elle vaut pour tout le sous-arbre.
>
> La translation se multiplie après la rotation, sinon l’objet tourne autour du monde.
>
> Et deux appels, `update()` et `draw()` sur la scène, suffisent à faire vivre l’arbre entier.
>
> Le chapitre suivant peuple cette scène : un objet parent qui entraîne ses enfants, et une caméra que le clavier fait tourner.

## Consignes de montage

- Montrer le cube qui tourne avant toute explication de code.
- Afficher le tableau des trois axes pendant l’explication du repère.
- Garder le code des deux classes visibles quand on parle de `box()`.
- Montrer le lien entre `y = 16`, la taille 32 et le contact avec le sol, avec un trait à l’écran.
- Faire varier `CAMERA_HEIGHT` en direct, puis revenir à la valeur du chapitre.
- Provoquer les trois erreurs en direct, sans couper.
- Conserver le même code final que l’article `article.qmd`.

## Vérification avant publication

- Le code compile et s’exécute avec Pyxel 3.0.1.
- `from pyxel.cube import Camera, Mat4, Node, Shading, Vec3` fonctionne.
- La fenêtre s’intitule « Cube 1 - scene 3D » et mesure 256 sur 256.
- Le sol est immobile, le cube tourne, le cube repose sur le sol.
- La touche `Q` ferme la fenêtre.
- Aucun texte affiché ne contient d’accent.
- Le code affiché est identique à celui de l’article.
