# PO Translator

Un petit utilitaire Python permettant de traduire automatiquement les fichiers `django.po` d'un projet Django à l'aide de l'API DeepL.

Le programme traduit les `msgid` en français vers :

* 🇪🇸 Espagnol (`es`)
* 🇵🇹 Portugais (`pt`)

et remplit automatiquement les `msgstr` vides sans modifier les `msgid`.

---

# Fonctionnalités

* Traduction automatique des fichiers `.po`
* Modification directe du fichier (`in-place`)
* Conservation des `msgid`
* Conservation de la structure du fichier `.po`
* Protection des variables Django/Python :

  * `%(name)s`
  * `%s`
* Gestion des chaînes multi-lignes
* Ignore les entrées déjà traduites
* Cache mémoire pour éviter les appels API en double
* Compatible avec tous les projets Django utilisant `gettext`

---

# Exemple

Avant :

```po
msgid "Nom complet"
msgstr ""

msgid "Adresse email"
msgstr ""
```

Après (`--lang es`) :

```po
msgid "Nom complet"
msgstr "Nombre completo"

msgid "Adresse email"
msgstr "Dirección de correo electrónico"
```

---

# Variables protégées

Le programme protège automatiquement les variables de traduction.

Avant :

```po
msgid "La taille de l'image ne peut pas dépasser %(max_size_kb)s ko."
msgstr ""
```

Après :

```po
msgid "La taille de l'image ne peut pas dépasser %(max_size_kb)s ko."
msgstr "El tamaño de la imagen no puede superar %(max_size_kb)s KB."
```

La variable `%(max_size_kb)s` est conservée intacte.

---

# Chaînes multi-lignes

Le programme gère également les textes sur plusieurs lignes.

Exemple :

```po
msgid ""
"Votre compte non activé sera supprimé dans 3 jours. "
"Activez-le si vous voulez le garder !"
msgstr ""
```

Après traduction :

```po
msgstr "Su cuenta no activada será eliminada en 3 días. ¡Actívela si desea conservarla!"
```

---

# Installation

## 1. Cloner le projet

```bash
git clone https://github.com/votre-utilisateur/po-translator.git
cd po-translator
```

---

## 2. Créer un environnement virtuel

Windows :

```bash
py -m venv .venv
```

Linux / macOS :

```bash
python3 -m venv .venv
```

---

## 3. Activer l'environnement virtuel

Windows :

```bash
.venv\Scripts\activate
```

Linux / macOS :

```bash
source .venv/bin/activate
```

---

## 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

# Dépendances

Le fichier `requirements.txt` :

```txt
polib
requests
```

Ou pour générer le fichier :

```bash
pip freeze > requirements.txt
```

---

# Obtenir une clé API DeepL

Créer un compte :

https://www.deepl.com/pro-api

Choisir le plan :

* DeepL API Free
* DeepL API Pro

Une clé ressemble à :

```text
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx:fx
```

Le suffixe `:fx` indique une clé API gratuite.

---

# Configuration

## Méthode recommandée : variables d'environnement

Créer un fichier `.env` :

```env
DEEPL_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Installer :

```bash
pip install python-dotenv
```

Puis :

```python
from dotenv import load_dotenv
import os

load_dotenv()

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
```

---

## Méthode simple

Modifier directement :

```python
DEEPL_API_KEY = "YOUR_API_KEY"
```

⚠️ Ne jamais publier votre clé API sur GitHub.

---

# Utilisation

Le script recherche par défaut un fichier :

```text
django.po
```

dans le dossier courant.

---

## Traduire en espagnol

```bash
py po_translator.py --lang es
```

---

## Traduire en portugais

```bash
py po_translator.py --lang pt
```

---

## Traduire un autre fichier

```bash
py po_translator.py --lang es --file locale/es/LC_MESSAGES/django.po
```

---

# Fonctionnement

Le programme :

1. Ouvre le fichier `.po`
2. Parcourt toutes les entrées
3. Ignore les `msgstr` déjà remplis
4. Traduit les `msgid`
5. Écrit les traductions dans `msgstr`
6. Sauvegarde le fichier

---

# Ce qui est modifié

Uniquement :

```po
msgstr ""
```

devient :

```po
msgstr "Traduction"
```

---

# Ce qui n'est jamais modifié

* `msgid`
* commentaires
* références de fichiers
* numéros de ligne
* variables Django/Python
* structure logique du fichier

---

# Sauvegarde recommandée

Avant chaque exécution :

Windows :

```bash
copy django.po django.po.bak
```

Linux :

```bash
cp django.po django.po.bak
```

---

# Workflow Django recommandé

Extraire les traductions :

```bash
django-admin makemessages -l es
```

ou

```bash
django-admin makemessages -l pt
```

Traduire :

```bash
py po_translator.py --lang es
```

Compiler :

```bash
django-admin compilemessages
```

---

# Exemple complet

```bash
django-admin makemessages -l es

py po_translator.py --lang es

django-admin compilemessages
```

---

# Limitations actuelles

Le programme ne gère pas encore :

* `msgid_plural`
* les traductions par batch DeepL
* la reprise automatique après interruption
* les logs dans un fichier
* le cache persistant sur disque

---

# Améliorations futures possibles

* Traduction par lots (batch)
* Reprise automatique
* Support de `msgid_plural`
* Interface graphique
* Publication sur PyPI
* Support d'autres APIs de traduction
* Cache SQLite

---

# Licence

MIT License.

Vous êtes libre d'utiliser, modifier et distribuer ce projet.
