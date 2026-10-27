# Sandbox-notebook — Matplotlib, bloc 01

Ouvrir `notebooks/00_test_postgres.ipynb` pour vérifier PostgreSQL, puis `notebooks/01_graphiques_fiables.ipynb` pour le cours Matplotlib. Le cours est dans le dossier `docs` du kit complet ; le notebook contient les consignes nécessaires pour travailler seul.

## Avec une sandbox Jupyter existante

Importer ensemble `notebooks/`, `data/` et `resultats/`, puis choisir un noyau Python disposant de pandas et Matplotlib. Le notebook accepte un lancement depuis la racine de la sandbox ou depuis son dossier `notebooks`. Les versions de référence sont fixées dans `requirements.txt`.

## Avec Docker

Docker Desktop doit être démarré. Depuis ce dossier :

```bash
docker compose up --build -d
docker compose logs notebook
```

Ouvrir **http://localhost:8890/lab**, puis saisir le jeton affiché dans les logs (la ligne de logs peut annoncer le port interne 8888 ; utiliser 8890 dans le navigateur). Ouvrir le notebook dans le dossier `notebooks`.

Le premier build nécessite Internet. Les données sont ensuite disponibles hors ligne. L'accès est limité au poste local et utilise le jeton Jupyter généré au démarrage. Les notebooks et exports restent dans les dossiers montés.

## PostgreSQL et test de connexion

Le Compose démarre aussi PostgreSQL 17, dans un service séparé. Jupyter attend que son contrôle de disponibilité réussisse. La base conserve ses données dans le volume `postgres_data`, y compris après `docker compose down`.

Depuis Jupyter, ouvrez **`notebooks/00_test_postgres.ipynb`**, puis exécutez sa cellule. Vous pouvez également tester depuis votre terminal :

```bash
docker compose exec -T notebook python scripts/test_postgres.py
```

Résultat attendu : **Connexion PostgreSQL OK**, base `formation`, utilisateur `apprenant`, résultat SQL `1 + 1 = 2`, puis version du serveur. Le test ouvre réellement une connexion avec Psycopg et vérifie la réponse SQL ; il ne modifie aucune table et retourne une erreur en cas d'échec.

Les variables `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER` et `PGPASSWORD` sont déjà transmises à Jupyter. Le serveur est **`postgres:5432` à l'intérieur de Docker**, pas `localhost`. Aucun port PostgreSQL n'est publié sur la machine hôte. Le test est prévu dans le Jupyter Docker ; un Jupyter externe nécessite sa propre connexion PostgreSQL.

Les valeurs pédagogiques par défaut sont base `formation`, utilisateur `apprenant`, mot de passe `formation_locale`. Pour les personnaliser **avant la première initialisation**, copier `.env.example` en `.env` et modifier les valeurs. Le fichier `.env` est ignoré par Git et exclu de l'archive.

En cas d'échec : `docker compose ps` doit afficher PostgreSQL `healthy` ; consulter `docker compose logs postgres`. Si `psycopg` manque, relancer `docker compose up --build -d`. Changer `.env` après initialisation ne change pas les identifiants déjà enregistrés dans la base : conserver les identifiants initiaux ou modifier l'utilisateur en SQL. `docker compose down` conserve la base ; l'option `-v` supprimerait ses données.

Les données commerciales restent dans le CSV pour le bloc Matplotlib ; le test ne les importe pas dans PostgreSQL.

## Arrêt et reprise

```bash
docker compose down
# Reprendre :
docker compose up -d
```

Si le port est occupé, créer un fichier `.env` avec `JUPYTER_PORT=8891`, relancer et ouvrir http://localhost:8891/lab. Sur Linux, si l'UID 1000 ne peut pas écrire dans les dossiers, adapter l'utilisateur du service à l'UID/GID du poste dans une surcharge Compose et définir `HOME: /tmp`.

## Sans Docker, avec Python 3.13

Créer un environnement dédié, l'activer, puis installer les dépendances :

```bash
python -m venv .venv
# macOS / Linux :
source .venv/bin/activate
# Windows PowerShell (à la place de la ligne précédente) :
# .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m jupyter lab --port=8890
```

## Travailler et rendre

1. Faire une copie du notebook à son nom.
2. Lire les démonstrations, prédire, puis exécuter avec Maj + Entrée.
3. Compléter les quatre exercices et les cellules Markdown.
4. Garder les quatre PNG dans `resultats`.
5. Redémarrer le noyau puis tout exécuter avant de rendre.

Une cellule « À vous » vide n'est pas une réponse, même si son exécution ne produit aucune erreur.

Les corrigés sont séparés dans le kit formateur et ne sont pas montés par la configuration Docker apprenant. Pour le formateur : copier le notebook corrigé dans son propre dossier `notebooks` pour l'exécuter via cette configuration, ou l'ouvrir avec un Jupyter local depuis la racine de la sandbox. L'archive apprenant ne contient pas les corrigés ; les solutions HTML du cours restent accessibles pour l'autoformation.

## Références PostgreSQL

- [Image officielle PostgreSQL](https://hub.docker.com/_/postgres)
- [Ordre de démarrage et contrôles de disponibilité Compose](https://docs.docker.com/compose/how-tos/startup-order/)
- [Installation de Psycopg](https://www.psycopg.org/psycopg3/docs/basic/install.html)
