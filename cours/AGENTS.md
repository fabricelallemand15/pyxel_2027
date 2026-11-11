# Production du cours Pyxel — consignes de travail

Ce fichier décrit le contexte, les conventions et les vérifications à respecter pour produire la suite du cours Pyxel contenu dans `cours/pyxel-platformer/`.

Il s’adresse à toute personne ou à tout agent qui reprend la production. Il complète le plan détaillé et ne le remplace pas.

## 1. Documents de référence

| Document | Rôle |
| --- | --- |
| `docs/plan-formation-pyxel.md` | Référence de fond : finalité, progression des leçons 0 à 11, architecture visée, module bonus |
| `cours/AGENTS.md` | Le présent document : consignes de production et conventions |
| `AGENTS.md` à la racine | Règles générales du dépôt Pyxel |
| `docs/api-reference.md` | API exacte de Pyxel 3.0.1 |
| `docs/editor-manual.md` | Éditeur d’images, de tilemaps, de sons et de musiques |
| `docs/pyxres-format.md` | Structure du fichier `.pyxres` |
| `docs/user-guide.md` | Boucle `update` / `draw`, ressources, distribution |

En cas de contradiction entre ce fichier et le plan, appliquer le plan pour le fond pédagogique et ce fichier pour la forme. Signaler la contradiction plutôt que de la masquer.

## 2. Public et objectif

- Public : élèves de Première et Terminale NSI, débutants en création de jeux.
- Objectif : produire un mini-platformer 2D complet et préparer la participation à la Nuit du Code.
- Environnement d’exécution : PyxelStudio dans Capytale, avec Pyxel 3.0.1.
- Le fil rouge est un platformer vu de côté. La chasse au trésor vue du dessus est réservée à un second tutoriel, après celui-ci.
- La 3D avec Pyxel Cube est un bonus de fin de formation, hors progression 2D.
- Aucune évaluation scolaire, aucun barème : les exercices et défis sont facultatifs.

## 3. Contraintes non négociables

| Contrainte | Portée |
| --- | --- |
| Un seul fichier `main.py` | Tout le code Python du jeu, y compris toutes les classes |
| Un seul fichier `res.pyxres` | Placé dans le même dossier que `main.py` |
| Fenêtre 256 × 256 pixels | Toute la formation ; 128 × 128 est seulement mentionné comme variante autorisée |
| Tuiles de 8 × 8 pixels | Banque d’images et tilemap |
| Niveau de 32 × 32 tuiles | Remplit exactement l’écran 256 × 256 |
| Pyxel 3.0.1 | Signatures de l’API de cette version, par exemple `pyxel.play(ch, snd)` |
| PyxelStudio dans Capytale | Environnement principal ; ni installation locale, ni VS Code comme parcours par défaut |
| POO obligatoire | Une classe par type d’élément du jeu |
| Méthodes `update()` et `draw()` | Pour chaque objet qui évolue et s’affiche |
| Code simple | Pas de décoration, pas de construction avancée |

Le dépôt public historique en Pyxel 1.8.8 n’est pas la référence technique : ne pas s’en inspirer pour le code.

## 4. État de la production

| Leçon | Dossier | État |
| --- | --- | --- |
| 0 — Découvrir PyxelStudio | aucun | non produite |
| 1 — Boucle de jeu et classe `Game` | `01-boucle-et-game/` | produite |
| 2 — Fichier de ressources `.pyxres` | `02-ressources-pyxres/` | produite |
| 3 — Joueur et contrôles | `03-joueur/` | produite |
| 4 — Gravité et saut | `04-gravite-et-saut/` | produite |
| 5 — Niveau et tilemap | `05-tilemap/` | produite |
| 6 — Collisions avec la tilemap | `06-collisions/` | produite |
| 7 — Plusieurs types d’objets | `07-objets/` | produite |
| 8 — Règles du jeu | `08-regles-du-jeu/` | produite |
| 9 — Animation et caméra | `09-animation-et-camera/` | à produire |
| 10 — Audio, interface, états | `10-audio-et-scenes/` | à produire |
| 11 — Préparation Nuit du Code | `11-nuit-du-code/` | à produire |
| Bonus — Pyxel Cube | `bonus-cube/` | à produire |

