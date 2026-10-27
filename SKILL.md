---
name: cours-web-exercices-qcm
description: Concevoir ou réviser un cours web avec une charte existante, des exemples guidés, des exercices autonomes, des QCM séquentiels et un TP. Utiliser pour reproduire ce modèle pédagogique sur un autre sujet ou améliorer un parcours existant.
---

# Cours web avec exercices autonomes et QCM

Produire un parcours lisible où chaque exemple prépare un exercice, puis une application autonome. Adapter le sujet, les données, les prérequis et le nombre de blocs à la demande. Les consignes récentes de l’utilisateur priment sur les paramètres d’un cours précédent.

Pour intervenir dans le projet Matplotlib actuel ou s’en servir comme réalisation de référence, lire [le modèle Matplotlib et Power BI](references/pattern-matplotlib.md). Les chemins, données et nombres de questions de cette référence décrivent ce projet ; ils ne sont pas à imposer à tous les cours.

## Préparer la progression

Avant de rédiger ou de modifier :
- Identifier le public, ses acquis, les objectifs, le contexte métier et le travail final.
- Repérer la source effective des contenus et le générateur éventuel ; des définitions anciennes peuvent être remplacées au chargement.
- Examiner la charte existante et les captures fournies. Identifier le composant précis à reproduire : carte d’accueil, encart de cours ou page de questions.
- Dresser une correspondance entre chaque notion, ses prérequis, son exemple, son exercice et son livrable.

Introduire les notions dans l’ordre de leurs dépendances. Commencer par un calcul simple avant une comparaison de plusieurs mesures. Expliquer les méthodes et les unités au moment de leur première utilisation. Réserver les approfondissements à une partie identifiée ; le TP obligatoire doit rester réalisable avec les notions du socle.

## Construire les blocs

Ouvrir chaque bloc par une question concrète et quelques notions utiles, puis proposer plusieurs séquences :
1. Un exemple guidé, avec des étapes courtes et du code commenté lorsque le sujet en comporte.
2. Un résultat visible : graphique, tableau, capture ou démonstration pertinente.
3. Une interprétation brève qui explique ce résultat et ses limites.
4. Un exercice autonome portant sur une application nouvelle.

Chaque exercice comporte un titre, une consigne claire et un livrable. Conserver une difficulté principale identifiable. Les apprenants doivent pouvoir comprendre ce qu’ils cherchent et reconnaître le travail à produire.

Pour les cours de code :
- Montrer du code complet dans les exemples et commenter l’intention des opérations.
- Préférer des étapes et variables intermédiaires lisibles aux expressions imbriquées.
- Laisser les apprenants écrire le code des exercices.
- Exclure des exercices les amorces de code, « Code à compléter », indices, valeurs attendues et critères donnant la réponse.
- Conserver les corrections dans les supports formateur. Ne pas placer de correction ou de « Mise en commun » sous les exercices, même repliée.

Ne pas afficher de durées dans les blocs du cours : l’enseignant gère le rythme.

## Auditer les répétitions

Contrôler les exercices entre eux et chaque exercice face à son propre exemple. Une réponse déjà donnée dans l’interprétation ou directement lisible dans le résultat de l’exemple ne constitue pas un exercice autonome suffisant.

Réutiliser une technique est utile si l’exercice change au moins un élément pertinent : mesure, regroupement, périmètre, référence, période ou comparaison à effectuer. Le changement doit conduire à une véritable recherche, sans introduire une méthode encore inexpliquée.

Remplacer les doublons par de nouvelles applications en conservant la quantité de pratique attendue. Distinguer les exercices de lecture assumés des exercices de programmation ; ne pas transformer une séquence entière en questions de lecture répétitives.

## Placer et faire fonctionner les QCM

Insérer les QCM dans la progression :
- Réactivation au début, sur les prérequis.
- Consolidation après les blocs qui enseignent les notions évaluées.
- Éventuellement un QCM d’approfondissement après les contenus avancés.

Adapter leurs nombres de questions au cours. Ne pas regrouper tous les QCM dans une section isolée en fin d’accueil.

Chaque QCM suit ce fonctionnement :
1. Une seule question est visible, avec sa position dans le questionnaire.
2. La question propose quatre choix et une seule réponse correcte.
3. Le choix enregistre et verrouille la réponse.
4. Le feedback apparaît pour cette question : réponse retenue, réponse correcte et explication du principe.
5. L’apprenant passe explicitement à la question suivante après avoir pu lire l’explication.
6. Le bilan et le score apparaissent après la dernière question.
7. « Recommencer » apparaît uniquement au bilan final.
8. Recommencer remet à zéro les réponses, le score, les feedbacks, les contrôles et la position dans le QCM.

