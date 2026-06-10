# Défense — Data Archivist — Théorie complète

---

## 1. Les fichiers — concept fondamental

### Qu'est-ce qu'un fichier ?

Un fichier est une séquence d'octets (bytes) stockée sur un support persistant (disque dur, SSD). Le système d'exploitation gère l'accès aux fichiers via des **descripteurs de fichier** (*file descriptors*) — des identifiants numériques qui représentent une connexion ouverte entre le programme et le fichier.

Quand tu fais `open()`, le système d'exploitation :
1. Vérifie que le fichier existe et que tu as les permissions nécessaires.
2. Crée un descripteur de fichier (un entier, ex: `3`, `4`, `5`...).
3. Retourne cet accès à Python sous forme d'un objet fichier.

Le système a un **nombre limité** de descripteurs disponibles (typiquement 1024 par processus sous Linux). Si tu ne fermes pas tes fichiers, tu épuises cette ressource → les prochains `open()` échouent.

### Qu'est-ce qu'un buffer ?

Quand tu écris dans un fichier, Python n'écrit pas immédiatement sur le disque — c'est trop lent. Il accumule les données dans un **buffer** (zone mémoire temporaire) et les envoie en bloc au disque plus tard.

Conséquence : si le programme se termine brutalement sans fermer le fichier, les données dans le buffer peuvent être **perdues** et ne jamais atteindre le disque.

`.close()` force deux choses :
1. **Flush** : vider le buffer vers le disque.
2. **Libérer** le descripteur de fichier.

---

## 2. `open()` — tout ce qu'il faut savoir

### Ce que retourne `open()` — LA question du PDF

`open()` ne retourne **pas** le contenu du fichier. Il retourne un **objet fichier** (un *file object* ou *stream*).

Le type exact dépend du mode :
- Mode texte (`"r"`, `"w"`...) → `io.TextIOWrapper`
- Mode binaire (`"rb"`, `"wb"`...) → `io.BufferedReader` / `io.BufferedWriter`

De façon générique, on parle de `typing.IO` ou `TextIO`.

```python
f = open("file.txt", "r")
print(type(f))
# <class '_io.TextIOWrapper'>
```

C'est un objet qui représente la **connexion** au fichier, pas son contenu. Le contenu vient ensuite avec `.read()`.

### Les modes d'ouverture

| Mode | Comportement | Fichier inexistant |
|------|-------------|-------------------|
| `"r"` | Lecture seule, curseur au début | `FileNotFoundError` |
| `"w"` | Écriture, **écrase** le contenu existant, curseur au début | Crée le fichier |
| `"a"` | Écriture en ajout, curseur à la fin | Crée le fichier |
| `"x"` | Création exclusive | `FileExistsError` si existe déjà |
| `"r+"` | Lecture + écriture | `FileNotFoundError` |
| `"b"` | Mode binaire (combiné : `"rb"`, `"wb"`) | Retourne `bytes` |

### Les méthodes sur l'objet fichier

**`.read()`**
Lit **tout** le contenu depuis la position du curseur jusqu'à la fin. Retourne un `str` (mode texte) ou `bytes` (mode binaire).

```python
f = open("file.txt", "r")
content = f.read()   # str contenant tout le fichier
```

Si le fichier est vide ou si le curseur est déjà à la fin → retourne `""`.