Une leçon n’est terminée que si ses trois livrables existent : `main.py`, `article.html`, `script-video.md`. À partir de la leçon 2, `res.pyxres` s’y ajoute.

## 5. Arborescence et nommage

```text
cours/
  AGENTS.md
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
    ...
```

Règles :

- nom de dossier de leçon : `NN-nom-court`, numéro sur deux chiffres, mots en minuscules séparés par des tirets ;
- un dossier de leçon est autonome : on doit pouvoir copier `main.py` et `res.pyxres` dans PyxelStudio sans rien chercher ailleurs ;
- `res.pyxres` est généré dans `outils/`, puis recopié à l’identique dans chaque dossier de leçon qui l’utilise ;
- aucun fichier généré inutile (`__pycache__`, archives temporaires) ne doit être commité.

## 6. Contenu attendu d’une leçon

### 6.1. Code

- Le code livré est le code complet et exécutable de la leçon, pas un fragment.
- Il reprend le code de la leçon précédente et n’introduit que les changements annoncés.
- Il doit tenir dans un seul fichier et ne dépendre que de `res.pyxres`.
- Il se lance tel quel dans PyxelStudio.

### 6.2. Article

L’article est écrit en HTML autonome, sans chaîne de production et sans ressource distante. Il suit la structure décrite en section 9.

### 6.3. Script vidéo

Le script décrit la vidéo image par image : minutage, action à l’écran, narration, notes de montage. Il suit la structure décrite en section 10.

## 7. Conventions de code

### 7.1. Ordre du fichier

1. `import pyxel` ;
2. constantes en majuscules, regroupées par thème ;
3. classes, de la plus élémentaire à la plus générale : `Level`, `Player`, `Game` ;
4. une seule ligne finale : `Game()`.

### 7.2. Forme

- deux lignes vides entre les blocs de premier niveau ;
- quatre espaces d’indentation ;
- méthodes dans l’ordre `__init__()`, `update()`, `draw()`, puis les méthodes auxiliaires ;
- appels longs écrits un argument par ligne, avec virgule finale ;
- noms de classes et d’attributs en anglais (`Player`, `Level`, `self.dx`), textes affichés et prose en français ;
- pas d’annotation de type, pas de décorateur, pas de classe de données, pas de compréhension imbriquée, pas de générateur ;
- pas de variable globale mutable : tout état vit dans un objet ;
- commentaires rares et utiles uniquement.

### 7.3. Forme de référence

```python
import pyxel


SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.x += 1

    def draw(self):
        pyxel.rect(
            self.x,
            self.y,
            8,
            8,
            pyxel.COLOR_YELLOW,
        )


class Game:
    def __init__(self):
        pyxel.init(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            title="Mon platformer",
        )

        self.player = Player(40, 216)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()

    def draw(self):
        pyxel.cls(pyxel.COLOR_DARK_BLUE)
        self.player.draw()


Game()
```

### 7.4. Valeurs de référence

| Élément | Valeur | Origine |
| --- | --- | --- |
| Dimensions de la fenêtre | 256 × 256 | Règlement Nuit du Code |
| Taille d’une tuile | 8 × 8 | Banque d’images |
| Dimensions du niveau | 32 × 32 tuiles | Remplit l’écran |
| Haut du sol, ligne de tuiles | 28 | Niveau de référence |
| Coordonnée `GROUND_Y` | 224 | `28 × 8` |
| Position verticale du joueur | 216 | `224 - 8` |
| Position horizontale du joueur, leçons 3 à 5 | 40 | Colonne 5 |
| Position horizontale du joueur, à partir de la leçon 6 | 8 | Place devant le joueur |
| Vitesse horizontale du joueur | 2 pixels par image | Contrôles au clavier |
| Gravité | 1 pixel par image² | Accélération verticale |
| Vitesse de saut | −11 pixels par image | Valeur négative, vers le haut |
| Hauteur du saut | environ 55 pixels | Mesurée au sommet de la trajectoire |
| Tuiles solides | (0, 1), (1, 1), (2, 1) | Sol, remplissage, plateforme |
| Case vide de la tilemap | (5, 5) | Zone transparente de la banque |
| Tuile de la pièce | (3, 1) | Banque d’images |
| Tuile de l’ennemi | (4, 0) | Banque d’images |
| Pièces du niveau | 9, aux positions des tuiles de la tilemap | Lues par `Level.take_coins()` |
| Ennemis | 2 : (88, 216) et (104, 144) | Écrits dans `Game.__init__()` |
| Vitesse de l’ennemi | 1 pixel par image | Allée et retour entre deux bornes |
| Points par pièce | 1 | `Game.score` |
| Canal du saut | 0 | Son 0 |
| Canal de la pièce | 1 | Son 1 |
| Canal de la collision | 2 | Son 2 |
| Défaite | `is_game_over` à vrai | `update()` sort immédiatement |
| Signature des collisions | `collide(x, y, w, h, dx, dy, walls)` | Renvoie le déplacement corrigé |
| Position du joueur sur la première plateforme | 176 | Dessus de la ligne 23 |
| Arrêt du saut sous la première plateforme | 192 | Dessous de la ligne 23 |

