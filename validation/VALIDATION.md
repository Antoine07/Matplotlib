# Vérification du bloc 01 — 27 octobre 2026

## Contrôles réussis

- `site.css` et `tableau.css` sont identiques octet pour octet aux fichiers de TABLEAU.
- Le CSV de la sandbox et celui du support sont identiques à `TABLEAU/docs/data/tp01_commandes_detail.csv`.
- Calcul indépendant avec `csv` et `Decimal` : 60 lignes, 30 commandes, 45 831 € ; chaque montant correspond à quantité × prix × (1 − remise).
- Contrôle des totaux par catégorie, région Sud et produit ; vérification des couples catégorie–longueur effectivement dessinés.
- Le bug pédagogique inverse effectivement les montants de deux catégories tout en conservant le total général.
- Les deux notebooks respectent le format nbformat 4.5. Leurs cellules Python ont été exécutées dans l'ordre, avec un espace de variables neuf et une copie temporaire de la sandbox pour chaque parcours : 8 cellules apprenant, 9 cellules corrigé.
- Les quatre exports du corrigé ont été produits ; le parcours apprenant produit son exemple et conserve les zones à compléter. L'exécution d'une cellule apprenant vide n'est pas comptée comme la réussite de l'exercice.
- Les figures sont disponibles dans `validation/figures/` et les mêmes images illustrent le corrigé HTML. La figure du cours a été inspectée visuellement : titres, unités et étiquettes lisibles.
- Les liens locaux, ressources et ancres HTML ont été contrôlés ; tous les extraits Python du HTML compilent.
- Les flashcards et le QCM ont été exercés avec jsdom : carte suivante/précédente, boucle, absence de réponse, score 8/8, remise à zéro, mauvaise réponse, score 7/8 et feedback.
- La syntaxe des deux scripts JavaScript est valide.
- `docker compose config` valide la configuration : port local 8890 vers 8888, notebooks et résultats persistants, données en lecture seule.
- Archive apprenant contrôlée : neuf fichiers, aucun corrigé ni résultat de travail ; CRC valide.

## Environnement réellement utilisé

Python 3.13.3, Matplotlib 3.10.8, pandas 3.0.1, NumPy 2.4.0, nbformat 5.10.4, nbclient 0.10.4. Les versions directes de `requirements.txt` correspondent aux bibliothèques disponibles. Aucun environnement existant n'a été modifié.

Le détail machine est dans `bilan.json`. Les traces numériques sont dans `notebooks_execution.txt` et `corrections_execution.txt`.

## Limites de la vérification

- Le serveur Docker n'est pas accessible dans cette session (accès au socket refusé). L'image n'a donc pas été construite ni le service Jupyter lancé.
- Le code des notebooks a été exécuté directement cellule par cellule avec le backend Agg, pas via un noyau Jupyter piloté par nbclient. L'affichage interactif dans Jupyter reste à confirmer lors du lancement de la sandbox ; les exports et calculs ont été vérifiés.
- Chromium n'a pas pu démarrer dans le bac à sable système : refus macOS `bootstrap_check_in / MachPortRendezvous`. Pas de capture du cours ni de validation visuelle desktop/mobile en navigateur. Les styles responsives sont ceux du cours TABLEAU ; les interactions ont été vérifiées via jsdom, qui ne contrôle pas le rendu visuel.
- Le premier build Docker et l'installation locale ont besoin d'Internet. Les sources de données et le support HTML fonctionnent ensuite sans téléchargement.

## Rejouer

Depuis un Python disposant des dépendances de la sandbox :

```bash
python scripts/valider.py
python scripts/empaqueter.py
```

Le test d'interactions utilise Node et jsdom :

```bash
node scripts/verifier_interactions.cjs
```

`JSDOM_PATH` peut désigner un module jsdom installé ailleurs. Node 24.12.0 a été utilisé pour ce contrôle. La validation ne modifie pas les travaux apprenants.
