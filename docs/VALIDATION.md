# Vérifications du parcours Superstore

## Classeur source

Le fichier copié dans `data/sample_-_superstore.xls` a été lu depuis la feuille `Orders` avec R `readxl` après vérification que l’environnement Python ne disposait pas de `xlrd`. La feuille contient 10 194 lignes et 21 colonnes ; les 9 colonnes exigées par le parcours sont présentes, sans valeur manquante. Le fichier contient 5 111 `Order ID` distincts, 4 régions et 3 catégories, du 3 janvier 2023 au 30 décembre 2026.

Agrégats vérifiés sur le classeur : Sales total = 2 326 534,35 ; Profit total = 292 296,81. Sales par catégorie : Furniture = 754 747,76 ; Office Supplies = 731 893,31 ; Technology = 839 893,28. Sales par région : Central = 503 170,67 ; East = 691 828,17 ; South = 391 721,91 ; West = 739 813,61. La série mensuelle a 48 périodes ; minimum = février 2023, 4 519,89 ; maximum = novembre 2026, 118 454,51. Le graphique du bloc 0 compare aussi les lignes et les commandes distinctes par catégorie : Furniture (2 201 lignes, 1 819 commandes), Office Supplies (6 128, 3 812) et Technology (1 865, 1 560).

## Contrôles automatisés

`python -m unittest discover -s docs/tests -v` : 20 contrôles découverts, dont les tests de fixture de ratios et variations, le jeu du TP Power BI, les chemins HTML locaux, les QCM (4 choix, position variée et réponse correcte préservée), la structure JSON des notebooks, la compilation syntaxique des cellules Python et le nouveau bloc de découverte. Pendant la génération, 17 contrôles ont réussi et 3 tests du classeur `.xls` ont été sautés car `xlrd` n’est pas installé dans l’interpréteur local.

Le classeur est présent dans `requirements.txt` via `xlrd>=2.0.1`. La lecture pandas du `.xls` et l’exécution des carnets depuis un noyau neuf restent à confirmer après installation des dépendances. Une tentative d’exécution locale était bloquée aussi par l’absence de Matplotlib dans l’interpréteur. Les tests n’affirment donc pas que les notebooks ont été exécutés.

## Révision de la progression

Un bloc de présentation est inséré après la réactivation et avant « Explorer les commandes », sans renuméroter les blocs existants. Il montre cinq graphiques différents : barres horizontales, colonnes groupées, courbe, nuage de points et boxplot. Les DataFrames fictifs sont construits directement dans le code affiché ; leurs valeurs servent aussi aux tableaux HTML et aux illustrations SVG. Aucun exercice ni QCM n’est ajouté à ce bloc.

Les cellules de données ont été exécutées avec Pandas. Les interprétations ont été contrôlées : Écran à 2 100 €, progression maximale de Nord de 30 k€, baisses en mars et juin, relation positive budget/ventes, dispersion interquartile maximale dans Nord et valeur atypique à 350 €. Les quartiles utilisés dans le SVG ont été comparés à `DataFrame.quantile()` ; les moustaches utilisent les valeurs observées dans les bornes à 1,5 IQR. Les cinq SVG distincts sont valides XML, et chaque cellule de tracé compile. Matplotlib reste absent localement ; l’installation temporaire a échoué faute d’accès au registre de paquets. Ces contrôles ne constituent pas une exécution des tracés Matplotlib ni une inspection visuelle de la page.

Les 21 exercices sont conservés. Les parts du total sont abordées avant la comparaison de deux contributions ; le comptage mensuel des commandes est déplacé du bloc 01 au bloc 04. Les exercices qui reproduisaient les exemples sont remplacés par des applications à d’autres mesures, regroupements ou périodes. Les corrections HTML et les notebooks formateur sont régénérés depuis ces mêmes consignes.

Les calculs des 21 exemples et exercices ont été exécutés avec Pandas sur un export de la feuille Orders obtenu avec R `readxl`. Les appels de tracé ont été exclus, Matplotlib restant absent de l’interpréteur local. Cette vérification ne constitue pas une exécution graphique des notebooks.

Résultats contrôlés pour les nouveaux exercices :