Toute nouvelle valeur de ce type doit être ajoutée à ce tableau.

### 7.5. Collisions

- Le joueur est décrit par un rectangle : `x`, `y`, `width`, `height`.
- Aucun objet ne modifie sa position avant d’avoir obtenu l’autorisation du niveau.
- La classe `Level` expose une méthode `move_player(x, y, dx, dy)` qui appelle `self.tilemap.collide()` et renvoie un couple `(dx, dy)` corrigé, jamais une position.
- Les dimensions transmises viennent des constantes `PLAYER_WIDTH` et `PLAYER_HEIGHT`.
- `SOLID_TILES` est une liste de tuiles de la banque d’images, pas de cases du niveau.
- L’état « au sol » se déduit du résultat : un déplacement vertical annulé alors que l’objet tombait.
- `is_solid()` n’est pas conservée après la leçon 6 : `collide()` couvre le besoin.

### 7.6. Objets du jeu

- Un type d’élément du jeu = une classe, avec `update()` et `draw()`.
- Une méthode `update()` peut rester vide (`pass`) : elle fait partie de l’interface commune.
- Les instances d’un même type sont rangées dans une liste, construite une seule fois dans `Game.__init__()`.
- Les listes sont parcourues par des boucles séparées dans `update()` et dans `draw()` ; jamais d’appel nommé objet par objet.
- Ordre du dessin : fond, niveau, pièces, ennemis, joueur, textes.
- Une tuile appartient au décor et ne peut pas disparaître ; un objet est une instance et peut être retiré.
- Les pièces du niveau restent des tuiles dans `res.pyxres` ; `Level.take_coins()` les efface en mémoire avec `pset()` et renvoie leurs positions en pixels.
- Les positions écrites à la main dans une liste servent aux objets absents de la tilemap, comme les ennemis.

### 7.7. Règles du jeu

- Le contact entre deux objets se teste avec `Game.collide(a, b)`, qui lit `x`, `y`, `width` et `height` ; ce n’est pas une classe.
- Les quatre inégalités sont strictes : des bords jointifs ne sont pas un contact.
- Ne pas confondre cette méthode avec `Tilemap.collide()`, qui corrige un déplacement contre le décor.
- Un objet qui disparaît porte `is_alive` : il est marqué pendant le parcours, puis la liste est reconstruite après la boucle.
- Ne jamais retirer un élément d’une liste pendant qu’on la parcourt.
- La reconstruction de liste s’écrit en compréhension, avec la boucle équivalente expliquée dans l’article.
- L’état du jeu vit dans des attributs de `Game` (`score`, `is_game_over`) ; `update()` sort immédiatement quand la partie est terminée.

## 8. Conventions des ressources

### 8.1. Génération

Le fichier `res.pyxres` n’est jamais modifié à la main ni produit par un outil externe pendant la production : il est généré par `cours/pyxel-platformer/outils/generer_ressources.py`.

```bash
python cours/pyxel-platformer/outils/generer_ressources.py
```

Le script :

- construit les images à partir de dessins ASCII de 8 × 8 caractères ;
- écrit un TOML dans une archive ZIP, conformément à `docs/pyxres-format.md` ;
- relit l’archive et vérifie les pixels, les tuiles, les sons et la musique ;
- recopie le fichier dans le dossier de la leçon 2.

Pour une nouvelle leçon, recopier `outils/res.pyxres` dans le dossier de la leçon. Ne jamais produire deux versions différentes du même fichier.

### 8.2. Banque d’images 0

