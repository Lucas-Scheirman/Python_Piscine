# Théorie — Défense Orale Data Quest

---

## Règles générales

- Python 3.10 ou plus
- Respecter **flake8** (style de code, max 79 caractères par ligne)
- **Type hints** sur toutes les fonctions, vérifiés avec `mypy`
- Pas de fichiers I/O, tout en mémoire ou via arguments

---

## Ex0 — sys.argv (listes)

### C'est quoi sys.argv ?
Liste des arguments passés en ligne de commande.
`sys.argv[0]` est toujours le nom du programme, les vrais arguments commencent à `sys.argv[1]`.
```python
# python3 script.py hello world
sys.argv[0]  # → 'script.py'
sys.argv[1]  # → 'hello'
sys.argv[2]  # → 'world'
```

### C'est quoi un slice ?
Coupe une liste en donnant un index de début et/ou de fin :
```python
liste = [0, 1, 2, 3, 4]
liste[1:]   # → [1, 2, 3, 4]  (enlève le premier)
liste[:3]   # → [0, 1, 2]     (garde les 3 premiers)
liste[-1]   # → 4             (dernier élément)
liste[1:3]  # → [1, 2]        (du 2ème au 3ème)
```

### C'est quoi enumerate ?
Donne l'index ET la valeur en même temps dans une boucle :
```python
liste = ["alice", "bob", "charlie"]

for i, name in enumerate(liste, 1):  # commence à 1
    print(i, name)
# → 1 alice
# → 2 bob
# → 3 charlie
```
Le deuxième paramètre `, 1` change le départ du compteur.

### C'est quoi pop() ?
Supprime ET retourne un élément d'une liste :
```python
liste = ["a", "b", "c"]
liste.pop(0)   # supprime et retourne "a" → liste = ["b", "c"]
liste.pop()    # sans index → supprime le dernier
```
Différence avec `del` : `del` supprime seulement, sans retourner la valeur.

### 5 façons d'ignorer sys.argv[0]
L'évaluateur peut demander des alternatives, en connaître 2 ou 3 suffit.

**1. range(1, n) — style C** *(solution utilisée)*
```python
for i in range(1, n):
    print(sys.argv[i])
```
On commence la boucle à l'index 1, ce qui saute naturellement sys.argv[0].

**2. Slice sys.argv[1:] — le plus pythonique**
```python
args = sys.argv[1:]  # nouvelle liste sans le premier élément
for i, arg in enumerate(args, 1):
    print(arg)
```

**3. enumerate direct sur le slice — compact**
```python
# sys.argv[1:] → ignore argv[0]
# , 1          → compteur commence à 1
for i, arg in enumerate(sys.argv[1:], 1):
    print(arg)
```

**4. pop(0)**
```python
args = sys.argv.copy()  # copie pour ne pas modifier sys.argv
args.pop(0)             # supprime le premier élément
```

**5. del args[0]**
```python
args = sys.argv.copy()
del args[0]  # supprime sans retourner la valeur
```

---

## Ex1 — try/except (listes)

### C'est quoi try/except ?
Permet de gérer les erreurs sans crasher le programme.
Le code dans `try` s'exécute, si une erreur se produit on va dans `except`.
```python
try:
    value = int("abc")    # plante ici → va dans except
    print("jamais affiché")
except ValueError as e:
    print(f"Erreur: {e}") # on arrive ici
```

### ValueError
Levée quand une conversion de type échoue :
```python
int("abc")    # → ValueError
float("xyz")  # → ValueError
int("3.14")   # → ValueError (int ne gère pas les décimaux)
```

### Comportement si invalide
`value` n'est jamais assigné, le code après le `try` ne s'exécute pas,
on affiche l'erreur et on continue avec l'argument suivant. ✅

---

## Ex2 — tuples

### C'est quoi un tuple ?
Comme une liste mais **immutable** : une fois créé, on ne peut plus le modifier.
C'est utile pour protéger des données contre les modifications accidentelles.
```python
mon_tuple = (1.0, 2.5, 3.0)
mon_tuple[0]    # → 1.0  (lecture OK)
mon_tuple[0] = 99  # → TypeError ! immutable
```

### Différence liste vs tuple
```python
# Liste → modifiable
liste = [1, 2, 3]
liste[0] = 99   # ✅ OK

# Tuple → immutable
tup = (1, 2, 3)
tup[0] = 99     # ❌ TypeError
```

### Différence tuple vs parenthèses
Les `()` servent aussi pour les fonctions, ce qui est différent des tuples :
```python
(1, 2, 3)   # → tuple
set()       # → appel de fonction, crée un set vide
int()       # → appel de fonction, crée un int
```

