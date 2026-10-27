# Le labo Matplotlib

## Nouveau parcours Superstore

Le cours refait selon [SKILL.md](SKILL.md) est dans le dossier autonome [cours-superstore](cours-superstore/README.md). Ouvrir son [accueil](cours-superstore/index.html), son [TP en binômes](cours-superstore/supports/tp_binomes.html) ou consulter la [validation et ses limites](cours-superstore/VALIDATION.md). Il utilise le vrai classeur `Orders`, conserve la charte TABLEAU et sépare les notebooks apprenants des corrections formateur.

## Version précédente — CSV de commandes

Ouvrir **[le parcours](docs/index.html)**. Les feuilles de style de TABLEAU sont conservées à l'identique. Les supports HTML fonctionnent sans serveur et sans téléchargement distant.

Le cours s'adresse à un public connaissant les bases de Python et les premiers tracés. Chaque séquence suit **exemple → petit exercice → correction collective**, puis un **QCM avec feedback en fin de bloc**. Aucune durée pédagogique n'est affichée : le formateur gère le rythme.

- [Bloc 1 — Comprendre et construire ses graphiques](docs/supports/01_graphiques_fiables.html) : rappel des outils, galerie de graphiques, chargement, agrégation, Figure / Axes, lisibilité, parts du total et démonstration Seaborn.
- [Bloc 2 — Représenter les indicateurs](docs/supports/02_indicateurs.html) : variation, évolution depuis janvier, cumul, moyenne mobile, marge sur CA et synthèse. Power BI reste une passerelle facultative.
- [Sandbox apprenant](docs/data/sandbox-notebook.zip) : deux carnets, données, galerie et environnement Jupyter avec PostgreSQL ; aucun corrigé ni travail personnel.
- [QCM du bloc 1](docs/qcm/01_graphiques_fiables.html) et [QCM du bloc 2](docs/qcm/02_indicateurs.html) : huit questions chacun, avec six flashcards.
- [Correction collective du bloc 1](docs/supports/correction_01.html) et [du bloc 2](docs/supports/correction_02.html).
- [Audit pédagogique](AUDIT_PEDAGOGIQUE.md) et [vérifications](validation/VALIDATION.md).

Les données du bloc 1 sont celles du TP Tableau : 60 lignes de vente, 30 commandes, 45 831 €. Le tableau mensuel du bloc 2 est un **scénario indépendant**, avec profit fictif ; ce n'est pas l'agrégation du premier fichier.

## Dans la sandbox

Lire [les instructions](sandbox-notebook/README.md). Seaborn est inclus : reconstruire l'image avec `docker compose up --build -d` si elle existait avant cette version.

- `00_test_postgres.ipynb` : test court `SELECT 1`, directement dans le notebook.
- `01_comprendre_graphiques.ipynb` : carnet du bloc 1.
- `02_indicateurs.ipynb` : carnet du bloc 2.

Faire des copies à son nom. Les notebooks corrigés sont conservés localement dans `sandbox-notebook/corrections/`, ignorés par Git et exclus de l'archive apprenant. Les corrections HTML restent consultables après les exercices.

## Sources et régénération

- `scripts/contenu_cours.py` : exemples, exercices, solutions et questions.
- `scripts/construire_cours.py` : supports HTML et carnets modèles. Il ne modifie pas `00_test_postgres.ipynb` ni les copies personnelles, mais **remplace les carnets modèles portant les noms ci-dessus**.
- `scripts/valider.py` : exécution isolée des quatre carnets, calculs indépendants, génération des figures et contrôles de liens.
- `scripts/empaqueter.py` : archive apprenant par liste blanche.

```bash
python scripts/construire_cours.py
python scripts/valider.py
python scripts/empaqueter.py
```

La validation utilise les dépendances de `sandbox-notebook/requirements.txt`. Hors Docker, elle redirige les chemins `/workspace` vers une copie temporaire et conserve les travaux apprenants. Le test PostgreSQL, qui exige un serveur réel, reste séparé.