| Position | Contenu |
| --- | --- |
| (0, 0) | Joueur au repos, image 0 |
| (1, 0) | Joueur au repos, image 1 |
| (2, 0) | Joueur en marche, image 0 |
| (3, 0) | Joueur en marche, image 1 |
| (4, 0) | Ennemi |
| (0, 1) | Sol, tuile du dessus |
| (1, 1) | Sol, remplissage |
| (2, 1) | Plateforme |
| (3, 1) | Pièce |
| (4, 1) | Buisson |

Les nouvelles tuiles s’ajoutent à la suite, sans déplacer les positions existantes : le code et les tilemaps déjà produits en dépendent.

La couleur 0 est la couleur transparente des sprites. Aucun dessin de sprite ne doit l’utiliser ; les contours emploient le bleu nuit.

### 8.3. Tilemap 0

- niveau de 32 × 32 tuiles ;
- sol à partir de la ligne 28 ;
- plateau technique : une case vide référence la tuile (5, 5), zone transparente de la banque ;
- les cases situées hors du niveau utilisent également la tuile (5, 5) ;
- neuf tuiles de pièce sur les lignes 22, 18 et 14 ; la leçon 7 les remplace en mémoire par des objets.

### 8.4. Sons et musiques

| Numéro | Contenu |
| --- | --- |
| Son 0 | Saut |
| Son 1 | Pièce, utilisée aussi pour le rebond en leçon 2 |
| Son 2 | Collision |
| Sons 8 à 11 | Mélodie de la musique 0, canal 0 |
| Sons 12 et 13 | Accompagnement de la musique 0, canal 1 |
| Musique 0 | Thème du niveau |

Les numéros déjà attribués ne changent pas. Les ajouts prennent les numéros suivants.

Chaque bruitage occupe un canal distinct : 0 pour le saut, 1 pour la pièce, 2 pour la collision.

## 9. Conventions de l’article HTML

### 9.1. Structure de page

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>…</title>
  <meta name="description" content="…">
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

Règles :

- un seul `h1`, placé dans `header.lesson-header` ;
- sections en `h2`, sous-sections en `h3`, sous-sous-sections en `h4` ;
- identifiants de section en minuscules sans accent, par exemple `la-taille-de-la-fenetre-a-la-nuit-du-code` ;
- sommaire `nav.lesson-toc` reprenant les `h2` ;
- blocs de code dans `<pre><code class="language-python">`, contenu échappé ;
- tableaux dans `<div class="table-wrapper">` puis `<table>`, avec `<thead>` ;
- aucune ressource distante : pas de CDN, pas de police, pas de script, pas d’image externe ;
- aucun style en ligne : toute la mise en forme est dans `styles/article.css`.

### 9.2. Encadrés

```html
<aside class="callout callout-note">
  <p class="callout-title">Titre de l’encadré</p>
  <p>Texte de l’encadré.</p>
</aside>
```

| Classe | Usage |
| --- | --- |
| `callout-note` | information complémentaire, rappel |
| `callout-tip` | conseil, méthode de travail |
| `callout-warning` | erreur fréquente, piège |
| `callout-important` | règle à ne pas modifier |

Une nouvelle variante suppose l’ajout de la classe et de son style dans `styles/article.css`, pas d’un style ponctuel dans la page.

### 9.3. Contenu attendu

1. Présentation de la leçon et de son résultat.
2. Objectifs, sous forme de liste numérotée.
3. Notions nouvelles.
4. Code complet de `main.py`.
5. Explication du programme, section par section.
6. Étapes de vérification du résultat.
7. Erreurs fréquentes, en encadrés `callout-warning`.
8. Expérimentations facultatives.
9. Synthèse « À retenir ».
10. Transition vers la leçon suivante.

Le code affiché dans l’article doit être identique, à l’octet près, à celui de `main.py`.

## 10. Conventions du script vidéo

Le script est en Markdown et comporte les parties suivantes, dans cet ordre :

1. fiche de production (public, environnement, version, durée cible, fichiers, ressource) ;
2. intention pédagogique ;
3. objectifs annoncés aux élèves ;
4. préparation de l’enregistrement ;
5. code final complet ;
6. découpage minuté ;
7. consignes de montage ;
8. vérification avant publication.

Chaque étape du découpage s’écrit ainsi :

