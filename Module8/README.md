# 🔴 The Matrix — Bienvenue dans le Monde Réel de la Data Engineering

> *"Tu prends la pilule bleue, l'histoire s'arrête. Tu prends la pilule rouge, tu restes au pays des merveilles et je te montre jusqu'où va le terrier."* - Morpheus

---

## 📋 Table des Matières

- [Présentation](#présentation)
- [Concepts Abordés](#concepts-abordés)
- [Structure du Projet](#structure-du-projet)
- [Exercices](#exercices)
  - [Exercice 0 — Entering the Matrix](#exercice-0--entering-the-matrix)
  - [Exercice 1 — Loading Programs](#exercice-1--loading-programs)
  - [Exercice 2 — Accessing the Mainframe](#exercice-2--accessing-the-mainframe)
- [Prérequis](#prérequis)
- [Utilisation](#utilisation)

---

## Présentation

**The Matrix** est un projet Python centré sur les outils fondamentaux de la data engineering : les environnements virtuels, la gestion de packages et la configuration sécurisée via variables d'environnement. Ces compétences sont essentielles pour construire des systèmes robustes et maintenables dans le monde réel.

---

## Concepts Abordés

| Concept | Description |
|---|---|
| **Environnement virtuel** | Espace isolé pour installer des packages sans affecter le système global |
| **`venv`** | Outil Python natif pour créer des environnements virtuels |
| **`pip`** | Gestionnaire de packages Python — installe depuis `requirements.txt` |
| **`Poetry`** | Gestionnaire moderne — résout les conflits de versions automatiquement |
| **`requirements.txt`** | Liste des dépendances pour pip |
| **`pyproject.toml`** | Fichier de configuration Poetry avec gestion des versions |
| **Variables d'environnement** | Stocker des secrets et configurations en dehors du code |
| **`.env`** | Fichier de configuration locale — ne jamais commiter sur git |
| **`python-dotenv`** | Librairie pour charger les variables depuis un fichier `.env` |

---

## Structure du Projet

```
Module8/
├── .venv/                 # Environnement virtuel (ne pas commiter)
├── ex0/
│   └── construct.py       # Détection d'environnement virtuel
├── ex1/
│   ├── loading.py         # Programme d'analyse de données
│   ├── requirements.txt   # Dépendances pip
│   └── pyproject.toml     # Dépendances Poetry
└── ex2/
    ├── oracle.py          # Système de configuration sécurisé
    ├── .env.example       # Modèle de configuration (commiter)
    ├── .env               # Configuration réelle (ne pas commiter)
    └── .gitignore         # Fichiers à exclure du git
```

---

## Exercices

### Exercice 0 — Entering the Matrix

**Fichier :** `ex0/construct.py`

Détecte si le programme tourne dans un environnement virtuel ou non, et affiche des informations sur l'environnement Python actuel.

#### Comment détecter un venv

```python
import sys
import os

# Si sys.prefix != sys.base_prefix → on est dans un venv
in_venv = sys.prefix != sys.base_prefix

# Nom du venv
venv_name = os.path.basename(os.environ.get('VIRTUAL_ENV', ''))
```

#### Sortie hors venv

```
MATRIX STATUS: You're still plugged in
Current Python: /usr/bin/python3
Virtual Environment: None detected
WARNING: You're in the global environment!
To enter the construct, run:
python -m venv matrix_env
source matrix_env/bin/activate # On Unix
matrix_env\Scripts\activate # On Windows
```

#### Sortie dans un venv

```
MATRIX STATUS: Welcome to the construct
Current Python: /path/to/matrix_env/bin/python
Virtual Environment: matrix_env
Environment Path: /path/to/matrix_env
SUCCESS: You're in an isolated environment!
Package installation path:
/path/to/matrix_env/lib/python3.10/site-packages
```

#### Pourquoi les venvs sont essentiels

Sans venv, `pip` installe dans deux endroits :
- `/usr/lib/python3/dist-packages/` → apt (système)
- `/home/user/.local/lib/python3.10/site-packages/` → pip (utilisateur)

Python peut mélanger les deux et créer des conflits ! Le venv isole tout dans un seul endroit.

---

### Exercice 1 — Loading Programs

**Fichiers :** `ex1/loading.py`, `ex1/requirements.txt`, `ex1/pyproject.toml`

Programme d'analyse de données qui utilise pandas, numpy et matplotlib, avec gestion gracieuse des dépendances manquantes.

#### Différence pip vs Poetry

| | `pip` | `Poetry` |
|---|---|---|
| Fichier config | `requirements.txt` | `pyproject.toml` |
| Gestion conflits | Manuel | Automatique |
| Reproductibilité | Partielle | Totale (via `.lock`) |
| Commande install | `pip install -r requirements.txt` | `poetry install` |
| Commande run | `python3 loading.py` | `poetry run python loading.py` |

#### Détection des dépendances

```python
import importlib.util
import importlib.metadata

def check_dependency(name: str, description: str) -> bool:
    if importlib.util.find_spec(name) is not None:
        version = importlib.metadata.version(name)
        print(f"[OK] {name} ({version}) - {description}")
        return True
    print(f"[MISSING] {name} - {description}")
    return False
```

#### Installation

```bash
# Avec pip
pip install -r ex1/requirements.txt

# Avec Poetry
cd ex1
poetry install
poetry run python loading.py
```

#### Sortie attendue

```
LOADING STATUS: Loading programs...
Checking dependencies:
[OK] pandas (2.3.3) - Data manipulation ready
[OK] numpy (1.26.4) - Numerical computation ready
[OK] matplotlib (3.8.0) - Visualization ready
Analyzing Matrix data...
Processing 1000 data points...
Generating visualization...
Analysis complete!
Results saved to: matrix_analysis.png
```

---

### Exercice 2 — Accessing the Mainframe

**Fichiers :** `ex2/oracle.py`, `ex2/.env.example`, `ex2/.gitignore`

Système de configuration sécurisé qui charge des variables depuis un fichier `.env` avec `python-dotenv`.

#### Pourquoi ne jamais hardcoder les secrets

```python
# ❌ JAMAIS faire ça
API_KEY = "mon_secret_123"
DATABASE_URL = "postgresql://user:password@localhost/db"

# ✅ Toujours utiliser les variables d'environnement
API_KEY = os.getenv("API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
```

Si tu hardcodes tes secrets dans le code et que tu pousses sur git → **tout le monde peut les voir** !

#### Variables de configuration

| Variable | Description | Exemple |
|---|---|---|
| `MATRIX_MODE` | Mode d'exécution | `development` ou `production` |
| `DATABASE_URL` | Connexion base de données | `postgresql://localhost/matrix` |
| `API_KEY` | Clé API secrète | `sk-abc123...` |
| `LOG_LEVEL` | Niveau de logs | `DEBUG`, `INFO`, `ERROR` |
| `ZION_ENDPOINT` | URL réseau Zion | `http://zion.local:8080` |

#### Les 3 cas de test

```bash
# Cas 1 — Sans configuration
python3 ex2/oracle.py
# → affiche des warnings pour les variables manquantes

# Cas 2 — Avec .env
cp ex2/.env.example ex2/.env
python3 ex2/oracle.py
# → charge la configuration depuis .env

# Cas 3 — Override production
MATRIX_MODE=production API_KEY=secret123 python3 ex2/oracle.py
# → les variables en ligne de commande écrasent le .env
```

#### `.env.example` vs `.env`

- `.env.example` → **commité** sur git, valeurs fictives, sert de modèle
- `.env` → **jamais commité**, vraies valeurs, dans `.gitignore`

---

## Prérequis

- Python 3.10+
- `pip` — installé avec Python
- `Poetry` — gestionnaire moderne

```bash
# Installer Poetry
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"

# Installer python-dotenv
pip install python-dotenv
```

---

## Utilisation

```bash
# Créer et activer le venv
python3 -m venv .venv
source .venv/bin/activate

# Exercice 0
python3 ex0/construct.py

# Exercice 1 — avec pip
pip install -r ex1/requirements.txt
python3 ex1/loading.py

# Exercice 1 — avec Poetry
cd ex1 && poetry install && poetry run python loading.py

# Exercice 2
cp ex2/.env.example ex2/.env
python3 ex2/oracle.py

# Ne jamais commiter le venv et le .env !
echo ".venv/" >> .gitignore
echo ".env" >> .gitignore
```

---

*The Matrix — "Il n'y a pas de cuillère. Mais il y a des environnements virtuels, et ils sont bien réels."*