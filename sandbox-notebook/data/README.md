# Données commerciales fictives

`commandes.csv` est une copie identique de `TABLEAU/docs/data/tp01_commandes_detail.csv`, renommée pour la sandbox. Aucune ligne ni valeur n'a été modifiée.

- 60 lignes de vente, 30 commandes distinctes.
- Période : 1er au 30 janvier 2026 (pas un mois calendaire complet).
- Trois régions : Nord, Ouest, Sud ; deux canaux : En ligne, Magasin.
- Trois catégories, six produits ; total Ventes : **45 831 €**.

| Champ | Type / sens |
|---|---|
| Ligne | Identifiant unique de ligne |
| Commande | Identifiant de commande ; plusieurs lignes possibles |
| Date | Date de commande, format ISO |
| Region | Région commerciale |
| Canal | En ligne ou Magasin |
| Categorie | Famille de produits |
| Produit | Produit vendu |
| Quantite | Nombre d'unités |
| Prix_unitaire | Euros avant remise |
| Remise | Fraction (0.05 = 5 %) |
| Ventes | Quantite × Prix_unitaire × (1 − Remise), euros après remise |

Les coûts, bénéfices et retours ne sont pas disponibles. Le jeu est pédagogique, pas un relevé d'activité réel. Ne pas extrapoler janvier à une année ni présenter une vente moyenne par ligne comme un panier moyen par commande.

## Scénario mensuel du bloc 2

`indicateurs_mensuels.csv` reprend les six lignes construites dans le notebook 02 : dates de janvier à juin 2026, ventes et profits fictifs en euros. Une ligne = un mois. Total ventes : 80 500 € ; total profit : 18 350 €.

Ce scénario est **indépendant** des commandes du premier fichier : il ne s'agit pas de leur agrégation ni d'un prolongement de leurs montants. La marge sur chiffre d'affaires du scénario vaut environ 22,80 %.

`visuels/` contient les trois graphiques d'observation du bloc 1, produits à partir de commandes.csv. Ils permettent de commencer le carnet sans avoir encore exécuté le code.