```markdown
### 04:20 — Titre de l’étape

**À l’écran :** ce qui est visible.

**Narration :**

> Texte à dire, une idée par paragraphe.

**Action :** manipulation à effectuer.
```

Règles :

- minutage cumulatif, cohérent avec la durée annoncée ;
- narration au présent, phrases courtes ;
- le script ne lit pas l’article : il montre les décisions et le comportement du jeu ;
- les erreurs volontairement montrées sont signalées comme telles ;
- les inconnues d’interface sont présentées comme telles, avec une solution de repli, plutôt que décrites avec une fausse précision.

## 11. Ton et langue

- Ton neutre et informatif, sans emphase.
- Vouvoiement dans les articles, narration à la première personne du pluriel dans les vidéos.
- Pas de point d’exclamation, pas d’emoji, pas de superlatif publicitaire.
- Termes techniques introduits avant emploi, puis réutilisés à l’identique.
- Une notion par paragraphe, paragraphes courts.
- Typographie française : guillemets « », espaces insécables avant les deux-points, le point-virgule, le point d’interrogation et le point d’exclamation.
- Apostrophe typographique « ’ » dans les articles et les scripts ; apostrophe droite dans le code Python.

## 12. Procédure de production d’une leçon

1. Relire la section de la leçon dans `docs/plan-formation-pyxel.md`.
2. Vérifier les signatures utilisées dans `docs/api-reference.md`.
3. Partir du `main.py` de la leçon précédente et n’ajouter que les changements annoncés.
4. Mettre à jour `res.pyxres` par le script de génération si la leçon ajoute des ressources, puis recopier le fichier dans le dossier.
5. Écrire `main.py`, puis vérifier qu’il se compile et respecte les conventions de la section 7.
6. Écrire `article.html` en réutilisant `styles/article.css`.
7. Écrire `script-video.md`.
8. Exécuter les vérifications de la section 13.
9. Mettre à jour le tableau d’état de ce fichier.

## 13. Vérifications avant de considérer une leçon terminée

```bash
# 1. Syntaxe du code
python -m py_compile cours/pyxel-platformer/NN-lecon/main.py

# 2. Ressources reproductibles
python cours/pyxel-platformer/outils/generer_ressources.py
cmp cours/pyxel-platformer/outils/res.pyxres cours/pyxel-platformer/NN-lecon/res.pyxres
```

Vérifier également, par lecture ou par script :

- le code de l’article est identique à `main.py` ;
- les balises HTML sont équilibrées et aucun Markdown résiduel ne subsiste (`#`, `|`, `:::`, `**`) ;
- les liens de la feuille de style et des ancres sont valides ;
- le script vidéo décrit le même code que l’article ;
- la fenêtre mesure 256 × 256 et le niveau 32 × 32 tuiles ;
- aucun fichier généré inutile n’est ajouté au dépôt.

Si Pyxel ne peut pas être exécuté dans l’environnement de production, l’indiquer explicitement et limiter la validation à ce qui est vérifiable.

## 14. Ce qu’il ne faut pas faire

- Ajouter un second fichier Python ou un module personnel.
- Charger une image, un son ou une police depuis un fichier externe.
- Utiliser Quarto, un générateur de site ou une dépendance de rendu.
- Introduire du JavaScript ou un style en ligne dans les articles.
- Revenir à une fenêtre 128 × 128, sauf mention explicite comme variante.
- Modifier `res.pyxres` à la main ou déplacer les tuiles existantes.
- Introduire des décorateurs, des annotations de type ou des constructions Python avancées.
- Ajouter une évaluation, une note ou un barème.
- Reprendre l’architecture des exemples officiels de Pyxel : certains n’attribuent pas de méthode `draw()` à chaque élément.
- Produire une leçon sans son code exécutable et vérifié.

## 15. Quand une règle change

Une décision de forme prise en cours de production doit être appliquée partout :

1. mettre à jour `docs/plan-formation-pyxel.md` ;
2. mettre à jour ce fichier ;
3. mettre à jour les leçons déjà produites, y compris leur code et leurs captures de texte ;
4. relancer les vérifications de la section 13 sur toutes les leçons concernées ;
5. signaler les changements dans la description de la modification.

Une règle qui ne vit que dans une conversation n’existe pas : elle doit figurer ici ou dans le plan.
