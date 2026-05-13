# 🌐 Code Nexus — Flux de Données Polymorphiques dans la Matrice Digitale

> *Néo-Tokyo, 2087. Les données circulent à travers des réseaux de fibres quantiques comme des rivières de néon. Bienvenue au Code Nexus.*

---

## 📋 Table des Matières

- [Présentation](#présentation)
- [Concepts Abordés](#concepts-abordés)
- [Structure du Projet](#structure-du-projet)
- [Exercices](#exercices)
  - [Exercice 0 — Processeur de Données](#exercice-0--processeur-de-données)
  - [Exercice 1 — Flux de Données Polymorphique](#exercice-1--flux-de-données-polymorphique)
  - [Exercice 2 — Pipeline de Données](#exercice-2--pipeline-de-données)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Utilisation](#utilisation)

---

## Présentation

**Code Nexus** est un projet Python centré sur la maîtrise de la programmation orientée objet à travers un système de traitement de données cyberpunk.

L'objectif est de construire un **pipeline de données polymorphique** capable de recevoir des flux de données mixtes, de router chaque élément vers le bon processeur, et d'exporter les résultats dans plusieurs formats — le tout sans que le pipeline ne connaisse le type exact des données qu'il traite.

---

## Concepts Abordés

| Concept | Description |
|---|---|
| **Classes Abstraites (ABC)** | Définissent une interface commune que tous les processeurs doivent implémenter |
| **Méthodes Abstraites** | Forcent les sous-classes à implémenter `validate` et `ingest` |
| **Héritage** | Les processeurs spécialisés héritent de `DataProcessor` |
| **Surcharge de Méthode** | Chaque processeur redéfinit les méthodes avec sa propre logique |
| **Polymorphisme** | Le flux appelle `validate` sans savoir à quel processeur il s'adresse |
| **Duck Typing (Protocol)** | Les plugins d'export sont compatibles par structure, pas par héritage |
| **Annotations de Types** | Couverture complète vérifiée avec `mypy --strict` |
| **Gestion des Exceptions** | Les données invalides lèvent des exceptions pour protéger le pipeline |

---

## Structure du Projet

```
Module5/
├── ex0/
│   └── data_processor.py     # Classe abstraite + 3 processeurs spécialisés
├── ex1/
│   └── data_stream.py        # Routeur DataStream avec dispatch polymorphique
└── ex2/
    └── data_pipeline.py      # Pipeline complet avec plugins CSV et JSON
```

---

## Exercices

### Exercice 0 — Processeur de Données

**Fichier :** `ex0/data_processor.py`

Construit les fondations du système avec une classe abstraite et trois processeurs spécialisés.

#### Hiérarchie des Classes

```
DataProcessor (ABC)
├── validate(data: Any) -> bool        # abstraite
├── ingest(data: Any) -> None          # abstraite
└── output() -> tuple[int, str]        # concrète — extraction FIFO

NumericProcessor(DataProcessor)
├── Accepte : int, float, list[int | float]
└── Stocke : représentation str + rang

TextProcessor(DataProcessor)
├── Accepte : str, list[str]
└── Stocke : string brute + rang

LogProcessor(DataProcessor)
├── Accepte : dict[str, str], list[dict[str, str]]
└── Stocke : format "LEVEL: message" + rang
```

#### Décisions de Conception

- `validate(self, data: Any) -> bool` — même signature dans toutes les classes, accepte n'importe quoi et retourne un booléen
- `ingest` a des **signatures spécifiques** par sous-classe reflétant les types acceptés
- `output` extrait l'élément **le plus ancien** (FIFO) avec son rang d'ingestion — le rang ne diminue jamais même après les extractions
- Les appels invalides à `ingest` lèvent une `ValueError`

#### Exemple de Sortie

```
=== Code Nexus - Data Processor ===
Testing Numeric Processor...
Trying to validate input '42': True
Trying to validate input 'Hello': False
Test invalid ingestion of string 'foo' without prior validation:
Got exception: Improper numeric data
Processing data: [1, 2, 3, 4, 5]
Extracting 3 values...
Numeric value 0: 1
Numeric value 1: 2
Numeric value 2: 3
```

---

### Exercice 1 — Flux de Données Polymorphique

**Fichier :** `ex1/data_stream.py`

Introduit la classe `DataStream` — un routeur qui reçoit des données mixtes et dispatche chaque élément vers le bon processeur grâce au **polymorphisme**.

#### Méthodes de DataStream

| Méthode | Description |
|---|---|
| `register_processor(proc)` | Enregistre un processeur dans le flux |
| `process_stream(stream)` | Route chaque élément vers le premier processeur compatible |
| `print_processors_stats()` | Affiche le total traité et les éléments restants par processeur |

#### Comment Fonctionne le Routage

```python
for element in stream:
    for processor in self._processors:
        if processor.validate(element):   # appel polymorphique
            processor.ingest(element)     # appel polymorphique
            break
    else:
        print(f"DataStream error - Can't process element: {element}")
```

`DataStream` ne sait jamais s'il parle à un `NumericProcessor` ou un `LogProcessor` — il appelle juste `validate` et Python fait le reste. C'est le **polymorphisme de sous-type** en action.

#### Exemple de Sortie

```
=== Code Nexus - Data Stream ===
Initialize Data Stream...
== DataStream statistics ==
No processor found, no data
Registering Numeric Processor
...
== DataStream statistics ==
Numeric Processor: total 8 items processed, remaining 8 on processor
Text Processor: total 3 items processed, remaining 3 on processor
Log Processor: total 2 items processed, remaining 2 on processor
```

---

### Exercice 2 — Pipeline de Données

**Fichier :** `ex2/data_pipeline.py`

Complète le pipeline avec un **système de plugins d'export** basé sur le **duck typing** via `Protocol`.

#### Protocol ExportPlugin

```python
class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None: ...
```

Toute classe implémentant `process_output` avec la bonne signature est automatiquement compatible — pas besoin d'héritage explicite.

#### Plugins Disponibles

**CSVExportPlugin** — affiche les valeurs séparées par des virgules :
```
CSV Output:
3.14,-1,2.71
```

**JSONExportPlugin** — affiche un objet JSON en utilisant le rang d'ingestion comme clé :
```
JSON Output:
{"item_3": "42", "item_4": "21", "item_5": "32"}
```

#### output_pipeline

```python
def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
    for process in self._processors:
        items = []
        for i in range(min(nb, len(process._data))):
            items.append(process.output())
        plugin.process_output(items)
```

Consomme jusqu'à `nb` éléments de chaque processeur et les envoie au plugin. Utilise `min` pour éviter d'extraire plus que ce qui est disponible.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    DataStream                        │
│  ┌─────────────────────────────────────────────┐    │
│  │           process_stream(stream)             │    │
│  │  pour chaque élément :                       │    │
│  │    → validate() sur chaque processeur        │    │
│  │    → ingest() sur le premier compatible      │    │
│  └─────────────────────────────────────────────┘    │
│  ┌──────────────┐ ┌─────────────┐ ┌─────────────┐  │
│  │   Numeric    │ │    Text     │ │     Log     │  │
│  │  Processor   │ │  Processor  │ │  Processor  │  │
│  └──────────────┘ └─────────────┘ └─────────────┘  │
│  ┌─────────────────────────────────────────────┐    │
│  │         output_pipeline(nb, plugin)          │    │
│  │  → CSVExportPlugin  ou  JSONExportPlugin     │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

---

## Prérequis

- Python 3.10+
- `flake8` — vérification du style de code
- `mypy` — vérification statique des types

```bash
pip install flake8 mypy black
```

Imports autorisés : `abc` et `typing` uniquement.

---

## Utilisation

```bash
# Exercice 0
python3 Module5/ex0/data_processor.py

# Exercice 1
python3 Module5/ex1/data_stream.py

# Exercice 2
python3 Module5/ex2/data_pipeline.py
```

```bash
# Vérifier le style de code
flake8 Module5/

# Vérifier les types
mypy Module5/ --strict

# Formater automatiquement
black --line-length 79 Module5/
```

---

*Construit dans le cadre d'un programme d'apprentissage Python — Code Nexus, 2087.*