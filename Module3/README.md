# Data Quest — Maîtriser les Collections Python

---

## Présentation du module

Ce module a pour but de découvrir et maîtriser les principales structures de données
de Python dans un contexte de jeu vidéo. Chaque exercice introduit une nouvelle
structure de données et des concepts associés.

Le fil conducteur est la construction d'une plateforme d'analyse de données de jeu :
gestion des joueurs, des scores, des coordonnées, des achievements, de l'inventaire
et des événements en temps réel.

---

## Règles générales

- Python 3.10 ou plus
- Respecter le standard **flake8** (style de code, max 79 caractères par ligne)
- **Type hints** obligatoires sur toutes les fonctions, vérifiés avec `mypy`
- Pas de fichiers I/O, tout en mémoire ou via arguments en ligne de commande
- Chaque exercice n'autorise que certaines fonctions et modules

---

## Exercice 0 — Command Quest

**Fichier :** `ex0/ft_command_quest.py`

**But :** Découvrir comment un programme reçoit des arguments depuis la ligne de
commande via `sys.argv`.

**Ce qu'on gère :**
- Afficher le nom du programme (`sys.argv[0]`)
- Afficher chaque argument reçu avec son index
- Gérer le cas où aucun argument n'est fourni
- Afficher le nombre total d'arguments

**Concepts clés :** listes, `sys.argv`, slice, `len()`

---

## Exercice 1 — Score Cruncher

**Fichier :** `ex1/ft_score_analytics.py`

**But :** Traiter des scores de jeu passés en ligne de commande et calculer des
statistiques, tout en gérant les erreurs de saisie.

**Ce qu'on gère :**
- Ignorer les valeurs non numériques avec un message d'erreur (`try/except`)
- Stocker les scores valides dans une liste
- Calculer le total, la moyenne, le score max, le score min et l'écart
- Afficher un message d'usage si aucun score valide n'est fourni

**Concepts clés :** listes, `try/except`, `ValueError`, `sum()`, `max()`, `min()`

---

## Exercice 2 — Position Tracker

**Fichier :** `ex2/ft_coordinate_system.py`

**But :** Gérer des coordonnées 3D sous forme de tuples et calculer des distances
dans l'espace.

**Ce qu'on gère :**
- Demander des coordonnées à l'utilisateur au format `x,y,z`
- Relancer la saisie en boucle jusqu'à recevoir un input valide
- Gérer les erreurs de format (mauvais nombre de valeurs, valeurs non numériques)
- Calculer la distance au centre (0,0,0)
- Calculer la distance entre deux points avec la formule euclidienne 3D

**Formule :** `math.sqrt((x2-x1)² + (y2-y1)² + (z2-z1)²)`

**Concepts clés :** tuples, immutabilité, `while True`, `input()`, `math.sqrt()`, `round()`

---

## Exercice 3 — Achievement Hunter

**Fichier :** `ex3/ft_achievement_tracker.py`

**But :** Gérer des collections d'achievements uniques pour plusieurs joueurs et
effectuer des opérations ensemblistes.

**Ce qu'on gère :**
- Générer aléatoirement des achievements pour 4 joueurs
- Trouver tous les achievements distincts parmi tous les joueurs (union)
- Trouver les achievements communs à tous les joueurs (intersection)
- Trouver les achievements exclusifs à chaque joueur (différence)
- Trouver les achievements manquants pour chaque joueur (différence inverse)

**Opérations :**
- `|` union → tout ce que tout le monde a
- `&` intersection → ce que tout le monde a en commun
- `-` différence → ce qu'un joueur a et pas les autres

**Concepts clés :** sets, opérations ensemblistes, `random.sample()`, `random.randint()`

---

## Exercice 4 — Inventory Master

**Fichier :** `ex4/ft_inventory_system.py`

**But :** Construire un système d'inventaire à partir d'arguments en ligne de commande
et effectuer des analyses sur les données.

**Ce qu'on gère :**
- Parser les arguments au format `nom:quantité`
- Détecter et ignorer les paramètres invalides (mauvais format, doublons, quantité non entière)
- Stocker l'inventaire dans un dictionnaire
- Calculer la quantité totale et le pourcentage de chaque item
- Trouver l'item le plus et le moins abondant (premier en cas d'égalité)
- Ajouter un nouvel item avec `dict.update()`

**Concepts clés :** dictionnaires, `dict.keys()`, `dict.values()`, `dict.items()`, `dict.update()`, parsing

---

## Exercice 5 — Stream Wizard

**Fichier :** `ex5/ft_data_stream.py`

**But :** Découvrir les générateurs Python pour produire des données à la demande
sans surcharger la mémoire.

**Ce qu'on gère :**
- Créer un générateur infini `gen_event()` qui produit des tuples `(joueur, action)`
- Appeler ce générateur 1000 fois avec `next()`
- Créer une liste de 10 tuples depuis un nouveau générateur
- Créer un générateur fini `consume_event()` qui pioche et supprime des éléments
  de la liste jusqu'à ce qu'elle soit vide
- Utiliser `consume_event()` directement dans un `for`

**Concepts clés :** générateurs, `yield`, `next()`, `while True`, `while liste`, `pop()`, mémoire

---

## Exercice 6 — Data Alchemist

**Fichier :** `ex6/ft_data_alchemist.py`

**But :** Maîtriser les compréhensions Python pour transformer et filtrer des données
de façon concise et élégante.

**Ce qu'on gère :**
- List comprehension pour capitaliser tous les noms
- List comprehension avec filtre pour garder seulement les noms déjà capitalisés
- Dict comprehension pour associer un score aléatoire à chaque joueur
- Dict comprehension avec filtre pour garder seulement les scores au-dessus de la moyenne

**Concepts clés :** list comprehension, dict comprehension, set comprehension, `sum()`, `round()`

---

## Résumé des structures de données

| Structure | Ordonné | Doublons | Mutable | Accès |
|-----------|---------|----------|---------|-------|
| list      | ✅ oui  | ✅ oui   | ✅ oui  | index |
| tuple     | ✅ oui  | ✅ oui   | ❌ non  | index |
| set       | ❌ non  | ❌ non   | ✅ oui  | aucun |
| dict      | ✅ oui  | ❌ clés  | ✅ oui  | clé   |