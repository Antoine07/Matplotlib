# Validation — deux blocs Matplotlib

## Contrôles effectués

- Les feuilles `site.css` et `tableau.css` et le CSV de commandes sont identiques aux sources TABLEAU.
- Calculs indépendants avec `csv` et `Decimal` : 60 lignes, 30 commandes, 45 831 € ; totaux par catégorie et région.
- Scénario mensuel contrôlé indépendamment : 80 500 € de ventes, 18 350 € de profit ; six variations, évolutions, cumuls et taux vérifiés ; quatre moyennes mobiles complètes.
- Ratio global : environ 22,80 % ; moyenne des taux mensuels : 22,50 %.
- Deux carnets apprenants et deux corrigés conformes à nbformat, exécutés cellule par cellule dans un espace neuf par carnet. Les chemins `/workspace` sont redirigés vers une copie temporaire des données et exports ; les autres instructions sont exécutées telles quelles.
- Les démonstrations Seaborn sont exécutées avec Seaborn 0.13.2. Aucun remplacement par une figure Matplotlib simulant Seaborn.
- Les images attendues sont produites et copiées dans les supports ; une inspection visuelle a confirmé la lisibilité de l'histogramme, des variations, du lissage et de la marge cumulée.
- Les cellules apprenants à compléter restent volontairement ouvertes : leur exécution sans erreur ne signifie pas qu'un exercice est réussi.
- Tous les extraits Python des HTML compilent ; les liens et ancres locales sont vérifiés.
- Aucune durée pédagogique dans les pages HTML. Les fenêtres de trois mois restent présentes car elles définissent un indicateur.
- Les deux QCM ont été testés avec jsdom : navigation des flashcards, réponse obligatoire, feedback correct et incorrect sur les huit questions, verrouillage, remise à zéro, scores 8/8 et 0/8.
- L'archive utilise une liste blanche : deux carnets de cours, test PostgreSQL, galerie, données et configuration. Aucun corrigé, `.env`, fichier de corbeille ou notebook personnel.
- Le test PostgreSQL court et les notebooks personnels existants n'ont pas été modifiés par la refonte.

## Environnement et limites

Python 3.13.3, Matplotlib 3.10.8, pandas 3.0.1, NumPy 2.4.0, Seaborn 0.13.2. Seaborn a été chargé depuis une copie temporaire de son package Python déjà présent sur la machine ; aucun environnement existant n'a été modifié.

L'exécution utilise le backend Agg et des espaces Python neufs, pas des noyaux Jupyter pilotés par le navigateur. Les chiffres et fichiers exportés sont validés ; le lancement du serveur Jupyter Docker n'a pas été vérifié dans cette session. Il faut reconstruire l'image pour disposer de Seaborn.

Le rendu complet desktop/mobile n'a pas pu être validé en navigateur dans cette session. Le thème de référence est conservé ; les interactions sont testées avec jsdom, qui ne contrôle pas le rendu visuel. Les figures ont été inspectées séparément.

Le test PostgreSQL reste un test réel à lancer depuis la sandbox ; il ne fait pas partie de la validation hors ligne des cours.

## Rejouer

Avec les dépendances de la sandbox :

```bash
python scripts/construire_cours.py
python scripts/valider.py
python scripts/empaqueter.py
```

Pour les interactions, avec Node et jsdom :

```bash
node scripts/verifier_interactions.cjs
```

`JSDOM_PATH` permet d'indiquer une installation existante. Le détail de l'exécution et des chiffres est dans `bilan.json` ; les traces sont nommées d'après les quatre notebooks.
