# Présentation de la formation — script vidéo

## Fiche de production

- **Formation :** Créer un mini-platformer 2D avec Pyxel, module bonus Pyxel Cube compris
- **Public :** élèves de Première et Terminale NSI, enseignants, toute personne qui découvre la formation
- **Environnement :** PyxelStudio dans Capytale
- **Version ciblée :** Pyxel 3.0.1
- **Durée cible :** 3 minutes 20
- **Fichiers du projet :** aucun ; la vidéo ne montre que des captures du jeu et des leçons
- **Ressource utilisée :** aucune, hormis les captures extraites des leçons
- **Titre à l’écran :** Présentation de la formation

## Intention pédagogique

Cette vidéo ne montre pas de code. Elle répond à trois questions qu’un élève ou un enseignant se pose avant de commencer : qu’est-ce qu’on fabrique, qu’est-ce qu’on apprend en chemin, et qu’est-ce qu’on sait faire à la fin.

Le parti pris est de montrer le jeu terminé dès les premières secondes. La formation se juge sur un résultat jouable, pas sur une liste de chapitres. Le reste de la vidéo rend ce résultat crédible : il est atteignable parce qu’il se construit brique par brique, et chaque brique correspond à une leçon.

La vidéo se termine par le premier geste du parcours, pour que le spectateur puisse commencer immédiatement.

## Objectifs annoncés

À la fin de la vidéo, le spectateur doit savoir :

1. ce que produit la formation : un petit jeu de plateforme 2D complet, jouable de la première à la dernière seconde ;
2. comment le parcours est organisé : onze leçons sur un même jeu, puis trois chapitres de module bonus en 3D ;
3. quelles notions Python et quelles notions de création de jeu sont abordées ;
4. à quoi correspond le format imposé par la Nuit du Code : deux fichiers, aucun autre ;
5. comment suivre la formation : environnement, rythme, ressources fournies.

## Préparation de l’enregistrement

### Captures à préparer

- **Leçon 11 :** écran titre, partie complète, victoire, défaite, retour au titre.
- **Leçons 3 à 10 :** un plan court de chaque étape du jeu, dans l’ordre de la progression.
- **Leçons 5 et 9 :** un plan du niveau complet, puis un plan du décor qui défile avec la caméra.
- **Leçon 10 :** un plan de l’écran titre, un plan d’une fin de partie.
- **Module bonus :** le cube en rotation, l’anneau de quatre cubes, une partie du petit jeu 3D.

### Vérifications avant d’enregistrer

- Le jeu de la leçon 11 fonctionne et se termine par une victoire nette.
- Les captures montrent toujours la fenêtre complète, 256 sur 256, sans bord d’éditeur.
- Chaque plan dure au moins quatre secondes, pour laisser le temps de lire le jeu.
- Le son des captures est coupé, la musique du jeu ne doit pas passer sous la voix.
- Les chiffres cités sont vérifiés : onze leçons, trois chapitres bonus, deux fichiers, dix-huit pièces, trois ennemis.

## Texte de la narration

Cette vidéo ne comporte pas de code final : elle ne montre aucun programme. La narration se lit d’affilée, du début à la fin, et suit un débit calme d’environ cent cinquante mots par minute.

### 00:00 — Le jeu terminé

> Voici le jeu que nous construisons dans cette formation : un petit jeu de plateforme en deux dimensions, écrit en Python avec la bibliothèque Pyxel.
>
> Un joueur qui marche et qui saute, un décor de soixante-quatre cases de large, dix-huit pièces à ramasser, trois ennemis qui font les cent pas.
>
> Quatre écrans : le titre, la partie, la défaite et la victoire. Une musique, trois bruitages.
>
> Et deux fichiers, pas un de plus : le programme, et la ressource qui contient les images, le décor et les sons.

### 00:35 — Pourquoi cette formation

> La formation s’adresse à des débutants en création de jeux, élèves de NSI ou adultes qui veulent essayer.
>
> Nous n’apprenons pas Pyxel pour Pyxel. Nous apprenons à organiser un programme qui bouge : une mise à jour à chaque image, un dessin séparé de la logique, des objets Python qui représentent le joueur, le décor et les règles.

### 00:58 — Un seul jeu, onze leçons

