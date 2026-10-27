# Le labo Matplotlib — premier bloc

Ouvrir **[docs/index.html](docs/index.html)** dans un navigateur. Le cours fonctionne en fichiers locaux, sans serveur ni dépendance distante. Le graphisme reprend à l'identique les feuilles `site.css` et `tableau.css` du cours voisin `TABLEAU` : couleurs, typographie, cartes, sommaire, exercices et révision.

**Public :** personnes connaissant déjà les premiers tracés Matplotlib et les bases de Python. **Durée :** 2 h 30 hors pause. **Fil rouge :** le carnet visuel d'une boutique ; mêmes données que le TP Tableau (60 lignes de vente / 30 commandes).

- [Cours du bloc 01](docs/supports/01_graphiques_fiables.html) : Figure / Axes, préparation des données, barres triées, lisibilité, export et interprétation.
- [Sandbox à distribuer](docs/data/sandbox-notebook.zip) : notebook apprenant, CSV et environnement Jupyter ; sans corrigé.
- PostgreSQL 17 dans la sandbox, avec volume persistant et test dans `notebooks/00_test_postgres.ipynb` (ou `docker compose exec -T notebook python scripts/test_postgres.py` depuis la sandbox).
- [Flashcards et QCM](docs/qcm/01_graphiques_fiables.html) : six cartes et huit questions avec feedback.
- [Correction expliquée](docs/supports/correction_01.html) et notebook dans `sandbox-notebook/corrections/`.
- [Guide formateur et reprise](GUIDE_FORMATEUR.md).
- [Vérifications effectuées](validation/VALIDATION.md).

Le cours se lit dans le navigateur ; les exercices s'exécutent dans une sandbox-notebook existante ou dans le Jupyter Docker fourni. Voir [les instructions de lancement](sandbox-notebook/README.md).

## Continuer demain

Le bloc 01 est utilisable. Les blocs 02 (dates et périmètres) et 03 (vues multiples) sont seulement des jalons prévus, pas des chapitres déjà rédigés. Conserver le même fil rouge et la même présentation. Voir `GUIDE_FORMATEUR.md` pour les choix et les suites proposées.

## Sources et régénération

`scripts/construire_cours.py` est la source du cours HTML, des exercices, du QCM et des notebooks. Le relancer **remplace ces fichiers générés**, y compris les notebooks d'origine : travailler dans des copies à son nom.

Le notebook `00_test_postgres.ipynb` est maintenu séparément et appelle `sandbox-notebook/scripts/test_postgres.py`. Son test nécessite PostgreSQL démarré ; il ne fait pas partie de la validation hors ligne du cours.

```bash
python scripts/construire_cours.py
python scripts/valider.py
python scripts/empaqueter.py
```

La validation nécessite les dépendances de `sandbox-notebook/requirements.txt`. Elle exécute les cellules dans des espaces de variables neufs, contrôle les calculs indépendamment avec `csv` et `Decimal`, produit les figures de référence et vérifie les liens. Les rendus d'apprenants dans `sandbox-notebook/resultats` ne sont pas modifiés.
