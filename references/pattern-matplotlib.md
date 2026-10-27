# Réalisation de référence : Matplotlib et préparation à Power BI

Lire cette référence pour modifier ce projet ou reprendre ses choix concrets dans un autre cours. Adapter les données, le vocabulaire et le découpage au nouveau contexte.

## Sources du projet

À partir de la racine du dépôt :
- `docs/scripts/construire.py` génère les pages HTML, les QCM, les styles complémentaires et les notebooks formateur.
- `docs/scripts/lesson_content.py` définit les séquences effectivement affichées et leurs exercices ; elles remplacent certaines définitions historiques présentes dans le générateur.
- `docs/scripts/discovery_content.py` définit la présentation de cinq graphiques : petits DataFrames fictifs, code commenté, tableaux et illustrations SVG calculés sur les mêmes données.
- `docs/scripts/tp_content.py` contient le sujet, les données attendues, les quatre visuels, les deux insights de correction et la question facultative du TP.
- `docs/scripts/generer_donnees_tp.py` génère le CSV fictif du TP avec une graine fixe.
- `docs/assets/site.css` et `docs/assets/tableau.css` portent la charte TABLEAU existante.
- `docs/assets/course.css` et `docs/assets/quiz.js` sont générés ; modifier leur source dans le générateur.
- `docs/formateur/notebooks/` et `docs/corrections/` conservent les corrections.
- `docs/VALIDATION.md` décrit les calculs vérifiés et les limites des vérifications.

Les pages publiques sont sous `docs/`. La sandbox de travail est sous `sandbox-notebook/`. Ne pas réintroduire de notebooks de cours préremplis dans `sandbox-notebook/notebooks/`.

## Public et progression actuelle

Les étudiants connaissent les bases de Python, Pandas et Matplotlib. Ils lisent le cours dans une fenêtre et créent leur notebook dans JupyterLab.

Après le QCM de réactivation, le bloc « Découvrir cinq graphiques » présente les barres horizontales, les colonnes groupées, la courbe, le nuage de points et le boxplot. Chaque exemple comporte un petit DataFrame visible, le code Matplotlib commenté, son illustration et une lecture métier. Ce bloc est uniquement une présentation : pas d’exercice ni de QCM supplémentaire. Il est accessible dans les cartes de l’accueil et dans la navigation des cours, avant le bloc 01 ; la numérotation des blocs existants reste inchangée. Les étudiants peuvent essayer les cellules dans un notebook créé dans JupyterLab, sans fichier à charger.

| Bloc | Notions | Exercices |
| --- | --- | --- |
| 01 — Explorer les commandes | Grain, comptages distincts, catégories, années | 3 |
| 02 — Agréger et comparer | Totaux, parts simples, comparaison de contributions, classements | 4 |
| 03 — Comparer ventes et profit | Ratio des sommes, segments, périmètre filtré, moyenne des taux | 4 |
| 04 — Lire l’évolution mensuelle | Agrégation mensuelle, variation relative et en montant | 3 |
| 05 — Approfondir les cumuls | Cumul, base fixe, moyenne mobile, ratio des cumuls | 4 |
| 06 — Explorer les distributions | Quartiles, changement de grain, moyenne et médiane | 3 |

Le parcours contient 21 exercices. Le socle correspond aux blocs 01 à 04 ; les deux suivants sont des approfondissements. Le comptage par mois commence au bloc 04. Les parts simples précèdent la comparaison des parts de deux mesures.

Les exercices changent de mesure, de regroupement ou de période par rapport à l’exemple : clients par année après commandes par année, segments après régions, pertes d’une région après bilan global, cumuls recommencés sur une année après cumul de toute la période.

Préserver les conventions demandées pour la lisibilité :
```python
# Ajouter l’année avant de regrouper
orders["annee"] = orders["Order Date"].dt.year
commandes_annee = orders.groupby("annee")["Order ID"].nunique()

# Sélectionner la colonne avant les deux comptages
par_categorie = orders.groupby("Category")["Order ID"].agg(
    lignes="size",
    commandes="nunique"
)
```

## Données et environnement

### Cours : Superstore

`docs/data/sample_-_superstore.xls`, feuille `Orders`, est copié dans `sandbox-notebook/data/`. Il contient 10 194 lignes et 5 111 commandes distinctes. Une ligne représente une ligne de commande ; un Order ID peut se répéter.

Champs utilisés : Order ID, Order Date, Customer ID, Category, Sub-Category, Region, Segment, Sales et Profit. Les unités monétaires ne sont pas réputées être des euros.

Le chargement du premier bloc crée `df`, puis explicite `orders = df` pour la suite. Les dates doivent être reconnues comme dates avant `dt.year` ou `resample()`. La lecture du XLS nécessite `xlrd`.

`Profit / Sales` est le profit fourni rapporté aux ventes. Ne pas le nommer taux de marge commerciale : le coût d’achat des marchandises n’est pas fourni dans ce jeu.

