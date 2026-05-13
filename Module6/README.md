# 📜 The Codex — Maîtriser les Mystères des Imports Python

> *Dans les temps anciens, les alchimistes cherchaient à transformer les métaux en or. Aujourd'hui, en tant qu'alchimiste Python, tu vas apprendre à transformer du code éparpillé en formules magiques organisées et réutilisables.*

---

## 📋 Table des Matières

- [Présentation](#présentation)
- [Concepts Abordés](#concepts-abordés)
- [Structure du Projet](#structure-du-projet)
- [Les Quatre Mystères Sacrés](#les-quatre-mystères-sacrés)
  - [Partie 1 — L'Alambic](#partie-1--lalambic)
  - [Partie 2 — La Distillation](#partie-2--la-distillation)
  - [Partie 3 — La Grande Transmutation](#partie-3--la-grande-transmutation)
  - [Partie 4 — Éviter l'Explosion](#partie-4--éviter-lexplosion)
- [Prérequis](#prérequis)
- [Utilisation](#utilisation)

---

## Présentation

**The Codex** est un projet Python centré sur la maîtrise des mécanismes d'import. À travers une série d'expériences alchimiques, on explore les quatre mystères sacrés des imports Python : l'initialisation des packages, les chemins d'import, les imports absolus vs relatifs, et la gestion des dépendances circulaires.

---

## Concepts Abordés

| Concept | Description |
|---|---|
| **Modules** | Un fichier `.py` est un module — importable depuis n'importe où |
| **Packages** | Un dossier avec `__init__.py` devient un package importable |
| **`import ...`** | Importe le module entier, accès via préfixe |
| **`from ... import ...`** | Importe directement une fonction ou variable |
| **Import absolu** | Chemin complet depuis la racine du projet |
| **Import relatif** | Chemin depuis le fichier actuel avec `.` ou `..` |
| **`__init__.py`** | Contrôle ce qui est exposé depuis le package |
| **Dépendances circulaires** | Deux modules qui s'importent mutuellement → explosion |

---

## Structure du Projet

```
.
├── alchemy
│   ├── __init__.py
│   ├── elements.py
│   ├── grimoire
│   │   ├── __init__.py
│   │   ├── dark_spellbook.py
│   │   ├── dark_validator.py
│   │   ├── light_spellbook.py
│   │   └── light_validator.py
│   ├── potions.py
│   └── transmutation
│       ├── __init__.py
│       └── recipes.py
├── elements.py
├── ft_alembic_0.py
├── ft_alembic_1.py
├── ft_alembic_2.py
├── ft_alembic_3.py
├── ft_alembic_4.py
├── ft_alembic_5.py
├── ft_distillation_0.py
├── ft_distillation_1.py
├── ft_kaboom_0.py
├── ft_kaboom_1.py
├── ft_transmutation_0.py
├── ft_transmutation_1.py
└── ft_transmutation_2.py
```

---

## Les Quatre Mystères Sacrés

### Partie 1 — L'Alambic

**Mystère :** Accéder à des fichiers locaux et des modules via différentes syntaxes d'import.

#### Fichiers créés

- `elements.py` — contient `create_fire()` et `create_water()`
- `alchemy/elements.py` — contient `create_earth()` et `create_air()`
- `alchemy/__init__.py` — expose partiellement le package

#### Les deux syntaxes d'import

```python
# import ... — accès via préfixe
import elements
elements.create_fire()

# from ... import ... — accès direct
from elements import create_water
create_water()
```

#### Accéder à un sous-package

```python
# import ...
import alchemy.elements
alchemy.elements.create_earth()

# from ... import ...
from alchemy.elements import create_air
create_air()
```

#### Le rôle de `__init__.py`

`__init__.py` agit comme une **vitrine** — il décide ce qui est visible depuis l'extérieur :

```python
# alchemy/__init__.py
from .elements import create_air as create_air  # exposé ✅
# create_earth n'est pas exposé → AttributeError ❌
```

#### Scripts de test

| Script | Syntaxe | Fichier cible | Fonction |
|---|---|---|---|
| `ft_alembic_0.py` | `import ...` | `elements.py` | `create_fire()` |
| `ft_alembic_1.py` | `from ... import ...` | `elements.py` | `create_water()` |
| `ft_alembic_2.py` | `import ...` | `alchemy/elements.py` | `create_earth()` |
| `ft_alembic_3.py` | `from ... import ...` | `alchemy/elements.py` | `create_air()` |
| `ft_alembic_4.py` | `import alchemy` | package alchemy | `create_air()` exposé, `create_earth()` caché |
| `ft_alembic_5.py` | `from alchemy import ...` | package alchemy | `create_air()` |

---

### Partie 2 — La Distillation

**Mystère :** Maîtriser les imports imbriqués et appeler du code depuis des fichiers distants.

#### Fichier créé

`alchemy/potions.py` — contient `healing_potion()` et `strength_potion()` qui appellent les quatre éléments fondamentaux depuis leurs modules respectifs.

#### Alias de package

Dans `__init__.py`, on peut créer un alias pour exposer une fonction sous un autre nom :

```python
from .potions import healing_potion as heal  # heal est un alias de healing_potion
```

Résultat :
```python
import alchemy
alchemy.heal()  # appelle healing_potion() via l'alias
```

#### Scripts de test

| Script | Syntaxe | Accès |
|---|---|---|
| `ft_distillation_0.py` | `from alchemy.potions import ...` | Direct vers `potions.py` |
| `ft_distillation_1.py` | `import alchemy` | Via `__init__.py` avec alias `heal` |

---

### Partie 3 — La Grande Transmutation

**Mystère :** Comprendre le débat entre imports absolus et relatifs.

#### Fichier créé

`alchemy/transmutation/recipes.py` — contient `lead_to_gold()` avec au moins un import absolu et un import relatif.

#### Import absolu vs relatif

```python
# Import absolu — chemin complet depuis la racine
import elements
from alchemy.elements import create_air

# Import relatif — depuis le fichier actuel
from ..elements import create_air    # .. = remonter dans alchemy/
from ..potions import strength_potion
```

#### Quand utiliser lequel ?

- **Import absolu** — plus lisible, recommandé pour les projets larges
- **Import relatif** — plus court, utile à l'intérieur d'un package pour éviter de répéter le nom du package

#### Scripts de test

| Script | Syntaxe | Accès |
|---|---|---|
| `ft_transmutation_0.py` | `import alchemy.transmutation.recipes` | Direct vers `recipes.py` |
| `ft_transmutation_1.py` | `import alchemy.transmutation` | Via `transmutation/__init__.py` |
| `ft_transmutation_2.py` | `import alchemy` | Via `alchemy/__init__.py` |

---

### Partie 4 — Éviter l'Explosion

**Mystère :** Identifier et casser la malédiction des dépendances circulaires.

#### Qu'est-ce qu'une dépendance circulaire ?

```
dark_spellbook.py importe dark_validator.py
dark_validator.py importe dark_spellbook.py
→ boucle infinie → ImportError !
```

#### Magie lumineuse — pas de dépendance circulaire ✅

`light_spellbook.py` importe `light_validator.py` mais `light_validator.py` n'importe PAS `light_spellbook.py` — il reçoit les ingrédients autorisés directement via le contexte, pas via import.

#### Magie noire — dépendance circulaire volontaire ❌

`dark_spellbook.py` importe `dark_validator.py` ET `dark_validator.py` importe `dark_spellbook.py` → explosion garantie !

```
ImportError: cannot import name 'dark_spell_allowed_ingredients'
from partially initialized module 'alchemy.grimoire.dark_spellbook'
(most likely due to a circular import)
```

#### Scripts de test

| Script | Résultat |
|---|---|
| `ft_kaboom_0.py` | Sort enregistré sans erreur ✅ |
| `ft_kaboom_1.py` | `ImportError` — explosion circulaire ❌ |

---

## Prérequis

- Python 3.10+
- `flake8` — vérification du style
- `mypy` — vérification des types

```bash
pip install flake8 mypy black
```

---

## Utilisation

```bash
# Partie 1 — L'Alambic
python3 ft_alembic_0.py
python3 ft_alembic_1.py
python3 ft_alembic_2.py
python3 ft_alembic_3.py
python3 ft_alembic_4.py
python3 ft_alembic_5.py

# Partie 2 — La Distillation
python3 ft_distillation_0.py
python3 ft_distillation_1.py

# Partie 3 — La Grande Transmutation
python3 ft_transmutation_0.py
python3 ft_transmutation_1.py
python3 ft_transmutation_2.py

# Partie 4 — L'Explosion
python3 ft_kaboom_0.py
python3 ft_kaboom_1.py
```

```bash
# Vérifier le style
flake8 .

# Vérifier les types
mypy . --strict
```

---

*The Codex — Laboratoire alchimique Python.*