> Tout le parcours construit le même jeu. On ne repart jamais de zéro.
>
> Chaque leçon ajoute une brique au programme précédent : un joueur, puis la gravité, puis un niveau, puis des collisions, puis des objets, puis des règles, puis une caméra, puis du son.
>
> Onze leçons, près de trois heures de vidéo, et un jeu qui se joue à chaque étape.

### 01:23 — Ce que couvre le parcours

> Les premières leçons installent la boucle de jeu, le fichier de ressources et les déplacements. Viennent ensuite la gravité et le saut, le niveau dessiné en tuiles, puis les collisions avec ce décor.
>
> La suite ajoute les objets à ramasser, les règles de victoire et de défaite, une caméra qui suit le joueur, des animations, une musique et des bruitages.
>
> La dernière leçon ne change pas le jeu : elle le vérifie, le rend autonome et prépare sa personnalisation.

### 01:55 — Le module bonus

> Après le parcours 2D, un module bonus ouvre la troisième dimension avec Pyxel Cube, le moteur 3D livré avec Pyxel depuis la version 3.
>
> Trois chapitres : une scène avec caméra et cube, des objets composés, puis un petit jeu complet en trois dimensions. Ce module n’est pas nécessaire pour le concours : il montre que les mêmes principes tiennent dans un autre moteur.

### 02:21 — Ce que vous saurez faire

> À la fin, vous savez écrire un jeu qui se joue : un joueur qui répond au clavier, un décor qui défile, des collisions, des règles, un score, des écrans de fin et du son.
>
> Vous savez aussi livrer ce jeu dans le format imposé par la Nuit du Code : deux fichiers dans un dossier, qui fonctionnent ailleurs que sur votre machine.
>
> Et vous savez où intervenir pour personnaliser : changer le niveau, ajouter un ennemi, régler la difficulté.

### 02:53 — Comment suivre

> Tout se passe dans PyxelStudio, dans Capytale, avec Pyxel 3.0.1. Chaque leçon fournit un article, un script vidéo et le code complet : ce que vous lisez est ce qui s’exécute.
>
> Le rythme conseillé tient en trois temps : une leçon, le jeu relancé, puis une modification personnelle. C’est la modification qui fixe les idées.

### 03:15 — Début du parcours

> Onze leçons, un module bonus, un jeu qui se termine. Nous commençons par la boucle de jeu.

## Découpage et visuels

| Timecode | À l’écran | Action |
| --- | --- | --- |
| 00:00 | Le jeu final en mouvement : partie, saut, ramassage | jouer trente secondes, sans coupe |
| 00:35 | La fenêtre du jeu, puis un plan large de l’éditeur | arrêter le jeu sur l’écran titre |
| 00:58 | Succession de plans courts : leçons 3, 4, 5, 6 | enchaîner les étapes dans l’ordre |
| 01:23 | Le niveau complet, puis le décor qui défile | montrer la caméra en mouvement |
| 01:55 | Cube en rotation, anneau de quatre cubes, petit jeu 3D | trois plans de trois secondes |
| 02:21 | Dossier de deux fichiers, puis victoire du jeu | montrer le dossier, puis la fin de partie |
| 02:53 | PyxelStudio dans Capytale, un article ouvert | survoler l’article d’une leçon |
| 03:15 | Retour au jeu, sur l’écran titre | couper au premier mouvement |

## Consignes de montage

- Commencer sur le jeu en mouvement, pas sur un logo ni sur un titre.
- Garder les captures sans interface d’éditeur : la fenêtre du jeu seule.
- Couper le son des captures et poser la voix dessus.
- Afficher les chiffres clés en incrustation discrète : onze leçons, trois chapitres bonus, deux fichiers.
- Ne jamais montrer de code : cette vidéo parle du résultat et du parcours.
- Terminer sur l’écran titre du jeu, sans générique.

## Vérification avant publication

- La durée réelle ne dépasse pas trois minutes trente.
- Les chiffres cités correspondent aux leçons : onze leçons, trois chapitres bonus, deux fichiers, dix-huit pièces, trois ennemis.
- Aucune image de code n’apparaît.
- La narration ne contient ni point d’exclamation ni superlatif publicitaire.
- Les apostrophes sont typographiques et les guillemets français.
- Le son du jeu ne couvre jamais la voix.
- La dernière phrase annonce la première leçon du parcours.