**`.readline()`**
Lit une **seule ligne**, incluant le `\n` final (sauf sur la dernière ligne si elle n'en a pas).

```python
line = f.readline()   # "[FRAGMENT 001] ...\n"
```

**`.write(s)`**
Écrit la chaîne `s` à la position du curseur. Retourne le nombre de caractères écrits. **N'ajoute pas** de `\n` automatiquement — c'est à toi de les inclure.

**`.close()`**
Ferme le fichier : flush le buffer + libère le descripteur. Après `close()`, toute opération sur l'objet lève `ValueError: I/O operation on closed file`.

### Pourquoi `open()` peut-il échouer ?

- Le fichier **n'existe pas** → `FileNotFoundError` (`[Errno 2]`)
- Tu n'as **pas les permissions** → `PermissionError` (`[Errno 13]`)
- Le chemin pointe vers un **dossier** et pas un fichier → `IsADirectoryError` (`[Errno 21]`)
- Le **disque est plein** (à l'écriture) → `OSError` (`[Errno 28] No space left on device`)

Toutes ces erreurs héritent de `OSError`.

---

## 3. Gestion des exceptions — en profondeur

### Pourquoi les exceptions existent

En Python, quand une opération échoue, le programme ne continue pas silencieusement — il **lève** (raise) une exception. Une exception est un objet qui contient :
- Le **type** de l'erreur (ex: `FileNotFoundError`).
- Un **message** lisible (ex: `[Errno 2] No such file or directory: 'foo'`).
- Un **traceback** (la pile d'appels au moment de l'erreur).

Si personne n'attrape l'exception, elle remonte jusqu'au sommet et le programme **crash** avec un traceback affiché.

### La structure complète try/except

```python
try:
    # Code risqué
    f = open("file.txt", "r")
    text = f.read()

except FileNotFoundError as e:
    # Attrape spécifiquement FileNotFoundError
    print(f"Fichier introuvable : {e}")

except PermissionError as e:
    # Attrape spécifiquement PermissionError
    print(f"Permission refusée : {e}")

except Exception as e:
    # Filet large : attrape tout ce qui hérite d'Exception
    print(f"Erreur inattendue : {e}")

else:
    # S'exécute SEULEMENT si aucune exception n'a été levée dans le try
    print("Tout s'est bien passé")

finally:
    # S'exécute TOUJOURS : erreur ou pas, return ou pas
    f.close()
```

### Comment Python cherche le bon `except`

Quand une exception est levée, Python parcourt les `except` **dans l'ordre**, du premier au dernier, et s'arrête au **premier qui correspond** (en vérifiant si l'exception est une instance de la classe indiquée, ou d'une de ses sous-classes).

C'est pour ça que l'ordre est crucial :

```python
# ❌ MAUVAIS : Exception avale tout avant ValueError
except Exception as e:
    print(f"Erreur : {e}")
except ValueError as e:       # jamais atteint !
    print(f"Valeur : {e}")

# ✅ BON : spécifique avant général
except ValueError as e:
    print(f"Valeur : {e}")
except Exception as e:
    print(f"Erreur : {e}")
```

`ValueError` hérite de `Exception`. Donc `except Exception` matche aussi les `ValueError`. Si tu le mets en premier, il les avale.

### La hiérarchie complète des exceptions

```
BaseException
│
├── KeyboardInterrupt        ← Ctrl+C
├── SystemExit               ← sys.exit()
├── GeneratorExit
│
└── Exception
    │
    ├── ValueError           ← valeur incorrecte (ex: int("abc"))
    ├── TypeError            ← mauvais type (ex: "a" + 1)
    ├── EOFError             ← input() sur stdin fermé
    ├── AttributeError       ← attribut inexistant
    ├── NameError            ← variable non définie
    ├── IndexError           ← index hors limites
    ├── KeyError             ← clé inexistante dans dict
    ├── StopIteration        ← fin d'itérateur
    │
    └── OSError              ← toutes les erreurs système/fichier
        ├── FileNotFoundError    → [Errno 2]
        ├── PermissionError      → [Errno 13]
        ├── IsADirectoryError    → [Errno 21]
        ├── FileExistsError      → [Errno 17]
        └── BlockingIOError      → [Errno 11]
```

**Points clés :**
- `KeyboardInterrupt` et `SystemExit` héritent directement de `BaseException`, **pas** d'`Exception`. C'est **intentionnel** : les développeurs Python ont voulu que Ctrl+C et `sys.exit()` ne soient pas silencieusement avalés par un `except Exception` générique.
- `OSError` est le parent commun de toutes les erreurs fichier. `except OSError` attrape donc `FileNotFoundError`, `PermissionError`, `IsADirectoryError`, etc.
- `except Exception` attrape tout sauf `KeyboardInterrupt`, `SystemExit`, `GeneratorExit`.

### `raise` — lever une exception manuellement

```python
raise ValueError("message d'erreur")
```

`raise` interrompt le flux normal et déclenche une exception. Python remonte les blocs `try` imbriqués du **plus proche au plus lointain**, en cherchant un `except` qui correspond.

```python
try:                              # TRY EXTERNE
    try:                          # TRY INTERNE
        raise ValueError("oups")  # levée dans TRY INTERNE
    except ValueError as e:       # ← attrapé ici en premier
        print("interne:", e)
except ValueError as e:           # ← jamais atteint
    print("externe:", e)
```

Si aucun `except` ne correspond → **crash** avec traceback.

### `str(e)` — récupérer le message d'erreur

`e` dans `except Exception as e` est l'objet exception. `str(e)` donne son message lisible :

```python
except Exception as e:
    print(str(e))
    # "[Errno 2] No such file or directory: 'foo'"
```

C'est exactement ce format que le sujet attend dans les sorties — d'où l'importance d'afficher `e` directement sans reformuler.

### `EOFError` — quand stdin est fermé

`input()` attend une entrée de l'utilisateur. Si stdin est fermé (ex: `< /dev/null` ou pipe fermé), il n'y a rien à lire → `input()` lève `EOFError`.

```bash
python3 script.py file.txt < /dev/null
# → EOFError: EOF when reading a line
```

Sans gestion → crash. D'où le `except (KeyboardInterrupt, EOFError)` dans l'ex1.

`sys.stdin.readline()` (ex2) ne lève **pas** `EOFError` — il retourne `""` silencieusement. Comportement différent, gestion différente.

---

## 4. Le `with` statement — context manager

### Le problème sans `with`

```python
f = open("file.txt", "r")
text = f.read()           # si ça lève une exception...
f.close()                 # ...cette ligne n'est jamais exécutée → fuite !
```

Pour corriger sans `with` :

```python
f = open("file.txt", "r")
try:
    text = f.read()
finally:
    f.close()   # toujours exécuté, même en cas d'exception
```

### `with` — la solution propre

```python
with open("file.txt", "r") as f:
    text = f.read()
# ici : f.close() est appelé automatiquement, même si une exception s'est produite
```

`with` est **exactement équivalent** au `try/finally` ci-dessus, mais en plus lisible et sans risque d'oublier le `close()`.

### Comment fonctionne `with` techniquement

`with` fonctionne avec n'importe quel objet qui implémente le protocole **context manager**, c'est-à-dire deux méthodes spéciales :

**`__enter__(self)`** : appelée à l'entrée du bloc `with`. La valeur retournée est assignée à la variable après `as`.

**`__exit__(self, exc_type, exc_val, exc_tb)`** : appelée à la sortie du bloc `with`, **qu'il y ait eu une exception ou non**. Si une exception s'est produite, les trois paramètres la décrivent. Si `__exit__` retourne `True`, l'exception est supprimée ; sinon elle se propage.

Pour `open()`, `__exit__` appelle `.close()` — c'est tout.

```python
# Ce que fait Python quand il voit "with open(...) as f:"
f = open("file.txt", "r").__enter__()
try:
    text = f.read()
finally:
    f.__exit__(...)   # appelle f.close()
```

### Pourquoi le sujet l'interdit avant l'ex3

Pour s'assurer que tu comprends d'abord la gestion manuelle avec `try/finally` et `.close()`. `with` est une abstraction qui cache ce mécanisme — il faut le comprendre avant de l'utiliser.

---

## 5. Les trois flux (streams) — Exercice 2

### Concept fondamental

Tout programme Unix communique avec le monde extérieur via trois canaux standards, ouverts automatiquement au démarrage :

| Flux | Numéro | Rôle | Accès Python |
|------|--------|------|-------------|
| **stdin** | 0 | Entrée standard (clavier par défaut) | `sys.stdin` |
| **stdout** | 1 | Sortie standard (terminal par défaut) | `sys.stdout` / `print()` |
| **stderr** | 2 | Sortie d'erreur (terminal par défaut) | `sys.stderr` |

Ces trois flux existent depuis les débuts d'Unix (années 1970) — d'où la référence du sujet à "channels older than the Internet itself".

### Pourquoi séparer stderr de stdout ?

Pour que les erreurs ne se mélangent pas avec la sortie normale. Ça permet de les **rediriger indépendamment** :

```bash
python3 script.py file.txt > sortie.txt 2> erreurs.txt
#                            ^stdout      ^stderr séparé
```

Ou de les ignorer :

```bash
python3 script.py file.txt 2>/dev/null   # supprime les erreurs
```

C'est pour ça que l'ex2 demande d'envoyer les erreurs sur `sys.stderr` — c'est une bonne pratique professionnelle.

### `print()` vs `sys.stdout.write()`

`print()` est une fonction de haut niveau qui fait plusieurs choses :
- Convertit les arguments en `str`.
- Les sépare par `sep` (défaut : `" "`).
- Ajoute `end` à la fin (défaut : `"\n"`).
- Écrit sur `file` (défaut : `sys.stdout`).

```python
print("hello")           # écrit "hello\n" sur stdout
print("a", "b", sep="-") # écrit "a-b\n"
print("x", end="")       # écrit "x" sans \n
print("err", file=sys.stderr)  # redirige vers stderr
```

`sys.stdout.write(s)` est de bas niveau :
- Prend **une seule chaîne**.
- N'ajoute **aucun** `\n`.
- Retourne le nombre de caractères écrits.

```python
sys.stdout.write("hello\n")   # équivalent à print("hello")
sys.stderr.write("[STDERR] erreur\n")  # erreur sur stderr
```

### Pourquoi `flush()` est nécessaire

La sortie est **bufferisée** : Python accumule les données en mémoire avant d'écrire sur le terminal (pour des raisons de performance).

Le buffer est vidé automatiquement quand :
- Il est plein.
- Tu écris un `\n` (en mode ligne).
- Le programme se termine normalement.
- Tu appelles `.flush()` explicitement.

En ex2, tu affiches un prompt **sans `\n`** :

```python
sys.stdout.write("Enter new file name (or empty): ")
sys.stdout.flush()    # force l'affichage immédiat
file_name = sys.stdin.readline().strip()
```

Sans `flush()`, le prompt reste dans le buffer et s'affiche **après** que l'utilisateur ait tapé sa réponse — comportement bizarre et inutilisable.

`print()` n'a pas ce problème car il ajoute un `\n` qui déclenche le vidage automatique.

### `sys.stdin.readline()` vs `input()`

`input(prompt)` fait en interne :
1. Affiche le prompt sur stdout.
2. Lit une ligne depuis stdin.
3. **Retire** le `\n` final.
4. Retourne la chaîne.
5. Lève `EOFError` si stdin est fermé.

`sys.stdin.readline()` :
1. Lit une ligne depuis stdin (incluant le `\n` final).
2. Retourne `""` si stdin est fermé (pas d'exception).
3. D'où le `.strip()` nécessaire pour retirer le `\n`.

```python
# input() :
name = input("Ton nom: ")     # retire \n automatiquement

# readline() :
sys.stdout.write("Ton nom: ")
sys.stdout.flush()
name = sys.stdin.readline().strip()   # .strip() retire le \n
```

### `sys.argv`

Liste des arguments de la ligne de commande, toujours de type `str` :

```bash
python3 script.py fichier.txt
# sys.argv = ["script.py", "fichier.txt"]
# sys.argv[0] = "script.py"  (nom du script)
# sys.argv[1] = "fichier.txt" (premier argument)
# len(sys.argv) = 2
```

On vérifie `len(sys.argv) != 2` pour s'assurer qu'il y a exactement **un** argument (le nom du fichier). Ni zéro, ni deux.

---

## 6. Le `tuple` — exercice 3

### Qu'est-ce qu'un tuple ?

Un tuple est une collection **ordonnée** et **immuable** de valeurs. Immuable = on ne peut pas le modifier après création.

```python
t = (True, "contenu du fichier")
print(t[0])   # True
print(t[1])   # "contenu du fichier"
```

### Pourquoi retourner un tuple ici ?

Python ne permet qu'**une seule valeur de retour** par fonction. Le tuple permet d'en retourner plusieurs "en une" :

```python
def secure_archive(...) -> tuple[bool, str]:
    # succès
    return (True, contenu)
    # ou échec
    return (False, message_erreur)
```

L'appelant peut alors décomposer :

```python
result = secure_archive("file.txt", "r")
success = result[0]   # bool
content = result[1]   # str
```

Ou directement :

```python
success, content = secure_archive("file.txt", "r")
```

### `tuple[bool, str]` — type hint

La notation `tuple[bool, str]` (disponible depuis Python 3.9) indique que le tuple contient exactement deux éléments : un `bool` et un `str`. Vérifié par `mypy`.

---

## 7. Type hints et mypy

### Pourquoi les type hints ?

Python est dynamiquement typé — une variable peut changer de type. Les type hints ajoutent des **annotations** qui documentent les types attendus et permettent à des outils comme `mypy` de vérifier la cohérence **sans exécuter le code**.

```python
def secure_archive(file: str, mode: str = "r",
                   content: str = "") -> tuple[bool, str]:
```

- `file: str` → le paramètre `file` doit être un `str`.
- `mode: str = "r"` → paramètre optionnel, défaut `"r"`.
- `-> tuple[bool, str]` → la fonction retourne un tuple de bool et str.

### `mypy` — vérification statique

```bash
mypy ft_vault_security.py
```

`mypy` analyse le code sans l'exécuter et signale les incohérences de types. Si une fonction annotée `-> str` retourne un `int` quelque part → mypy le signale.

---

## 8. flake8 — le linter

**flake8** vérifie le style du code selon PEP 8 (la convention de style Python) :

- Longueur de ligne ≤ 79 caractères.
- 4 espaces d'indentation (pas de tabs).
- Espaces autour des opérateurs.
- Lignes vides entre les fonctions.
- Imports en haut du fichier.
- Pas d'espaces en fin de ligne.

```bash
flake8 ft_ancient_text.py   # vérifie un fichier
flake8 ex0/                 # vérifie un dossier
```

Si flake8 retourne sans rien afficher → le code est conforme.

---

## 9. Résumé par exercice — ce que chaque ex démontre

### Ex0 — ft_ancient_text.py
**Concept central :** opérations basiques sur les fichiers.

- `sys.argv` pour lire l'argument de la ligne de commande.
- `open()` en mode `"r"` retourne un objet fichier (`TextIOWrapper`).
- `.read()` lit tout le contenu.
- `.close()` ferme et flush.
- `except Exception` attrape toutes les erreurs I/O (FileNotFoundError, PermissionError...).
- `KeyboardInterrupt` géré séparément car il n'hérite pas d'`Exception`.

### Ex1 — ft_archive_creation.py
**Concept central :** lecture + transformation + écriture.

- Réutilise ex0 pour la lecture.
- `str.split("\n")` découpe en lignes.
- List comprehension pour ajouter `#` à chaque ligne.
- `"\n".join(lines)` recompose en texte.
- `open(file, "w")` crée ou écrase le fichier.
- `.write()` écrit le contenu.
- `input()` lit l'entrée utilisateur → `EOFError` possible → géré.

### Ex2 — ft_stream_management.py
**Concept central :** les trois flux standards.

- Erreurs sur `sys.stderr.write()` avec préfixe `[STDERR]`.
- Input via `sys.stdin.readline()` + `.strip()` (pas d'`input()`).
- `sys.stdout.write()` + `sys.stdout.flush()` pour le prompt.
- `readline()` retourne `""` sur EOF → pas d'`EOFError` à gérer.

### Ex3 — ft_vault_security.py
**Concept central :** `with` statement + fonction réutilisable.

- `with open(...) as f:` → fermeture automatique garantie.
- Fonction `secure_archive()` avec type hints complets.
- Retourne `tuple[bool, str]` → pattern résultat/erreur.
- `except Exception as e: return (False, str(e))` → jamais de crash, toujours un retour propre.

---

## 10. Ce que le sujet dit explicitement sur la défense

> *"During evaluation, you may be asked to explain file operations, demonstrate error handling, or show how the with statement works. Make sure you understand the concepts behind each exercise."*

Les trois axes garantis :

**File operations** → savoir expliquer `open()`, les modes, `.read()`, `.write()`, `.close()`, le buffer, les descripteurs de fichier, et ce que retourne `open()` (objet fichier, pas le contenu).

**Error handling** → savoir expliquer `try/except/else/finally`, la hiérarchie des exceptions, pourquoi l'ordre des `except` compte, `raise`, `str(e)`, `EOFError`, `KeyboardInterrupt`.

**The `with` statement** → savoir expliquer le context manager, `__enter__`/`__exit__`, l'équivalent `try/finally`, et pourquoi c'est mieux que le close manuel.