Le feedback doit expliquer le raisonnement et la confusion éventuelle, plutôt que se limiter à « correct » ou « incorrect ». Préserver le focus clavier lors du passage à la question suivante.

Répartir les bonnes réponses entre A, B, C et D de manière variée et équilibrée, sans cycle prévisible. Si les choix sont mélangés, recalculer l’indice de correction et vérifier qu’il désigne toujours le même texte correct. Contrôler cette correspondance sur chaque QCM, ainsi que le feedback et le score après mélange.

## Reprendre la charte graphique

Réutiliser les composants réels de la référence, pas seulement une couleur approchante. Centraliser les styles partagés pour que les cartes équivalentes aient la même structure.

Dans le modèle validé :
- Les cartes de cours restent claires.
- Les cartes d’entrée des QCM portent l’accent distinctif de la charte et un bandeau d’action sur toute leur largeur.
- À l’intérieur des QCM, reprendre les tons généraux du cours, sans grand panneau coloré ni encadrement décoratif.
- Les réponses et le feedback restent lisibles et leur état compréhensible.

Prévoir un conteneur intérieur avec son espacement lorsqu’une carte utilise un bandeau bord à bord. Les grilles utilisent des colonnes réductibles ; les enfants peuvent se rétrécir et les textes longs se replient. Les blocs de code défilent horizontalement dans leur propre conteneur. Une colonne supprimée doit être retirée de la grille, sans laisser une zone vide.

Utiliser des graphiques qui répondent à des questions différentes. Faire correspondre code et illustration : données, ordre des catégories, légendes, couleurs, unités et valeurs affichées. Ne pas réutiliser une même image pour illustrer des résultats différents.

Si la référence distante ou le rendu navigateur est inaccessible, exploiter les fichiers locaux et les captures disponibles ; préciser ce qui a réellement pu être inspecté.

## Organiser la pratique et le TP

Pour un atelier Jupyter, les boutons du cours ouvrent l’accueil de JupyterLab. Les apprenants créent leur notebook. Ne pas générer ni synchroniser de notebooks étudiants préremplis dans la sandbox, sauf demande explicite. Les corrections formateur restent en dehors de la sandbox.

Le TP étudiant contient uniquement :
- Le contexte et la mission.
- Les données, leur grain, les champs nécessaires et leurs unités.
- Les tâches et les livrables.
- Une question facultative lorsqu’elle est demandée, clairement identifiée.

Le nombre de graphiques, d’insights ou d’autres livrables vient de la demande. Une question facultative peut approfondir l’analyse avec un tableau sans augmenter le nombre de graphiques imposé.

Ne pas afficher de barème, note, horaire, repères de passage ou consignes de soutenance dans le sujet. Dans ce modèle, le TP ne comporte pas de panneau latéral Jupyter. Les informations d’organisation relèvent de l’enseignant.

## Choisir et vérifier les données

Vérifier le fichier effectivement utilisé : schéma, types, dates, grain, valeurs manquantes, identifiants répétés et unités. Donner un chemin de chargement cohérent avec l’environnement et employer des noms de variables compatibles dans tout le support.

Calculer les résultats sur la source réelle. Un jeu synthétique doit être identifié comme fictif et reproductible, avec son mode de génération documenté. Ne pas mélanger ses résultats avec ceux d’un jeu réel ou d’un ancien cours.

Définir les indicateurs avant leur interprétation. Pour les ratios agrégés, préciser numérateur, dénominateur et périmètre ; vérifier les dénominateurs nuls. Dans un cours commercial, distinguer profit fourni, marge commerciale calculable et ratio rapporté aux ventes selon les champs réellement disponibles.

## Générer et contrôler les supports

Modifier les sources du générateur puis régénérer les pages et les corrections. Éviter les modifications isolées du HTML ou du CSS générés qui seraient perdues à la prochaine génération. Préserver les contenus déjà validés hors du périmètre de la demande.

Contrôler les comportements utiles :
- Ordre des prérequis et absence de réponses données avant l’exercice.
- Concordance entre consignes et corrections formateur.
- Résultats calculés, graphiques et unités cohérents.
- Liens, ancres, accès aux données et mise en page sur plusieurs largeurs.
- QCM séquentiel, feedback, score et remise à zéro uniquement depuis le bilan.
- Accès à JupyterLab sans ouverture automatique d’un notebook préparé.

Exécuter les vérifications adaptées aux changements. Distinguer compilation du code, exécution des calculs et rendu effectif des graphiques. Signaler les dépendances ou accès qui ont empêché une vérification, sans annoncer un rendu ou une exécution qui n’a pas eu lieu.
