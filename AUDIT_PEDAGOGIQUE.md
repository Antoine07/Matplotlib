# Audit et réorganisation pédagogique

## Constats sur la première version

Le support entrait rapidement dans Figure / Axes et les détails de chemins, sans galerie pour donner du sens aux représentations. Seaborn n'était pas situé. Les exercices étaient regroupés après plusieurs notions, ce qui retardait la pratique et la correction collective. Le programme annoncé ne couvrait pas encore les indicateurs proposés.

## Choix retenus

1. Rappeler le rôle de pandas, Matplotlib et Seaborn, puis observer trois graphiques sur le même CSV.
2. Conserver l'exemple de chargement simple demandé, dans la partie Introduction puis la séquence de chargement du bloc 1.
3. Enseigner chaque geste avec un exemple, un petit exercice et une correction accessible séparément pour la mise en commun.
4. Répartir les indicateurs : part du total au bloc 1 ; variation, évolution depuis l'origine, cumul, lissage et marge sur CA au bloc 2.
5. Donner à chaque bloc son QCM à feedback, avec une révision facultative par flashcards.
6. Garder la passerelle Power BI facultative, sans exiger de manipulation DAX dans le parcours Matplotlib.
7. N'afficher aucune durée pédagogique. Le formateur règle le rythme et décide de l'ouverture des corrections.

## Points de vigilance intégrés au contenu

- Le grain du CSV est la ligne de vente ; un histogramme de Ventes ne compte pas des commandes distinctes.
- Seaborn utilise Matplotlib. histplot compte ici des observations ; barplot estime par défaut une moyenne et ne remplace pas automatiquement l'agrégation des ventes.
- Une part doit nommer son dénominateur et son périmètre.
- Le scénario mensuel est distinct du CSV de janvier et contient des profits fictifs fournis.
- pct_change compare les lignes dans leur ordre ; une référence absente n'est pas une variation nulle.
- rolling(3) signifie trois lignes : le calendrier doit être complet pour parler de trois mois consécutifs.
- Un cumul de ventes positives peut monter pendant une baisse mensuelle ; avec des montants négatifs, la monotonie n'est plus garantie.
- La marge globale sur CA est le ratio des sommes. Elle diffère ici de la moyenne simple des taux mensuels.
- Les divisions par zéro sont indéfinies et ne doivent pas devenir artificiellement 0 %.
- RUNNINGSUM et MOVINGAVERAGE sont des calculs visuels Power BI : les axes, l'ordre, les fenêtres et le contexte doivent être vérifiés.

## Critères de réussite

L'apprenant sait prédire un résultat simple, choisir une représentation, expliquer le code utile, vérifier une valeur, corriger une erreur et formuler une observation avec unité et référence. Le QCM sert à identifier les notions à reprendre ; son score ne remplace pas l'observation des exercices.
