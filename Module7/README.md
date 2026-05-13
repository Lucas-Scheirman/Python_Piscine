# 🃏 DataDeck — Architecture de Cartes Abstraites

> *Gotta catch 'em all; but sometimes, the real treasure is the skills we made along the way.*

---

## 📋 Table des Matières

- [Présentation](#présentation)
- [Concepts Abordés](#concepts-abordés)
- [Structure du Projet](#structure-du-projet)
- [Exercices](#exercices)
  - [Exercice 0 — Creature Factory](#exercice-0--creature-factory)
  - [Exercice 1 — Capabilities](#exercice-1--capabilities)
  - [Exercice 2 — Abstract Strategy](#exercice-2--abstract-strategy)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Utilisation](#utilisation)

---

## Présentation

**DataDeck** est un projet Python centré sur les design patterns avancés à travers la construction d'un système de cartes de créatures inspiré des jeux de monstres. L'objectif est de concevoir un système flexible capable de gérer des milliers de types de cartes différents tout en maintenant un code propre et maintenable.

---

## Concepts Abordés

| Concept | Description |
|---|---|
| **Abstract Factory** | Créer des familles d'objets sans connaître leurs classes concrètes |
| **Héritage Multiple** | Une classe hérite de plusieurs parents simultanément |
| **Pattern Stratégie** | Encapsuler des comportements interchangeables dans des classes séparées |
| **Classes Abstraites (ABC)** | Définir des contrats que les sous-classes doivent respecter |
| **Polymorphisme** | Un même appel se comporte différemment selon l'objet |
| **`isinstance`** | Vérifier le type d'un objet à l'exécution |

---

## Structure du Projet

```
Module7/
├── battle.py          # Script de test ex0
├── capacitor.py       # Script de test ex1
├── tournament.py      # Script de test ex2
├── ex0/
│   ├── __init__.py    # Expose seulement les fabriques
│   ├── creature.py    # Creature + 4 créatures concrètes
│   └── factory.py     # CreatureFactory + FlameFactory + AquaFactory
├── ex1/
│   ├── __init__.py    # Expose seulement les fabriques
│   ├── capabilities.py # HealCapability + TransformCapability
│   ├── creature.py    # Sproutling, Bloomelle, Shiftling, Morphagon
│   └── factory.py     # HealingCreatureFactory + TransformCreatureFactory
└── ex2/
    ├── __init__.py    # Expose les stratégies
    └── strategy.py    # BattleStrategy + 3 stratégies concrètes
```

---

## Exercices

### Exercice 0 — Creature Factory

**Fichiers :** `ex0/`, `battle.py`

Construction du système de base avec des créatures organisées en familles, créées par des fabriques abstraites.

#### Hiérarchie des Classes

```
Creature (ABC)
├── Flameling    → "Fire"        → "Flameling uses Ember!"
├── Pyrodon      → "Fire/Flying" → "Pyrodon uses Flamethrower!"
├── Aquabub      → "Water"       → "Aquabub uses Water Gun!"
└── Torragon     → "Water"       → "Torragon uses Hydro Pump!"

CreatureFactory (ABC)
├── FlameFactory → crée Flameling + Pyrodon
└── AquaFactory  → crée Aquabub + Torragon
```

#### Le Pattern Abstract Factory

```python
# Le code client ne sait pas quelle créature il crée
def test_factory(factory: CreatureFactory) -> None:
    base = factory.create_base()      # Flameling ou Aquabub
    evolved = factory.create_evolved() # Pyrodon ou Torragon
    print(base.describe())
    print(base.attack())
```

#### Règle importante

`__init__.py` n'expose que les fabriques — jamais les créatures concrètes :

```python
# ex0/__init__.py
from .factory import FlameFactory as FlameFactory
from .factory import AquaFactory as AquaFactory
# Flameling, Pyrodon, etc. ne sont pas exposés !
```

#### Exemple de Sortie

```
Testing factory
Flameling is a Fire type Creature
Flameling uses Ember!
Pyrodon is a Fire/Flying type Creature
Pyrodon uses Flamethrower!
Testing battle
Flameling is a Fire type Creature
vs.
Aquabub is a Water type Creature
fight!
Flameling uses Ember!
Aquabub uses Water Gun!
```

---

### Exercice 1 — Capabilities

**Fichiers :** `ex1/`, `capacitor.py`

Ajout de capacités spéciales aux créatures via l'**héritage multiple**.

#### Hiérarchie des Classes

```
HealCapability (ABC)
└── heal() -> str

TransformCapability (ABC)
├── _transformed: bool
├── transform() -> str
└── revert() -> str

Sproutling(Creature, HealCapability)   → "Grass"
Bloomelle(Creature, HealCapability)    → "Grass/Fairy"
Shiftling(Creature, TransformCapability) → "Normal"
Morphagon(Creature, TransformCapability) → "Normal/Dragon"
```

#### Héritage Multiple en Action

```python
class Sproutling(Creature, HealCapability):
    def attack(self) -> str:
        return "Sproutling uses Vine Whip!"

    def heal(self) -> str:
        return "Sproutling heals itself for a small amount"
```

#### État Persistant dans TransformCapability

`_transformed` change le comportement de `attack()` :

```python
def attack(self) -> str:
    if self._transformed:
        return "Shiftling performs a boosted strike!"
    return "Shiftling attacks normally."
```

#### Exemple de Sortie

```
Testing Creature with healing capability
base:
Sproutling is a Grass type Creature
Sproutling uses Vine Whip!
Sproutling heals itself for a small amount
Testing Creature with transform capability
base:
Shiftling is a Normal type Creature
Shiftling attacks normally.
Shiftling shifts into a sharper form!
Shiftling performs a boosted strike!
Shiftling returns to normal.
```

---

### Exercice 2 — Abstract Strategy

**Fichiers :** `ex2/`, `tournament.py`

Implémentation du **pattern stratégie** pour un système de tournoi flexible.

#### Hiérarchie des Stratégies

```
BattleStrategy (ABC)
├── is_valid(creature) -> bool
└── act(creature) -> None

NormalStrategy     → valide pour toute créature → attack()
DefensiveStrategy  → valide pour HealCapability → attack() + heal()
AggressiveStrategy → valide pour TransformCapability → transform() + attack() + revert()
```

#### Pourquoi le Pattern Stratégie ?

Sans stratégie, le tournoi doit connaître chaque type de créature :
```python
# ❌ mauvais — le tournoi dépend des types
if isinstance(creature, HealCapability):
    creature.attack()
    creature.heal()
```

Avec stratégie, le tournoi appelle juste `act()` :
```python
# ✅ bon — le tournoi ne sait pas ce qui se passe à l'intérieur
strategy.act(creature)
```

#### Gestion des Erreurs

Si une stratégie incompatible est utilisée, une exception est levée :
```
Battle error, aborting tournament: Invalid Creature 'Flameling' for this aggressive strategy
```

#### Logique du Tournoi

Chaque opponent combat **une fois contre chaque autre opponent** :
```python
for i in range(len(opponents)):
    for j in range(i + 1, len(opponents)):
        # combat entre opponents[i] et opponents[j]
```

#### Exemple de Sortie

```
Tournament 2 (multiple)
[ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]
*** Tournament ***
3 opponents involved
* Battle *
Aquabub is a Water type Creature
vs.
Sproutling is a Grass type Creature
now fight!
Aquabub uses Water Gun!
Sproutling uses Vine Whip!
Sproutling heals itself for a small amount
```

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│              tournament.py                       │
│  battle(opponents: list[tuple[Factory, Strat]]) │
│    → strategy.act(creature)                      │
└─────────────────────────────────────────────────┘
         │                    │
         ▼                    ▼
┌─────────────────┐  ┌─────────────────────┐
│   ex0 / ex1     │  │       ex2           │
│  CreatureFactory│  │   BattleStrategy    │
│  ├── FlameFactory│  │  ├── NormalStrategy │
│  ├── AquaFactory │  │  ├── Defensive     │
│  ├── HealFactory │  │  └── Aggressive    │
│  └── Transform  │  └─────────────────────┘
└─────────────────┘
```

---

## Prérequis

- Python 3.10+
- `flake8` — vérification du style
- `mypy` — vérification des types

```bash
pip install flake8 mypy
```

---

## Utilisation

```bash
# Exercice 0
python3 battle.py

# Exercice 1
python3 capacitor.py

# Exercice 2
python3 tournament.py
```

```bash
# Vérifier le style
flake8 .

# Vérifier les types
mypy . --strict
```

---

*DataDeck — Maîtriser les design patterns Python à travers le jeu.*