### Formule distance euclidienne 3D
C'est le théorème de Pythagore étendu en 3 dimensions.
En 2D : `c² = a² + b²`
En 3D on ajoute une dimension :

Distance entre deux points (x1,y1,z1) et (x2,y2,z2) :
```python
math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
```
En clair : racine carrée de la somme des différences au carré.

Distance au centre (0,0,0) → simplifié car x1=y1=z1=0 :
```python
math.sqrt(x**2 + y**2 + z**2)
```

### while True + input()
Boucle infinie jusqu'à recevoir un input valide :
```python
while True:
    raw = input("Entrez x,y,z: ")
    # si valide → return (sort de la fonction ET de la boucle)
    # si invalide → continue (reboucle automatiquement)
```

### Ctrl+D / Ctrl+Z
- Linux/Mac → `Ctrl+D` envoie EOF (End Of File = fin de l'entrée)
- Windows → `Ctrl+Z`
- Fait crasher `input()` avec `EOFError` car il attendait une saisie
  mais le flux est fermé → non géré dans notre code

---

## Ex3 — sets

### C'est quoi un set ?
Collection **sans doublons** et **non ordonnée**.
Chaque élément est unique, les doublons sont automatiquement ignorés.
```python
ma_liste = [1, 2, 2, 3, 3, 3]  # garde les doublons
mon_set  = {1, 2, 2, 3, 3, 3}  # ignore les doublons

print(ma_liste)  # → [1, 2, 2, 3, 3, 3]
print(mon_set)   # → {1, 2, 3}
```

### Notation set vs dict vs tuple
```python
{1, 2, 3}       # set  → éléments seuls
{"a": 1, "b": 2} # dict → paires clé:valeur
(1, 2, 3)       # tuple → parenthèses
```

### Opérations sur les sets
```python
alice   = {"Boss Slayer", "Untouchable", "Survivor"}
bob     = {"Untouchable", "Speed Runner"}
charlie = {"Untouchable", "Treasure Hunter"}

# | union → TOUT ce que tout le monde a (sans doublons)
alice | bob  # → {"Boss Slayer", "Untouchable", "Survivor", "Speed Runner"}

# & intersection → seulement ce que TOUT LE MONDE a en commun
alice & bob & charlie  # → {"Untouchable"}

# - différence → ce qu'alice a mais que personne d'autre n'a
alice - bob - charlie  # → {"Boss Slayer", "Survivor"}

# all - alice → ce qu'alice n'a pas mais qui existe
all_achievements - alice  # → achievements manquants
```

### Pourquoi print(set()) affiche set() et pas {} ?
`{}` est déjà réservé pour les **dictionnaires vides** en Python.
Si Python affichait `{}` pour un set vide, on ne saurait pas si c'est un set ou un dict.
```python
{}       # → dict vide
set()    # → set vide (notation claire pour éviter la confusion)
```

### random.sample
Pioche n éléments **sans répétition** dans une liste :
```python
random.sample(["a", "b", "c", "d"], 2)  # → ["c", "a"]
# jamais le même élément deux fois dans le résultat
```

---

## Ex4 — dictionnaires

### C'est quoi un dict ?
Collection de paires **clé:valeur**. L'accès par clé est instantané.
```python
inventory = {"sword": 1, "potion": 5}
inventory["sword"]     # → 1
inventory.keys()       # → toutes les clés
inventory.values()     # → toutes les valeurs
inventory.items()      # → paires (clé, valeur)
```

### dict.update()
Ajoute ou met à jour des clés dans le dictionnaire :
```python
inventory.update({"magic_item": 1})
# → ajoute magic_item:1 à inventory
```

### Gestion des erreurs de parsing
```python
parts = arg.split(":")
if len(parts) != 2:     # pas exactement un ':' → paramètre invalide
if name in inventory:   # clé déjà présente → doublon
int(quantity)           # ValueError si quantity n'est pas un entier
```

### Inventaire vide
Si inventaire vide :
- `sum({}.values())` → 0, pas de crash
- La boucle `for` ne s'exécute jamais → pas de division par 0 ✅

### Pourquoi dict plutôt que liste ?
L'accès par clé est instantané dans un dict.
Dans une liste il faut parcourir tous les éléments pour trouver un item.

---

## Ex5 — générateurs

### C'est quoi un générateur ?
Fonction avec `yield` qui produit des valeurs **une par une** à la demande,
au lieu de tout retourner d'un coup en mémoire.
```python
# Fonction normale → crée TOUT en mémoire
def normale():
    return [1, 2, 3, 4, 5]  # liste entière en mémoire

# Générateur → produit UNE valeur à la fois
def generateur():
    yield 1  # produit 1, se met en pause
    yield 2  # reprend, produit 2, se met en pause
    yield 3  # reprend, produit 3, termine
```

### yield
`yield` fait deux choses :
1. Retourne la valeur au code qui a appelé `next()`
2. Met la fonction **en pause** exactement là où il est

Au prochain `next()`, la fonction reprend exactement après le `yield`.

### next()
Appelle le générateur une seule fois et récupère la valeur du prochain `yield` :
```python
gen = gen_event()
next(gen)  # → ('alice', 'run')   démarre, pause au yield
next(gen)  # → ('bob', 'sleep')   reprend, pause au yield
next(gen)  # → ('dylan', 'grab')  reprend, pause au yield
```
Sans `next()` le générateur ne produit rien, il attend qu'on lui demande.

### while True vs while liste
```python
# Générateur INFINI → while True, ne s'arrête jamais tout seul
# Contrôlé de l'extérieur avec next() ou range()
def gen_event():
    while True:
        yield (random.choice(players), random.choice(actions))

# Générateur FINI → while liste, s'arrête quand la liste est vide
# while liste = True si liste non vide, False si vide
def consume_event(liste):
    while liste:
        yield liste.pop(random.randint(0, len(liste) - 1))
```

### pop(index)
Supprime ET retourne l'élément à l'index donné :
```python
liste = ["a", "b", "c"]
liste.pop(1)  # → "b", liste = ["a", "c"]
```

### Pourquoi les générateurs économisent la mémoire ?
```python
# Liste → 1 million de tuples créés EN MÊME TEMPS en mémoire ❌
events = [(random.choice(p), random.choice(a)) for _ in range(1000000)]

# Générateur → UN seul tuple créé à la fois ✅
def gen_event():
    while True:
        yield (random.choice(players), random.choice(actions))
```

### Generator[X, Y, Z] — type hint
```python
Generator[tuple[str, str], None, None]
#         ↑ YieldType      ↑ SendType  ↑ ReturnType
```
- **YieldType** → type de ce que yield produit
- **SendType** → type de ce qu'on envoie avec `.send()` (None = non utilisé)
- **ReturnType** → type du return final (None = pas de return)

### .send() — fonctionnalité avancée
Envoie une valeur dans le générateur pendant qu'il tourne.
Non utilisé dans ce projet mais bon à connaître.

---

## Ex6 — compréhensions

### C'est quoi une compréhension ?
Façon courte et pythonique d'écrire une boucle en une ligne.

### List comprehension
```python
# Boucle normale
result = []
for x in liste:
    if condition:
        result.append(expression)

# Compréhension → même chose en 1 ligne
result = [expression for x in liste if condition]
```

### Dict comprehension
```python
# Clé: valeur pour chaque élément
scores = {name: random.randint(0, 1000) for name in players}

# Avec filtre
high = {name: score for name, score in scores.items() if score > average}
```

### Set comprehension
```python
# Comme list comprehension mais avec {} → résultat sans doublons
unique = {name.lower() for name in players}
```

### Syntaxe générale
```python
[expression for element in iterable if condition]       # liste
{clé: valeur for element in iterable if condition}      # dict
{expression for element in iterable if condition}       # set
```

### Règle flake8 — max 79 caractères
Si la compréhension est trop longue, utiliser des parenthèses/accolades :
```python
# Trop long sur une ligne → on coupe avec des accolades
high_scores = {
    name: score
    for name, score in scores.items()
    if score > average
}
# C'est toujours une seule compréhension ✅
```

---

## Questions pièges possibles

**Pourquoi utiliser un set plutôt qu'une liste ?**
→ Le set supprime automatiquement les doublons et les opérations
union/intersection/différence sont très rapides.

**Pourquoi utiliser un tuple plutôt qu'une liste ?**
→ Le tuple est immutable, il protège les données contre les modifications
accidentelles. Idéal pour des coordonnées qui ne doivent pas changer.

**Pourquoi utiliser un générateur plutôt qu'une liste ?**
→ Le générateur économise la mémoire car il produit les valeurs une par une
au lieu de tout stocker en même temps.

**Pourquoi utiliser un dict plutôt qu'une liste ?**
→ L'accès par clé est instantané dans un dict. Dans une liste il faut
parcourir tous les éléments pour trouver ce qu'on cherche.

**Quelle est la différence entre yield et return ?**
→ `return` termine la fonction et retourne une valeur.
`yield` met la fonction en pause et retourne une valeur, mais la fonction
peut reprendre au prochain `next()`.

**Quelle est la différence entre pop() et del ?**
→ `pop()` supprime ET retourne l'élément.
`del` supprime seulement, sans retourner la valeur.