### TP : réseau fictif Nova

`ventes_reseau_powerbi.csv` est un jeu distinct : 2 274 lignes, 1 273 commandes, année 2025, montants en euros HT. Sa génération utilise la graine `20261027`.

Champs : Ligne, Commande, Date, Region, Canal, Categorie, Produit, Quantite, Chiffre_affaires et Cout_achat. Le coût d’achat permet de calculer la marge commerciale comme différence avec le chiffre d’affaires. Le ratio demandé rapporte cette marge au chiffre d’affaires ; les autres charges ne sont pas décrites.

Les deux jeux sont accessibles sous `/workspace/data`, monté en lecture seule. Les figures sont exportées sous `/workspace/resultats`.

JupyterLab s’ouvre à `http://localhost:8890/lab`. Les liens ne pointent pas sur `/lab/tree/notebooks/...`.

## QCM du parcours

- Réactivation de 16 questions avant le premier bloc : bases Pandas et Matplotlib, distinction Series/DataFrame, regroupement sur deux champs et trois questions sur figsize, les DPI et les repères de taille des graphiques.
- Un QCM de synthèse de 15 questions après l’ensemble des blocs 01 à 04.
- Un QCM d’approfondissement de 8 questions après le bloc 06.

Tous utilisent le même moteur : une question visible, réponse verrouillée après le choix, feedback explicatif, passage à la suivante, bilan final. Le bouton « Recommencer » est masqué pendant toutes les questions et devient visible uniquement au bilan. Après remise à zéro, il est à nouveau masqué.

La génération répartit les bonnes réponses de façon déterministe et équilibrée entre A, B, C et D, avec au plus deux positions identiques consécutives. Le mélange déplace aussi les distracteurs et recalcule l’indice de correction ; la banque source conserve sa réponse de référence.

## Composants graphiques validés

La référence visuelle des cartes QCM est la carte d’accueil « Explorer les distributions », illustrée dans le dossier `images/`.

- `.path-card.qcm-path-card` : carte mauve, contenu intérieur espacé et bandeau foncé inférieur.
- `.qcm-card-content` ou `.qcm-course-link` : corps flexible avec son propre padding.
- `.qcm-inline-link` : lien sur toute la largeur du bandeau inférieur.
- `.course-section.qcm-section` : encart QCM dans un bloc de cours ; ce composant est distinct de la carte d’accueil.
- `.quiz-page .qcm-form` : questionnaire dans les tons généraux, sans fond mauve ni encadrement décoratif.
- `.course-layout.tp-layout` : navigation et sujet du TP sur deux colonnes, sans panneau Jupyter.

Couleurs de la charte : vert `#275c47`, lime `#b5cf66` pour les séries de graphiques ; mauve clair `#e8def6` et bandeau `#66518f` pour les cartes d’entrée des QCM. Reprendre les couleurs d’une nouvelle charte si le cours cible en utilise une autre.

Le bloc de découverte introduit `fig`, `ax` et `figsize=(8, 4)` à 100 DPI. Le bloc 01 reprend ces repères et fournit le tableau des formats. Son graphique guidé des lignes et commandes comporte deux séries, une légende et les valeurs avec `bar_label()`. Avec l’axe Matplotlib standard, un décalage positif en y déplace la barre vers le haut.

## TP actuel

Le TP prépare une maquette de tableau de bord Power BI avec Pandas et Matplotlib. Le sujet ne demande pas de fichier PBIX.

Les quatre graphiques sont :
1. Chiffre d’affaires mensuel.
2. Chiffre d’affaires par région.
3. Marge commerciale / chiffre d’affaires par catégorie.
4. Chiffre d’affaires et marge commerciale par canal, en barres groupées.

Demander exactement deux insights, chacun chiffré et relié aux graphiques, avec une implication métier ou une piste d’action. La question facultative croise région et canal au moyen d’un tableau ; elle n’ajoute pas un cinquième graphique.

Le sujet étudiant expose uniquement mission, données et dictionnaire, travail demandé, livrables et question facultative. Il ne comporte pas d’horaires, de barème, d’organisation des passages ni de panneau latéral Jupyter.

## Régénération et vérification

Depuis la racine :
```bash
python docs/scripts/generer_donnees_tp.py  # seulement pour régénérer le CSV fictif
python docs/scripts/construire.py
python -m unittest discover -s docs/tests -v
node --check docs/assets/quiz.js
```

Le générateur copie les données vers la sandbox ; il ne crée pas de notebook étudiant dans cette dernière. Vérifier que les 21 exercices, les liens, les trois QCM et les corrections formateur restent cohérents après une modification.

Si `xlrd` ou Matplotlib manquent localement, distinguer les vérifications possibles. Un export exact avec R `readxl` permet de contrôler les calculs du XLS avec Pandas ; exclure les appels de tracé ne valide pas le rendu graphique. Consigner cette limite dans `docs/VALIDATION.md`.

