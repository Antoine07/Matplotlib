# Sandbox-notebook — Matplotlib et indicateurs

Ouvrir `notebooks/00_test_postgres.ipynb` pour vérifier PostgreSQL, puis `notebooks/01_comprendre_graphiques.ipynb` et `notebooks/02_indicateurs.ipynb` pour les deux blocs. Le cours est dans le dossier `docs` du kit complet ; le notebook contient les consignes nécessaires pour travailler seul.


## Cours Superstore

Le parcours [cours-superstore](../docs/index.html) utilise la feuille `Orders` du classeur `data/sample_-_superstore.xls`. Depuis la racine du dépôt, reconstruire puis lancer cette sandbox ; les nouveaux carnets étudiants apparaissent dans `notebooks/00_demarrage.ipynb` et `notebooks/01_exploration.ipynb` à `06_boxplots_avance.ipynb`, ainsi que `notebooks/tp_binomes.ipynb`. Le classeur est monté en lecture seule. Le générateur du cours synchronise ces carnets, jamais les corrigés formateur.

Le chargement du `.xls` nécessite `xlrd`; il est ajouté à `requirements.txt`. Reconstruisez l’image après cette modification. Les exercices du cours utilisent pandas et Matplotlib ; ils ne se connectent pas à PostgreSQL.

## Avec une sandbox Jupyter existante

Importer ensemble `notebooks/`, `data/` et `resultats/`, puis choisir un noyau Python disposant de pandas, Matplotlib et Seaborn. Les exemples utilisent les chemins Docker `/workspace/data` et `/workspace/resultats` : dans un autre environnement, adapter ces chemins et créer le dossier des exports avant de lancer les figures. Les versions de référence sont fixées dans `requirements.txt`.

## Avec Docker

Docker Desktop doit être démarré. Depuis ce dossier :

```bash
docker compose up --build -d
docker compose logs notebook
```

Ouvrir **http://localhost:8890/lab**, puis saisir le jeton affiché dans les logs (la ligne de logs peut annoncer le port interne 8888 ; utiliser 8890 dans le navigateur). Ouvrir le notebook dans le dossier `notebooks`.

Si une ancienne image existe, la reconstruire pour installer Seaborn. Le premier build nécessite Internet. Les données sont ensuite disponibles hors ligne. L'accès est limité au poste local et utilise le jeton Jupyter généré au démarrage. Les notebooks et exports restent dans les dossiers montés.

## PostgreSQL et test de connexion

Le Compose démarre aussi PostgreSQL 17, dans un service séparé. Jupyter attend que son contrôle de disponibilité réussisse. La base conserve ses données dans le volume `postgres_data`, y compris après `docker compose down`.

Ouvrez **`notebooks/00_test_postgres.ipynb`** et exécutez la cellule. Elle lance `SELECT 1` et affiche **Connexion PostgreSQL OK** si la requête réussit.

Docker transmet les identifiants via les variables `PG*`. Le serveur est `postgres:5432` dans Docker. Les valeurs par défaut (`formation`, `apprenant`, `formation_locale`) peuvent être personnalisées avec `.env.example`, à copier en `.env` avant le premier démarrage.

En cas d'échec, vérifiez `docker compose ps` et `docker compose logs postgres`. Si `psycopg` manque, relancez `docker compose up --build -d`. Modifier `.env` ne change pas les identifiants d'une base déjà initialisée.

Le bloc 1 utilise le CSV ; le bloc 2 utilise un tableau mensuel fictif construit dans le notebook, également fourni en CSV. Un Jupyter hors Docker nécessite sa propre configuration PostgreSQL.

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
3. Après chaque exemple, faire le petit exercice, puis noter la correction collective dans la cellule prévue.
4. Garder les PNG dans `resultats` et faire le QCM avec feedback sur le support HTML en fin de bloc.
5. Redémarrer le noyau puis tout exécuter avant de rendre.

Une cellule « À vous » vide n'est pas une réponse, même si son exécution ne produit aucune erreur.

Les corrigés sont séparés dans le kit formateur et ne sont pas montés par la configuration Docker apprenant. Pour le formateur : copier le notebook corrigé dans son propre dossier `notebooks` pour l'exécuter via cette configuration, ou l'ouvrir avec un Jupyter local depuis la racine de la sandbox. L'archive apprenant ne contient pas les corrigés ; les solutions HTML du cours restent accessibles pour l'autoformation.

## Références PostgreSQL

- [Image officielle PostgreSQL](https://hub.docker.com/_/postgres)
- [Ordre de démarrage et contrôles de disponibilité Compose](https://docs.docker.com/compose/how-tos/startup-order/)
- [Installation de Psycopg](https://www.psycopg.org/psycopg3/docs/basic/install.html)
