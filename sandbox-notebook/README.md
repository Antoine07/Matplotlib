# Sandbox-notebook — Matplotlib, bloc 01

Ouvrir `notebooks/01_graphiques_fiables.ipynb`. Le cours est dans le dossier `docs` du kit complet ; le notebook contient les consignes nécessaires pour travailler seul.

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
