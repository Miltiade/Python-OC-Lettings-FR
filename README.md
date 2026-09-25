## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`

## Déploiement

### Vue d'ensemble

Le site est déployé sur [Render](https://oc-lettings-spwm.onrender.com) à partir d'une
image Docker publiée sur Docker Hub. Le pipeline GitHub Actions (`.github/workflows/`)
automatise la chaîne complète à chaque push sur `master` :

1. **build-test** — flake8 + pytest (couverture > 80 %). Tourne sur toutes les branches.
2. **dockerize** — seulement si build-test réussit ET sur `master` : construit
   l'image, la tague avec le hash court du commit (ex. `smith9567/oc-lettings:f7344a1`)
   et le tag `latest`, puis la pousse sur Docker Hub.
3. **deploy** — seulement si dockerize réussit : appelle le Deploy Hook Render,
   qui relance le service à partir de l'image `latest`.

Les autres branches ne déclenchent que les tests, jamais la conteneurisation
ni le déploiement. Le service Render est alimenté par une image Docker existante
(pas de connexion Git) : il n'y a donc pas d'Auto-Deploy à désactiver — les
déploiements ne peuvent venir QUE du pipeline.

### Configuration requise

- **Secrets GitHub** (Settings → Secrets and variables → Actions) :
  - `DOCKERHUB_USERNAME` — nom d'utilisateur Docker Hub
  - `DOCKERHUB_TOKEN` — access token Docker Hub (droits lecture/écriture)
  - `RENDER_DEPLOY_HOOK_URL` — URL du Deploy Hook du service Render
- **Service Render** (type : image Docker existante `smith9567/oc-lettings:latest`)
  avec ses variables d'environnement :
  - `SECRET_KEY` — clé secrète Django
  - `DEBUG` — `False` en production
  - `ALLOWED_HOSTS` — inclure le domaine Render
  - `SENTRY_DSN` — DSN du projet Sentry
- Aucun secret n'est versionné dans le dépôt (fichier `.env` non commité,
  `.dockerignore` exclut les fichiers locaux de l'image).

### Dérouler un déploiement

1. Modifier le code, committer, pousser sur `master` :
   `git add <fichiers> && git commit -m "<message>" && git push origin master`
2. Vérifier dans l'onglet **Actions** de GitHub que les trois jobs passent au vert
   (build-test → dockerize → deploy).
3. Attendre ~2–3 minutes (relance du service Render), puis vérifier
   https://oc-lettings-spwm.onrender.com (forcer le cache navigateur : Ctrl+F5).

### Relancer le site en local avec Docker (uniquement)

ATTENTION : le fichier `.env` (non versionné) doit contenir les clés : `SECRET_KEY` (requis),
`SENTRY_DSN` (recommandé).

```bash
docker pull smith9567/oc-lettings:latest
docker run -d -p 8000:8000 --env-file .env -e DEBUG=False \
  -e ALLOWED_HOSTS=localhost,127.0.0.1 --name oc-lettings-test smith9567/oc-lettings:latest
