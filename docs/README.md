# Le labo Matplotlib — parcours Superstore

Le support source est [l’accueil du parcours](index.html). Il reprend les couleurs, la typographie et les composants TABLEAU (`site.css` et `tableau.css`, copiés sans modification), sans en reprendre les leçons. Le style complémentaire reste dans `assets/course.css`.

## Données

Le classeur utilisé est `data/sample_-_superstore.xls`, feuille `Orders`. Il contient 10 194 lignes et 21 colonnes ; une ligne décrit une ligne de commande, et un même Order ID peut se répéter.

## Parcours

- QCM de réactivation, puis [découverte de cinq graphiques](supports/00_decouvrir_graphiques.html) sur de petits DataFrames fictifs.
- Blocs 01 à 04 : socle du matin, de la vérification des données à la variation mensuelle.
- TP en binômes : quatre graphiques et deux insights.
- Cumuls, moyenne mobile et boxplots : approfondissements autonomes.

Les cours ne lient pas de notebook prérempli. Les apprenants ouvrent JupyterLab et créent leur propre notebook. Les corrections formateur restent dans `formateur/notebooks/`, hors de la sandbox.

## Lancer JupyterLab avec Docker

Depuis la racine du dépôt :

```bash
cd sandbox-notebook
docker compose up --build -d
docker compose logs notebook
```

Ouvrir http://localhost:8890/lab et utiliser le jeton affiché dans les journaux. Le classeur Superstore est monté en lecture seule sous `/workspace/data`; les exports vont dans `/workspace/resultats`. Le lecteur `xlrd` est nécessaire à la lecture du `.xls`.

## Régénérer les supports

```bash
python scripts/construire.py
```

La feuille CSS `site.css` et la feuille de thème `tableau.css` sont conservées à l’identique.

## Progression des exercices

Le parcours conserve 21 exercices autonomes dans les blocs 01 à 06. Le bloc [Questions maths](supports/questions_maths.html), placé entre le bloc 04 et le QCM de synthèse, ajoute six questions sans corrigé : quatre fondamentales et deux approfondissements facultatifs. Le bloc 01 travaille les comptages annuels ; les regroupements mensuels commencent au bloc 04. Dans le bloc 02, une part du total précède la comparaison de deux contributions. Les exercices du bloc 03 appliquent les indicateurs à des sous-catégories, des segments et une région filtrée. Le bloc 05 fait changer de référence et recommencer les cumuls sur une année réelle. Les consignes étudiantes ne contiennent ni amorce de code ni correction sous les exercices.

## Données du TP Power BI

Le TP utilise un autre jeu, fictif : [ventes_reseau_powerbi.csv](data/ventes_reseau_powerbi.csv). Il décrit les ventes 2025 du réseau Nova par date, région, canal, catégorie et produit. Le chiffre d’affaires et le coût d’achat, exprimés en euros HT, permettent de calculer une marge commerciale. Les apprenants créent quatre graphiques avec Pandas et Matplotlib et rédigent exactement deux insights chiffrés pour préparer un futur tableau de bord Power BI.

Les données se régénèrent avec `python scripts/generer_donnees_tp.py` (graine fixe `20261027`). `python scripts/construire.py` copie le CSV dans la sandbox et régénère le sujet et les corrections formateur.