- Clients distincts par année : 605, 577, 653 et 704 de 2023 à 2026.
- L’écart maximal entre lignes et commandes se trouve dans West : 3 253 − 1 635 = 1 618. L’ancienne correction mentionnait Central à tort.
- Contributions régionales : East et West ont une part du profit supérieure à leur part des ventes, avec des écarts de +2,72 et +6,11 points.
- Ratio profit/ventes maximal par sous-catégorie : Labels, environ 43,90 %.
- Profit total maximal par segment : Consumer ; ratio maximal : Home Office, environ 14,02 %.
- Profits négatifs dans West : Bookcases (−1 608,43) et Machines (−541,71).
- Plus grand écart entre ratio des sommes et moyenne des taux par catégorie : Office Supplies, environ 3,22 points.
- Maximum mensuel de commandes distinctes en 2026 : novembre, 262 commandes.
- Évolution de décembre 2024 par rapport à janvier 2024 : environ +309,13 %.
- Ratio cumulé sur 2024 : environ 13,11 %, contre 12,25 % pour la moyenne des taux mensuels.

## Nouveau jeu du TP Power BI

`data/ventes_reseau_powerbi.csv` contient 2 274 lignes de commande fictives et 1 273 commandes sur les douze mois de 2025. Il est généré de façon déterministe avec la graine 20261027. Son grain, ses dix colonnes, la cohérence des dimensions au sein d’une commande et sa copie dans la sandbox ont été contrôlés. Le chiffre d’affaires total est de 405 188,35 € HT, le coût d’achat de 295 375,00 € HT et la marge commerciale de 109 813,35 € HT.

Le TP est réduit à deux graphiques : chiffre d’affaires mensuel et marge commerciale rapportée au chiffre d’affaires par catégorie. La question facultative est retirée du sujet et de la correction. Le notebook et la page formateur produisent deux figures et deux exemples d’insights. Les calculs ont été exécutés sur le CSV : évolution janvier-décembre de +149,06 %, marge/CA de 59,97 % pour les Accessoires et 20,14 % pour l’Informatique, soit environ 39,82 points d’écart calculés avant arrondi des taux. Les appels Matplotlib restent non exécutés dans l’interpréteur local, où cette dépendance est absente.

Le sujet étudiant présente les données, les deux graphiques et les deux insights attendus. Il ne contient ni durée, ni horaire, ni barème, ni indications de passage à l’oral, ni correction. Les notebooks formateur restent hors de la sandbox.

## QCM et modèle pédagogique réutilisable

Le bouton « Recommencer » est masqué pendant les questions et affiché uniquement après le bilan final. Le moteur JavaScript a été exécuté avec une interface DOM minimale pour les trois questionnaires (16, 15 et 8 questions) : passage séquentiel, verrouillage, feedback, score, apparition finale du bouton et remise à zéro complète ont été vérifiés. Ce contrôle ne remplace pas une inspection visuelle dans un navigateur.

La réactivation contient six questions supplémentaires : trois sur figsize (unité, conversion à 100 DPI et repère de taille pour un graphique détaillé), deux sur les sélections renvoyant une Series ou un DataFrame, et une sur groupby avec deux champs. Les deux sélections et l’agrégation par couple ont été vérifiées sur une mini-table Pandas ; la conversion en pixels a été contrôlée arithmétiquement.

Les choix sont désormais mélangés à la génération avec un indice de correction recalculé. Le texte de la bonne réponse et son explication sont comparés à la banque source pour chaque question ; les quatre choix sont conservés. Le mélange est reproductible et ne produit pas plus de deux bonnes réponses consécutives à la même position. Les tests de score et de remise à zéro ont été réexécutés après ce mélange.

| QCM | A | B | C | D |
| --- | --- | --- | --- | --- |
| Réactivation — 16 questions | 4 | 4 | 4 | 4 |
| Synthèse — 15 questions | 3 | 4 | 4 | 4 |
| Approfondissements — 8 questions | 2 | 2 | 2 | 2 |

L’audit des exercices confirme 21 consignes et 21 corrections distinctes. Aucune correction ne reproduit intégralement le code de son exemple. La vérification pédagogique porte aussi sur le changement de mesure, de regroupement, de périmètre ou de référence ; la réutilisation de méthodes reste volontaire.

Le `SKILL.md` racine décrit désormais le modèle générique. `references/pattern-matplotlib.md` conserve les paramètres de ce projet. Le validateur Python du skill était indisponible faute de PyYAML ; l’en-tête a été analysé avec Ruby YAML, puis le nom, la description et les liens relatifs ont été contrôlés.

## Charte et limites

`assets/site.css` et `assets/tableau.css` sont identiques aux fichiers de référence TABLEAU. Les pages locales, liens et ancres ont été contrôlés. Le rendu n’a pas été inspecté dans un navigateur pendant cette génération ; le démarrage Docker/Jupyter n’a pas été lancé.
