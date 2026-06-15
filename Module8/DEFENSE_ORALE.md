# Module 8 — *The Matrix* : Dossier théorique pour la défense orale

> Document de travail personnel. Il décortique en profondeur **chaque concept** du
> sujet et le relie à ton code (`ex0/construct.py`, `ex1/loading.py`,
> `ex2/oracle.py`). Objectif : que tu puisses **expliquer le *pourquoi*** et pas
> seulement le *comment*, car le peer-review note la compréhension, pas la
> simple exécution.

Le sujet annonce noir sur blanc ce que tu devras démontrer à l'oral :

1. Ta compréhension des **environnements virtuels** et pourquoi ils sont importants.
2. Les **différences entre pip et Poetry** pour la gestion des dépendances.
3. Comment les **variables d'environnement** rendent une application sûre et configurable.
4. Ta capacité à **expliquer ces concepts** à d'autres apprenants.

Ce document est organisé exactement autour de ces 4 axes.

---

## Table des matières

- [Partie 1 — Les environnements virtuels (ex0)](#partie-1)
- [Partie 2 — pip vs Poetry (ex1)](#partie-2)
- [Partie 3 — Variables d'environnement & configuration (ex2)](#partie-3)
- [Partie 4 — Concepts transverses (flake8, mypy, exceptions, typage)](#partie-4)
- [Partie 5 — Banque de questions/réponses pour la défense](#partie-5)
- [Annexe — Lexique express](#annexe)

---

<a name="partie-1"></a>
## Partie 1 — Les environnements virtuels (ex0 : `construct.py`)

### 1.1 Le problème de départ : pourquoi isoler ?

Un interpréteur Python installé « globalement » (le `/usr/bin/python3` du système)
possède **un seul** dossier `site-packages` où atterrissent toutes les
bibliothèques installées par `pip`. Conséquences si on installe tout là-dedans :

- **Conflits de versions (« dependency hell »).** Le projet A a besoin de
  `numpy==1.26`, le projet B de `numpy==2.4`. Un seul site-packages global ne peut
  contenir qu'**une** version à la fois → l'un des deux projets casse.
- **Pollution du Python système.** Sur Linux, des outils du système dépendent du
  Python système. Installer/mettre à jour des paquets globalement peut casser
  l'OS. (C'est pour ça que les distributions récentes refusent `pip install` en
  global : erreur *externally-managed-environment*, PEP 668.)
- **Non-reproductibilité.** Impossible de dire « ce projet a besoin de ces
  versions précises » si tout est mélangé dans un seul environnement partagé.
- **Droits.** Le site-packages global appartient souvent à `root` → installation
  nécessitant `sudo`, donc dangereux et non portable.

> **Phrase de défense :** « Un environnement virtuel résout le *dependency hell* :
> chaque projet a son propre site-packages isolé, donc ses propres versions, sans
> polluer le Python système ni les autres projets. »

### 1.2 Qu'est-ce **physiquement** qu'un venv ?

`python3 -m venv matrix_env` crée un **dossier** qui contient :

```
matrix_env/
├── bin/                     (Scripts/ sous Windows)
│   ├── python -> /usr/bin/python3   (lien symbolique vers le Python de base)
│   ├── activate             (script à "sourcer" dans le shell)
│   └── pip
├── lib/python3.X/site-packages/      (LE site-packages isolé du venv)
├── include/
└── pyvenv.cfg               (fichier de config qui "fait" le venv)
```

Le venv **ne copie pas** tout Python : il crée surtout un **lien** vers
l'interpréteur de base + son **propre** `site-packages` vide + un fichier
`pyvenv.cfg`. C'est léger et c'est ce qui explique pourquoi **on ne le commit
jamais** (voir §1.6).

`pyvenv.cfg` ressemble à :

```ini
home = /usr/bin
include-system-site-packages = false
version = 3.X.Y
```

C'est ce fichier qui dit à l'interpréteur : « ton Python de base est là, et tu ne
dois PAS voir les paquets du système ».

### 1.3 Le mécanisme d'isolation : `sys.prefix` vs `sys.base_prefix`

C'est **le cœur théorique** de l'exercice 0.

- `sys.prefix` = racine de l'environnement Python **courant**.
- `sys.base_prefix` = racine de l'installation Python **de base** (introduit par
  la **PEP 405**, Python 3.3).

| Situation | `sys.prefix` | `sys.base_prefix` | Égaux ? |
|---|---|---|---|
| **Hors venv** (Python système) | `/usr` | `/usr` | **oui** |
| **Dans un venv** | `/.../matrix_env` | `/usr` | **non** |

D'où la détection canonique, exactement celle de ton code :

```python
if sys.prefix != sys.base_prefix:
    # on est DANS un environnement virtuel
```

> **Pourquoi c'est la *bonne* méthode ?** Parce qu'elle est **fiable même sans
> activation**. Si tu lances directement `matrix_env/bin/python construct.py`
> *sans* faire `source activate`, l'isolation fonctionne quand même (l'interpréteur
> lit `pyvenv.cfg` au démarrage et ajuste `sys.prefix`). Tester la variable
> d'environnement `VIRTUAL_ENV` seule serait **faux** dans ce cas (voir §1.5).

### 1.4 Ce que fait `source activate` (et ce qu'il ne fait PAS)

`source matrix_env/bin/activate` (le `source` est obligatoire : il faut que le
script modifie **ton shell courant**, pas un sous-shell) fait 3 choses :

1. **Prépend** `matrix_env/bin` au `PATH` → quand tu tapes `python`, le shell
   trouve d'abord celui du venv.
2. **Exporte** la variable d'environnement `VIRTUAL_ENV=/.../matrix_env`.
3. Modifie le **prompt** (le fameux `(matrix_env) $>`) et définit la commande
   `deactivate`.

> **Point clé de compréhension :** `activate` ne « rentre » pas magiquement dans
> un venv. Il ne fait que **réordonner le PATH**. L'isolation réelle vient de
> l'interpréteur + `pyvenv.cfg`, pas de l'activation. L'activation est juste un
> **confort** pour ne pas taper le chemin complet.

### 1.5 Le nom et le chemin du venv : `VIRTUAL_ENV`

Le nom affiché (`matrix_env`) et le chemin viennent de la variable
`VIRTUAL_ENV`, que **seul `activate` pose**. Dans ton code :

```python
venv_name = os.path.basename(os.environ.get('VIRTUAL_ENV', ""))
print(f"Environment Path: {os.environ.get('VIRTUAL_ENV')}")
```

> **Question piège possible du correcteur :** « Et si je lance le python du venv
> sans l'activer ? » Réponse honnête : « La **détection** reste correcte
> (`sys.prefix != sys.base_prefix`), mais le **nom** sera vide car `VIRTUAL_ENV`
> n'est posée que par `activate`. Les exemples du sujet activent toujours
> l'environnement, donc le cas nominal est couvert. »

### 1.6 Pourquoi NE PAS commiter le venv (consigne explicite du sujet)

- **Chemins absolus.** `pyvenv.cfg` et les scripts contiennent des chemins
  absolus de TA machine → inutilisables ailleurs.
- **Spécifique à l'OS/l'archi.** Les binaires (`bin/python`, paquets compilés
  comme numpy) sont liés à ton OS et à ton CPU → incassables/non portables.
- **Taille & bruit.** Des milliers de fichiers qui polluent le dépôt et les diffs.
- **Reproductibilité par la recette, pas par le résultat.** On versionne la
  **recette** (`requirements.txt` / `pyproject.toml`) qui permet de **recréer**
  l'environnement n'importe où. C'est exactement ce que dit le sujet : *« You
  must be able to create a new one during review. »*

### 1.7 `site.getsitepackages()` — où vont les paquets

Le module **`site`** s'exécute au démarrage de Python et ajoute les dossiers
`site-packages` au `sys.path` (la liste où Python cherche les modules à importer).
`site.getsitepackages()` renvoie ces dossiers :

- **Hors venv** → un chemin **global** (ex. `/usr/local/lib/python3.X/dist-packages`).
- **Dans un venv** → le chemin **du venv** (`/.../matrix_env/lib/python3.X/site-packages`).

C'est ce qui te permet de **« montrer la différence entre l'emplacement des
paquets global et venv »** (consigne du sujet) : tu affiches ce chemin dans les
deux branches de ton `if/else`.

### 1.8 Lecture commentée de `construct.py`

```python
import sys, os, site                       # uniquement les modules autorisés

if sys.prefix != sys.base_prefix:          # §1.3 : détection fiable du venv
    # --- branche "DANS le venv" ---
    sys.executable                         # chemin du python courant (du venv)
    os.environ.get('VIRTUAL_ENV')          # §1.5 : nom/chemin posés par activate
    site.getsitepackages()[0]              # §1.7 : site-packages du venv
else:
    # --- branche "HORS venv" ---
    site.getsitepackages()[0]              # §1.7 : site-packages global (la diff)
    # + instructions pour créer/activer un venv (consigne du sujet)
```

---

<a name="partie-2"></a>
## Partie 2 — pip vs Poetry (ex1 : `loading.py` + `requirements.txt` + `pyproject.toml`)

### 2.1 pip : l'installateur historique

- **pip** installe des paquets depuis **PyPI** (Python Package Index).
- Formats : **wheel** (`.whl`, pré-compilé, rapide) ou **sdist** (source, à
  compiler). pip préfère les wheels.
- Depuis pip 20.3, pip a un **vrai résolveur** (backtracking) qui essaie de
  trouver un jeu de versions compatibles.
- **pip ne gère PAS les environnements virtuels** : tu crées le venv toi-même
  (`python -m venv`), puis tu `pip install` dedans. pip et venv sont deux outils
  séparés qui se complètent.

#### `requirements.txt`

Un simple fichier texte, une exigence par ligne. Le tien :

```
pandas==2.3.3
numpy==1.26.4
matplotlib==3.8.0
```

- `==` = **épinglage exact** (exact pin). On force LA version.
- On l'installe avec `pip install -r requirements.txt`.

> **La grande faiblesse de pip seul :** un `requirements.txt` écrit à la main ne
> liste en général que les dépendances **directes**. Les dépendances
> **transitives** (les dépendances de tes dépendances) ne sont **pas figées** →
> deux installations à deux moments différents peuvent récupérer des versions
> transitives différentes → **non reproductible**. Pour le rendre reproductible
> il faut un `pip freeze` (qui fige tout) ou un outil comme `pip-tools`.

### 2.2 Poetry : gestionnaire de dépendances + packaging + venv

Poetry fait **trois** métiers en un :

1. **Gestion des dépendances** (résolution + verrouillage).
2. **Gestion de l'environnement virtuel** (il en crée/gère un tout seul).
3. **Packaging** (construire et publier une bibliothèque).

#### `pyproject.toml` : la source unique de vérité

Fichier standardisé par les **PEP 518** (section `[build-system]`) et **PEP 621**
(métadonnées de projet). Poetry a historiquement utilisé la table
`[tool.poetry]`. Le tien :

```toml
[tool.poetry]
package-mode = false              # voir §2.4 (le point vicieux)
name = "matrix-loading"
version = "0.1.0"
...
[tool.poetry.dependencies]
python = "^3.10"
pandas = "^2.3.3"
numpy = "^1.26.4"
matplotlib = "^3.8.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

#### Le `^` (caret) et le versionnage sémantique (SemVer)

SemVer = `MAJEUR.MINEUR.CORRECTIF` :

- **MAJEUR** : changement **cassant** (incompatible).
- **MINEUR** : nouvelle fonctionnalité **rétro-compatible**.
- **CORRECTIF** : correction de bug **rétro-compatible**.

Le caret `^` autorise les mises à jour **qui ne changent pas le numéro MAJEUR** :

| Contrainte | Signifie | Logique |
|---|---|---|
| `^2.3.3` | `>=2.3.3, <3.0.0` | tout 2.x compatible |
| `^1.26.4` | `>=1.26.4, <2.0.0` | tout 1.x compatible |
| `^3.8.0` | `>=3.8.0, <4.0.0` | tout 3.x compatible |

> **Contraste pédagogique fort à sortir à l'oral :** pip avec `==` fige une
> version **exacte** ; Poetry avec `^` exprime une **plage compatible**. Mais
> alors, comment Poetry reste-t-il reproductible malgré des plages ? → grâce au
> **lock file** (juste en dessous).

#### `poetry.lock` : la reproductibilité déterministe

Quand tu fais `poetry install`, Poetry :

1. **Résout** tout le graphe de dépendances (directes **ET** transitives) à
   partir des plages du `pyproject.toml`.
2. **Écrit** dans `poetry.lock` les **versions exactes** retenues **+ les hashes**
   (empreintes de sécurité) de chaque paquet.
3. Installe **exactement** ce que dit le lock.

Tant que le `poetry.lock` est présent, **tout le monde obtient le même
environnement, au paquet et au hash près** — y compris les dépendances
transitives. C'est ça que pip seul (sans freeze) ne garantit pas.

### 2.3 Le tableau récapitulatif pip vs Poetry (à connaître par cœur)

| Critère | **pip** | **Poetry** |
|---|---|---|
| Rôle | Installateur de paquets | Dépendances + venv + packaging |
| Fichier de déclaration | `requirements.txt` | `pyproject.toml` |
| Notation des versions | exact (`==`) écrit à la main | plages (`^`, `~`) |
| Verrouillage transitif | ❌ non (sauf `pip freeze`) | ✅ `poetry.lock` (+ hashes) |
| Reproductibilité totale | partielle | ✅ déterministe |
| Gère le venv | ❌ (séparé) | ✅ intégré |
| Dépendances de dev séparées | ❌ (à la main) | ✅ groupes (`--group dev`) |
| Standardisé (PEP) | convention | `pyproject.toml` (PEP 518/621) |

> **Phrase de synthèse :** « pip **installe** ; Poetry **gère** : il résout,
> verrouille (lock + hashes), isole l'environnement et sait packager. pip avec
> `requirements.txt` est minimal et universel ; Poetry est plus complet et
> reproductible. »

### 2.4 Le point vicieux : `package-mode = false`

Le sujet impose que `poetry install` **fonctionne**. Or, par défaut, Poetry
considère ton projet comme **un paquet à installer**. Avec `name =
"matrix-loading"`, il cherche un module/dossier `matrix_loading` à installer… qui
**n'existe pas** (tu n'as qu'un script `loading.py`). Résultat : `poetry install`
**échoue** :

```
The current project could not be installed: No file/folder found for package matrix-loading
```

`package-mode = false` (Poetry ≥ 1.8) dit : **« je ne package rien, je veux juste
gérer des dépendances »**. Du coup `poetry install` installe les dépendances et
**n'essaie plus** d'installer le projet → plus d'erreur. C'est exactement ton
cas d'usage (Poetry comme gestionnaire de deps, pas comme outil de publication).

> **Si on le mettait à `true`** (= défaut), il faudrait *en plus* soit créer un
> vrai package `matrix_loading/`, soit lancer `poetry install --no-root` — deux
> contournements qui sortent du rendu demandé. Donc **`false` est la bonne
> réponse.**

### 2.5 Détecter une dépendance SANS l'importer : `importlib`

Le sujet demande de **gérer gracieusement les dépendances manquantes** et précise
que *« flake8 et mypy errors are allowed for this exercise, only for import
errors »*, tout en suggérant qu'*« il existe une mécanique pour les éviter »*.

Ta mécanique = **`importlib`** :

```python
import importlib.util, importlib.metadata

def check_dependency(name, description):
    if importlib.util.find_spec(name) is not None:   # le module est-il importable ?
        version = importlib.metadata.version(name)   # version installée (métadonnées)
        ...
```

- `importlib.util.find_spec(name)` répond « ce module est-il installé ? » **sans
  l'importer** (donc sans crash si absent, et sans `import numpy` au niveau global
  qui ferait hurler mypy/flake8).
- `importlib.metadata.version(name)` lit la **version** dans les métadonnées du
  paquet (PEP 566).

Les vrais `import numpy as np` / `pandas` / `matplotlib` n'ont lieu **qu'à
l'intérieur du `try`**, une fois qu'on sait que tout est présent. C'est ce qui
rend la **vérification** propre. Les seules erreurs mypy restantes portent sur ces
imports tardifs → **précisément celles que le sujet autorise**.

> **Pourquoi mypy crie sur ces imports ?** Parce que sans les paquets installés
> dans l'environnement de mypy, il ne trouve ni le module ni ses *stubs* de types
> (voir Partie 4). C'est documentaire, pas un défaut de logique.

### 2.6 numpy comme SOURCE des données (consigne vicieuse)

Le sujet est explicite : *« It must be the source of your dataset — not hardcoded
lists or range() »*. D'où :

```python
data = np.random.randn(1000)        # 1000 tirages gaussiens : numpy GÉNÈRE les données
df = pd.DataFrame(data, columns=["matrix_signal"])   # pandas MANIPULE
plt.savefig("matrix_analysis.png")  # matplotlib VISUALISE
```

- `np.random.randn(1000)` = 1000 valeurs aléatoires (loi normale). C'est **numpy**
  qui produit le jeu de données, pas une liste écrite à la main ni `range()`.
- **Pourquoi cette exigence ?** Pédagogiquement, pour prouver que tu sais te
  servir de numpy comme moteur de calcul/génération, pas juste « afficher des
  chiffres ». C'est le cœur métier d'un *data engineer*.
- **`requests` n'apparaît pas** dans ta sortie : le sujet dit que la ligne
  `requests` ne s'affiche **que si tu interroges une API**. Tu simules avec numpy
  → pas d'API → pas de `requests`. **C'est volontaire et correct.**

---

<a name="partie-3"></a>
## Partie 3 — Variables d'environnement & configuration (ex2 : `oracle.py` + `.env.example` + `.gitignore`)

### 3.1 Qu'est-ce qu'une variable d'environnement ?

Une **variable d'environnement** est un couple `CLÉ=VALEUR` (toujours du texte)
attaché au **processus**. Un processus **hérite** de l'environnement de son parent
(le shell). Donc quand le shell lance `python3`, Python reçoit une copie de
l'environnement du shell, lisible via `os.environ` / `os.getenv`.

Deux façons de poser une variable dans un shell :

```bash
export MATRIX_MODE=production        # persistante pour toutes les commandes suivantes
MATRIX_MODE=production python3 oracle.py   # juste pour CE processus python
```

### 3.2 Le principe : la config dans l'environnement (12-Factor App)

La méthodologie **« 12-Factor App »** (facteur III) énonce : **« stocke la
configuration dans l'environnement »**, strictement **séparée du code**. Pourquoi ?

- Le **code** est identique partout (dev, test, prod).
- La **config** (URL de base de données, clés d'API, niveau de log) **change**
  d'un déploiement à l'autre.
- On ne doit donc **jamais** coder en dur ces valeurs dans le code source.

> **Phrase de défense :** « Le code ne change pas entre dev et prod ; seule la
> configuration change. On l'injecte par l'environnement pour garder un code
> unique, configurable et sûr. »

### 3.3 Les fichiers `.env` et la bibliothèque `python-dotenv`

- Un fichier **`.env`** est une **convention** (issue de l'écosystème 12-factor) :
  des lignes `CLÉ=VALEUR`. **Python ne le lit PAS tout seul.**
- **`python-dotenv`** est la bibliothèque qui lit ce fichier et **injecte** ses
  valeurs dans `os.environ` :

```python
from dotenv import load_dotenv
load_dotenv(env_path)          # lit .env et peuple os.environ
```

> **Pourquoi le sujet impose python-dotenv et interdit un parseur maison ?** Pour
> t'apprendre l'**outil standard** et la **bonne pratique**, pas pour réinventer
> un analyseur de fichier. Le sujet le dit explicitement.

### 3.4 La règle de précédence (le point vicieux de l'override)

`load_dotenv()` a par défaut `override=False` : il **ne réécrit pas** une variable
**déjà présente** dans l'environnement. D'où l'ordre de priorité :

```
variable réelle de l'environnement  >  valeur du .env  >  valeur par défaut du code
```

C'est exactement ce que teste le sujet :

```bash
MATRIX_MODE=production API_KEY=secret123 python3 oracle.py
```

Ici `MATRIX_MODE` et `API_KEY` sont déjà dans l'environnement du processus **avant**
l'appel à `load_dotenv`. Comme `override=False`, le `.env` ne les écrase pas → les
valeurs de la **ligne de commande gagnent**. Les autres variables (non fournies en
CLI) viennent, elles, du `.env`. C'est le comportement attendu : *« use
environment variables over .env file »*.

### 3.5 Sécurité : `.gitignore`, secrets et `.env.example`

Le sujet insiste : *« Never commit real secrets! Your .env file should be in
.gitignore. You must be able to explain why. »*

**Pourquoi `.env` doit être dans `.gitignore` :**

- Un `.env` contient des **secrets réels** (clés d'API, mots de passe de BDD).
- L'historique Git est **permanent** : même si tu supprimes le fichier plus tard,
  le secret **reste dans l'historique** et peut être récupéré. S'il a été poussé
  sur un dépôt distant, il peut avoir été **mis en cache/indexé** → considéré comme
  **compromis** (à révoquer).
- Donc : on **n'y met jamais** un secret. On l'ignore via `.gitignore`.

**Pourquoi committer `.env.example` (et pas `.env`) :**

- `.env.example` documente **quelles variables** sont nécessaires, avec des
  **valeurs factices** (placeholders) — aucun secret réel.
- Un nouveau développeur fait `cp .env.example .env` puis remplit ses **vraies**
  valeurs en local. C'est le flux exact des exemples du sujet.

Ton `.gitignore` :

```
.env            # ignore le fichier de secrets
matrix_env/     # ignore un éventuel venv
.venv/
```

> **Subtilité utile :** le motif `.env` **n'ignore pas** `.env.example` (ce sont
> deux noms de fichiers différents) → `.env.example` reste bien versionné. ✅

### 3.6 Différence dev/prod **visible** (consigne vicieuse)

Le sujet : *« Demonstrates different configuration for development/production…
**it must be visible in the output** »*. Ton implémentation (option « stricte en
prod ») :

```python
mode = verif("MATRIX_MODE", "NOT SET")
strict = mode == "production"          # True seulement en prod
db = verif("DATABASE_URL", "NOT SET", strict)
...

def verif(key, default_value, strict=False):
    value = os.getenv(key, default_value)
    if value == default_value:         # variable absente
        if strict:
            print(f"ERROR: {key} required in production")    # PROD : intransigeant
        else:
            print(f"WARNING: {key} not configured - using default")  # DEV : tolérant
```

**La justification métier (à dire à l'oral) :** en **développement**, on tolère
des valeurs manquantes avec des défauts pour itérer vite. En **production**, une
configuration manquante est une **erreur bloquante** : on ne lance jamais un
système réel sans sa config complète (sinon corruption de données, fuite,
indisponibilité). La différence est **visible** dans la sortie :

```bash
python3 oracle.py                      # → WARNING ... using default   (dev)
MATRIX_MODE=production python3 oracle.py   # → ERROR ... required in production (prod)
```

### 3.7 Gestion d'erreur (consigne générale)

Tout `oracle.py` est enveloppé dans un `try/except` :

```python
try:
    ...                                       # chargement + lecture config
except Exception as error:
    print(f"Configuration error: {error}")    # dégrade proprement, ne crash pas
```

Cela répond à *« Exception handling should protect the data streams from
corruption »* : si le chargement de config échoue, on **n'écrit pas** de données
sur une config corrompue, on affiche un message propre.

---

<a name="partie-4"></a>
## Partie 4 — Concepts transverses

### 4.1 flake8 (la norme de style)

`flake8` est un **agrégateur** de trois outils :

- **pycodestyle** : respect de la **PEP 8** (style : indentation, longueur de
  ligne ≤ 79, espaces…).
- **pyflakes** : erreurs **logiques** (imports inutilisés, variables non définies…).
- **mccabe** : **complexité** cyclomatique.

> Note : dans `loading.py`, j'ai coupé les lignes de `compare_managers()` en deux
> précisément pour rester **≤ 79 caractères** (règle E501 de la PEP 8).

### 4.2 mypy, le typage statique et les *stubs*

- Python est **typé dynamiquement**, mais la **PEP 484** a introduit les
  **annotations de types** et le **typage graduel** : on annote, et **mypy**
  vérifie statiquement la cohérence **sans exécuter** le code.
- Pour vérifier le code utilisant une **bibliothèque tierce**, mypy a besoin des
  **informations de types** de cette lib. Deux sources possibles :
  - la lib embarque ses types + un marqueur **`py.typed`** (**PEP 561**) — c'est le
    cas de **numpy**, **matplotlib** et **python-dotenv** ;
  - sinon il faut un **paquet de stubs** séparé (ex. `pandas-stubs` pour pandas).

**Conséquences concrètes dans ton projet :**

- **ex0** : que de la stdlib → mypy **clean**.
- **ex2** : `python-dotenv` embarque `py.typed` → **une fois installé**, mypy est
  **clean** (prouvé : *Success: no issues found*). L'erreur que tu vois en local
  vient **uniquement** du fait que `python-dotenv` n'est pas installé dans
  l'environnement où tourne mypy — **pas** d'un défaut de code.
- **ex1** : sans les paquets installés, mypy renvoie des erreurs d'**import** ;
  et même installés, **pandas** déclenche `import-untyped` tant que `pandas-stubs`
  n'est pas là. **Le sujet autorise explicitement** ces erreurs d'import pour ex1.

### 4.3 La philosophie de la gestion d'exceptions

*« Exception handling should protect the data streams from corruption. »* En *data
engineering*, une panne partielle (réseau coupé, fichier manquant, config
invalide) ne doit **jamais** corrompre les données en aval ni faire planter
brutalement le pipeline. On **encadre** les opérations risquées (I/O, imports,
parsing) par `try/except` pour **dégrader proprement**.

- **ex2** : tout est protégé (chargement de config = opération risquée).
- **ex1** : la partie analyse (imports + calcul + écriture du PNG) est protégée.
- **ex0** : **aucune** I/O ni flux de données (juste lecture de `sys`/`os`/`site`)
  → rien à protéger. L'absence de `try/except` y est **justifiable** :
  *« ex0 ne manipule aucun flux de données, il n'y a pas de risque de corruption. »*

---

<a name="partie-5"></a>
## Partie 5 — Banque de questions/réponses pour la défense

### Sur les environnements virtuels (ex0)

**Q : C'est quoi un environnement virtuel, concrètement ?**
R : Un dossier contenant un lien vers un interpréteur Python, son **propre**
`site-packages` isolé, et un `pyvenv.cfg`. Il permet à chaque projet d'avoir ses
propres versions de paquets sans polluer le Python système ni les autres projets.

**Q : Comment ton programme détecte-t-il le venv ?**
R : En comparant `sys.prefix` (racine de l'environnement courant) et
`sys.base_prefix` (racine de l'install de base, PEP 405). S'ils diffèrent, on est
dans un venv. C'est fiable **même sans activation**, contrairement à tester
`VIRTUAL_ENV`.

**Q : Que fait `source activate` ?**
R : Il prépend le `bin/` du venv au `PATH`, exporte `VIRTUAL_ENV`, change le
prompt. Il ne « rentre » pas dans le venv : l'isolation vient de l'interpréteur +
`pyvenv.cfg`, l'activation n'est qu'un confort.

**Q : Pourquoi ne pas committer le venv ?**
R : Chemins absolus, binaires spécifiques à l'OS/CPU, taille énorme, et surtout :
on versionne la **recette** (requirements/pyproject) pour **recréer** l'env
n'importe où, pas le résultat.

**Q : Pourquoi un venv est-il important ?**
R : Il évite le *dependency hell* (conflits de versions entre projets), protège le
Python système, et rend les projets reproductibles et portables.

### Sur pip vs Poetry (ex1)

**Q : Différence fondamentale pip / Poetry ?**
R : pip **installe** des paquets (`requirements.txt`, versions exactes `==`, pas
de verrouillage transitif). Poetry **gère** tout : résolution, **lock file**
(`poetry.lock` avec versions exactes + hashes pour tout le graphe), gestion du
venv, et packaging, à partir d'un `pyproject.toml` qui exprime des **plages** `^`.

**Q : Si Poetry utilise des plages `^`, comment reste-t-il reproductible ?**
R : Grâce au `poetry.lock` qui fige les versions exactes résolues (directes ET
transitives) + leurs hashes. Tout le monde réinstalle à l'identique.

**Q : C'est quoi `^2.3.3` ?**
R : `>=2.3.3, <3.0.0` — compatible tant que le numéro **majeur** ne change pas
(versionnage sémantique : majeur = changement cassant).

**Q : Pourquoi `package-mode = false` ?**
R : Pour que `poetry install` n'essaie pas d'installer mon projet comme un paquet
(il chercherait un module `matrix_loading` inexistant et échouerait). Je n'utilise
Poetry que pour gérer des dépendances, pas pour publier une lib.

**Q : Comment gères-tu les dépendances manquantes sans planter ?**
R : J'utilise `importlib.util.find_spec` pour tester la présence d'un module
**sans l'importer**, et `importlib.metadata.version` pour lire sa version. Les
vrais imports n'ont lieu que si tout est présent.

**Q : Pourquoi pas de ligne `requests` dans la sortie ?**
R : Le sujet précise qu'elle n'apparaît **que si on interroge une API**. Je simule
les données avec numpy → pas d'API → pas de `requests`.

### Sur les variables d'environnement (ex2)

**Q : Pourquoi des variables d'environnement plutôt que coder en dur ?**
R : Principe 12-factor : séparer config et code. Le code est identique partout,
seule la config change (dev/prod). Et on ne met jamais de secret dans le code.

**Q : Comment marche l'override en ligne de commande ?**
R : `load_dotenv` a `override=False` par défaut : il n'écrase pas une variable
déjà posée. Donc une variable fournie en CLI a priorité sur le `.env`. Ordre :
env réel > .env > défaut du code.

**Q : Pourquoi `.env` dans `.gitignore` ?**
R : Il contient des secrets réels. L'historique Git est permanent : un secret
committé reste récupérable même après suppression, et s'il est poussé il est
compromis. On committe seulement `.env.example` avec des valeurs factices.

**Q : Comment montres-tu la différence dev/prod ?**
R : En prod (`MATRIX_MODE=production`), une config manquante devient une **erreur**
bloquante ; en dev, c'est un simple **warning** avec valeur par défaut. C'est
visible dans la sortie.

**Q : Pourquoi python-dotenv et pas ton propre parseur ?**
R : Le sujet veut l'apprentissage de l'outil standard et de la bonne pratique, pas
la réinvention d'un analyseur de fichier.

### Questions transverses

**Q : Pourquoi ex0 n'a pas de `try/except` alors que ex1 et ex2 oui ?**
R : Parce qu'ex0 ne manipule aucun flux de données (juste de l'introspection
`sys`/`os`/`site`). La consigne parle de protéger les *data streams* : sans flux,
rien à protéger. ex1 (imports + I/O fichier) et ex2 (chargement de config) en ont.

**Q : Pourquoi mypy renvoie une erreur sur `dotenv` / numpy / pandas ?**
R : Parce que les bibliothèques ne sont pas installées dans l'environnement de
mypy, ou n'ont pas de stubs. Une fois `python-dotenv` installé (il embarque
`py.typed`), ex2 est clean. Pour ex1, le sujet **autorise** ces erreurs d'import.

---

<a name="annexe"></a>
## Annexe — Lexique express

| Terme | Définition courte |
|---|---|
| `site-packages` | Dossier où pip installe les paquets ; ajouté au `sys.path`. |
| `sys.prefix` / `sys.base_prefix` | Racine de l'env courant / de l'install de base. Diffèrent dans un venv (PEP 405). |
| `pyvenv.cfg` | Fichier qui définit un venv (chemin du Python de base, isolation). |
| `VIRTUAL_ENV` | Variable d'env posée par `activate` (nom/chemin du venv). |
| **wheel** / **sdist** | Paquet pré-compilé / paquet source à compiler. |
| **PyPI** | Dépôt public des paquets Python. |
| **SemVer** | `MAJEUR.MINEUR.CORRECTIF` (cassant / fonctionnalité / correctif). |
| `^` (caret) | Plage compatible sans changement de majeur (`^2.3.3` = `>=2.3.3,<3.0.0`). |
| `poetry.lock` | Verrouillage déterministe des versions exactes + hashes. |
| `package-mode = false` | Poetry gère seulement les deps, sans packager le projet. |
| `importlib.util.find_spec` | Teste si un module est importable **sans l'importer**. |
| **12-Factor App** | Méthodologie ; config dans l'environnement, séparée du code. |
| `.env` / `python-dotenv` | Fichier `CLÉ=VALEUR` / lib qui le charge dans `os.environ`. |
| `override=False` | `load_dotenv` n'écrase pas une variable déjà définie. |
| **py.typed** (PEP 561) | Marqueur indiquant qu'une lib fournit ses propres types. |
| **flake8** | pycodestyle (PEP 8) + pyflakes (logique) + mccabe (complexité). |
| **mypy** | Vérificateur de types statique (PEP 484, typage graduel). |
```
