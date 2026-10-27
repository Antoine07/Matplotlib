"""Contenu pédagogique commun aux supports HTML et aux notebooks."""
LOAD = '''import pandas as pd
import matplotlib.pyplot as plt

ventes = pd.read_csv("/workspace/data/commandes.csv", parse_dates=["Date"])

print("Nombre de lignes :", len(ventes))
print("Nombre de commandes :", ventes["Commande"].nunique())
print("Chiffre d'affaires :", ventes["Ventes"].sum())

ventes.head()'''
MONTHS = '''import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "mois": pd.date_range("2026-01-01", periods=6, freq="MS"),
    "ventes": [10000, 12000, 9000, 15000, 18000, 16500],
    "profit": [2000, 3000, 1800, 3750, 4500, 3300]
})
df = df.sort_values("mois").reset_index(drop=True)
mois = df["mois"].dt.strftime("%m/%Y")
df'''

def plot(body, name):
    return body + f'\nfig.savefig("/workspace/resultats/{name}.png", dpi=140, bbox_inches="tight")\nplt.show()'

CATEGORY = plot('''par_categorie = ventes.groupby("Categorie")["Ventes"].sum().sort_values()
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.barh(par_categorie.index, par_categorie.values, color="#275c47")
ax.set_title("Ventes par catégorie · 1–30 janvier 2026")
ax.set_xlabel("Ventes après remise (€)")''','01_categories')
REGION = plot('''par_region = ventes.groupby("Region")["Ventes"].sum().sort_values()
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.barh(par_region.index, par_region.values, color="#275c47")
ax.set_title("Ventes par région · 1–30 janvier 2026")
ax.set_xlabel("Ventes après remise (€)")''','01_regions')
READABLE = plot('''par_categorie = ventes.groupby("Categorie")["Ventes"].sum().sort_values()
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.barh(par_categorie.index, par_categorie.values, color="#275c47")
ax.set_title("L’informatique domine les ventes · 1–30 janvier 2026")
ax.set_xlabel("Ventes après remise (€) · Toutes régions")
ax.set_xlim(left=0)
ax.grid(axis="x", alpha=0.2)
ax.set_axisbelow(True)''','01_lisible')
BUG = '''totaux = ventes.groupby("Categorie")["Ventes"].sum()
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.barh(totaux.index, sorted(totaux.values))
ax.set_title("Résultats")
plt.show()'''
PARTS = plot('''parts = par_categorie / par_categorie.sum() * 100
print(parts.round(2))
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.barh(parts.index, parts.values, color="#275c47")
ax.set_title("Poids des catégories · 1–30 janvier 2026")
ax.set_xlabel("Part des ventes de toute la boutique (%)")
ax.set_xlim(0, 100)''','01_parts')
PARTS_REGION = plot('''par_region = ventes.groupby("Region")["Ventes"].sum().sort_values()
parts_region = par_region / par_region.sum() * 100
print(parts_region.round(2))
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.barh(parts_region.index, parts_region.values, color="#275c47")
ax.set_title("Poids des régions · 1–30 janvier 2026")
ax.set_xlabel("Part des ventes de toute la boutique (%)")
ax.set_xlim(0, 100)''','01_parts_regions')
HIST = plot('''fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.hist(ventes["Ventes"], bins=6, color="#275c47", edgecolor="white")
ax.set_title("Répartition des montants · 60 lignes de vente")
ax.set_xlabel("Montant d’une ligne après remise (€)")
ax.set_ylabel("Nombre de lignes de vente")''','01_histogramme')
SEA = plot('''import seaborn as sns

fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
sns.histplot(data=ventes, x="Ventes", bins=6, ax=ax, color="#275c47")
ax.set_title("Répartition des montants · 60 lignes de vente")
ax.set_xlabel("Montant d’une ligne après remise (€)")
ax.set_ylabel("Nombre de lignes de vente")''','01_seaborn')
SEA_EX = SEA.replace('bins=6','bins=3').replace('01_seaborn.png','01_seaborn_3_classes.png')
DAILY = plot('''par_jour = ventes.groupby("Date")["Ventes"].sum().sort_index()
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.plot(par_jour.index.day, par_jour.values, marker="o", color="#275c47")
ax.set_title("Ventes quotidiennes · janvier 2026")
ax.set_xlabel("Jour de janvier")
ax.set_ylabel("Ventes après remise (€)")
ax.set_ylim(bottom=0)''','01_courbe')
MONTHLY = plot('''fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.plot(mois, df["ventes"], marker="o", color="#275c47")
ax.set_title("Ventes mensuelles · Scénario fictif")
ax.set_ylabel("Ventes (€)")
ax.set_ylim(bottom=0)''','02_mensuel')
VARIATION = plot('''df["variation_pct"] = df["ventes"].pct_change() * 100
print(df["variation_pct"].round(2))
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.bar(mois, df["variation_pct"], color="#275c47")
ax.axhline(0, color="#203b36", linewidth=1)
ax.set_title("Variation par rapport au mois précédent")
ax.set_ylabel("Variation (%)")''','02_variation')
EVOLUTION = plot('''df["evolution_pct"] = (df["ventes"] / df["ventes"].iloc[0] - 1) * 100
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.plot(mois, df["evolution_pct"], marker="o", color="#275c47")
ax.axhline(0, color="#203b36", linewidth=1)
ax.set_title("Évolution des ventes depuis janvier")
ax.set_ylabel("Écart à janvier (%)")''','02_evolution')
CUMUL = plot('''df["ventes_cumulees"] = df["ventes"].cumsum()
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.plot(mois, df["ventes_cumulees"], marker="o", color="#275c47")
ax.set_title("Ventes accumulées depuis janvier")
ax.set_ylabel("Ventes cumulées (€)")
ax.set_ylim(bottom=0)''','02_cumul')
ROLL = plot('''df["moyenne_mobile"] = df["ventes"].rolling(3).mean()
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.plot(mois, df["ventes"], marker="o", label="Ventes", color="#275c47")
ax.plot(mois, df["moyenne_mobile"], marker="s", linestyle="--",
        label="Moyenne sur 3 mois", color="#945324")
ax.set_title("Observer les ventes et leur lissage")
ax.set_ylabel("Ventes (€)")
ax.legend()''','02_moyenne_mobile')
MARGIN = plot('''df["marge_pct"] = df["profit"] / df["ventes"] * 100
marge_globale = df["profit"].sum() / df["ventes"].sum() * 100
print("Marge sur CA du semestre :", round(marge_globale, 2), "%")
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.bar(mois, df["marge_pct"], color="#275c47")
ax.set_title("Marge rapportée au chiffre d’affaires · Par mois")
ax.set_ylabel("Profit / ventes (%)")
ax.set_ylim(0, 30)''','02_marge')
MARGIN_CUM = plot('''df["marge_cumulee_pct"] = df["profit"].cumsum() / df["ventes"].cumsum() * 100
moyenne_taux = df["marge_pct"].mean()
print("Ratio cumulé final :", round(df["marge_cumulee_pct"].iloc[-1], 2))
print("Moyenne des taux mensuels :", round(moyenne_taux, 2))
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.plot(mois, df["marge_cumulee_pct"], marker="o", color="#275c47")
ax.set_title("Marge sur CA cumulée depuis janvier")
ax.set_ylabel("Profit cumulé / ventes cumulées (%)")
ax.set_ylim(0, 30)''','02_marge_cumulee')

def ex(title, prompt, deliverable, success, hints, solution='', answer='', starter='# À vous de jouer.\n', objective='', prereq='Exemple juste au-dessus.'):
    return dict(title=title,prompt=prompt,deliverable=deliverable,success=success,hints=hints,solution=solution,answer=answer,starter=starter,objective=objective or title,prereq=prereq)

B1 = [
 dict(id='observer',title='Lire un premier graphique',text='''<h2>Matplotlib en un coup d’œil.</h2><p>Matplotlib transforme des valeurs en graphiques, puis permet d’en régler les éléments et d’exporter l’image. pandas prépare les données ; Matplotlib les représente. Seaborn s’appuie sur Matplotlib pour faciliter certains graphiques statistiques. Nous le verrons après les premiers exemples.</p><h3>Exemple : ventes par catégorie</h3><p>Cette figure présente les ventes de janvier regroupées par catégorie.</p>''',figure='01_categories',alt='Trois barres horizontales comparent les ventes par catégorie. La barre Informatique est la plus longue.',code='',reading='''L’axe vertical nomme les catégories. L’axe horizontal indique le montant des ventes après remise, en euros. La longueur des barres permet de comparer les montants.''',
 exercise=ex('Lire le graphique','Quelle catégorie réalise le plus de ventes ?','Une réponse dans une phrase.','La phrase nomme la catégorie et s’appuie sur sa barre.',['Comparez la longueur des trois barres.'],answer='Informatique réalise le plus de ventes : sa barre est la plus longue.')),
 dict(id='charger',title='Charger et comprendre',text='''<h2>Lire le fichier, vérifier le grain.</h2><p>Une ligne du fichier représente une <strong>ligne de vente</strong>. Une commande peut en contenir plusieurs. Le CSV reprend à l’identique les données du TP Tableau : trois régions, trois catégories, six produits, du 1er au 30 janvier 2026.</p><p><code>Ventes</code> est le montant après remise : quantité × prix unitaire × (1 − remise). Exemple : 2 écrans × 220 € × (1 − 0,05) = 418 €. Le fichier ne contient ni coûts ni profits.</p>''',code=LOAD,reading='''<code>read_csv</code> ouvre le fichier dans la sandbox Docker ; <code>parse_dates</code> transforme Date en dates. <code>len</code> compte les lignes, <code>nunique</code> les commandes distinctes et <code>sum</code> additionne les ventes. <code>head()</code> montre les cinq premières lignes. Résultat attendu : 60 lignes, 30 commandes, 45 831 €.''',
 exercise=ex('Combien de produits ?','Prédisez ce que compte ventes["Produit"].nunique(), puis exécutez-le. Expliquez pourquoi 60 lignes ne signifie pas 60 commandes.','Une valeur et une phrase.','Six produits distincts ; une commande peut contenir plusieurs lignes.',['Reprenez le comptage de Commande.','Changez uniquement le nom de la colonne.'],solution='print("Produits distincts :", ventes["Produit"].nunique())',answer='Le résultat est 6 : il compte les noms de produits distincts. Les 60 lignes appartiennent à 30 commandes.')),
 dict(id='construire',title='Préparer puis tracer',text='''<h2>Des lignes aux barres.</h2><p>Pour comparer les ventes par catégorie, il faut d’abord additionner les montants de chaque groupe. Matplotlib reçoit les résultats : <code>barh</code> ne réalise pas cette addition.</p><div class="concept-grid"><article><h3>Figure : <code>fig</code></h3><p>Le document entier, sa taille et son export.</p></article><article><h3>Axes : <code>ax</code></h3><p>Une zone de dessin, avec ses marques, son titre et ses axes gradués.</p></article></div>''',code=CATEGORY,figure='01_categories',alt='Informatique 30 776 euros, Mobilier 13 302,50 euros, Accessoires 1 752,50 euros.',reading='''<code>groupby</code> forme les groupes, <code>sum</code> calcule leurs totaux, puis <code>sort_values</code> trie la Series avec ses étiquettes. <code>subplots</code> crée fig et ax ; figsize règle la taille, layout ajuste les marges. <code>barh</code> associe l’index aux montants. La première barre est en bas : le tri croissant place la plus grande en haut. <code>set_title</code> et <code>set_xlabel</code> donnent le contexte. <code>savefig</code> exporte le document dans le dossier prévu par Docker ; <code>show</code> l’affiche. Contrôle : les trois barres totalisent 45 831 €. La taille est en pouces, dpi règle la résolution et bbox_inches évite de couper les textes.''',
 exercise=ex('Comparer les régions','Reprenez l’exemple en regroupant par Region. Adaptez le titre et enregistrez 01_regions.png. Quelle région arrive en tête ?','Une figure et une observation chiffrée.','Trois barres ; Nord en tête ; total conservé.',['Changez la colonne dans groupby.','Triez la Series entière avant de transmettre index et values.'],solution=REGION,answer='Nord : 18 979,50 € ; Sud : 14 596,50 € ; Ouest : 12 255 €. Les barres comparent des catégories et la somme mesure leurs ventes cumulées. Le total reste 45 831 €.')),
 dict(id='lisibilite',title='Rendre la figure fiable',text='''<h2>Un graphique lisible doit être juste.</h2><p>Ajoutons un titre qui répond à la question, une unité, le périmètre et une grille légère. Pour des barres de montants positifs, l’origine à zéro permet de comparer les longueurs.</p>''',code=READABLE,figure='01_lisible',alt='Barres triées avec origine zéro, titre informatif, unité en euros et grille légère.',reading='''<code>set_xlim(left=0)</code> fixe le début de l’axe horizontal ; <code>grid(axis="x", alpha=0.2)</code> trace une grille légère. <code>set_axisbelow(True)</code> la place derrière les barres. Les données sont identiques à l’exemple précédent ; seule la présentation évolue.''',
 exercise=ex('Réparer un graphique trompeur','Exécutez le code ci-dessous. Comparez ses barres au tableau de sommes. Corrigez l’association des catégories et montants, puis rendez le titre et l’unité explicites.','Une figure corrigée et la cause du bug.','Informatique retrouve 30 776 € ; la justification explique pourquoi le total seul ne suffit pas.',['Comparez l’ordre des noms et celui des valeurs.','sort_values() garde chaque valeur avec son index. sorted(totaux.values) ne le fait pas.'],solution=READABLE.replace('01_lisible.png','01_audit_corrige.png'),answer='sorted(totaux.values) trie les montants seuls : les valeurs de Mobilier et Informatique sont échangées. Une somme globale reste juste après une permutation. Il faut vérifier chaque paire catégorie–montant.',starter=BUG)),
 dict(id='parts',title='Mesurer une part du total',text='''<h2>Quel poids dans l’ensemble ?</h2><p>La part d’une catégorie est son montant divisé par le total du périmètre, multiplié par 100. Ici, Informatique représente 30 776 / 45 831 × 100 ≈ <strong>67,15 %</strong>.</p><p>Le dénominateur fait partie de la définition : « part des ventes de toute la boutique » n’est pas « part des ventes du Sud ».</p>''',code=PARTS,figure='01_parts',alt='Parts des catégories : Informatique environ 67,15 %, Mobilier 29,02 %, Accessoires 3,82 %.',reading='''La division applique le même total à chaque montant de la Series. <code>* 100</code> exprime la fraction en pourcentage. <code>round(2)</code> sert à afficher, sans modifier les valeurs utilisées pour le tracé. Les parts non arrondies totalisent 100 % ; un petit écart est possible après arrondi.''',
 exercise=ex('Le poids des régions','Calculez les parts de vente des trois régions et représentez-les. Écrivez le dénominateur utilisé dans votre commentaire.','Des barres en pourcentage et une phrase.','La somme des parts non arrondies vaut 100 % ; le Nord représente environ 41,41 %.',['Réutilisez les sommes par région.','Divisez chaque somme régionale par le total de ces sommes.'],solution=PARTS_REGION,answer='Dénominateur : 45 831 €, toutes régions sur le fichier de janvier. Nord ≈ 41,41 %, Sud ≈ 31,85 %, Ouest ≈ 26,74 %. Une part n’est ni une variation ni une marge.')),
 dict(id='seaborn',title='Situer Seaborn',text='''<h2>Une autre façon de construire le même graphique.</h2><p>Un histogramme compte les observations dans des intervalles de valeurs. Ici, on étudie les montants des <strong>60 lignes de vente</strong>, pas les paniers des 30 commandes. Le nombre d’intervalles change la finesse de lecture.</p><h3>Exemple Matplotlib</h3>''',before_code=HIST,code=SEA,figure='01_seaborn',alt='Histogramme Seaborn en six intervalles, affichant les effectifs des lignes selon leur montant.',reading='''<code>ax.hist</code> reçoit une colonne de nombres ; <code>sns.histplot</code> reçoit la table et le nom du champ. Dans les deux cas, bins=6 demande six intervalles. Avec <code>ax=ax</code>, Seaborn dessine dans notre Axes : les réglages et l’export restent ceux de Matplotlib. Certaines autres fonctions Seaborn agrègent automatiquement : par exemple, barplot estime une moyenne par défaut, pas une somme de ventes.''',
 exercise=ex('Changer la finesse de lecture','Avant d’exécuter, prédisez l’effet de bins=3 à la place de bins=6 dans histplot. Faites le changement et expliquez ce qui reste identique.','Un histogramme et une observation.','Trois intervalles plus larges ; toujours 60 observations au total.',['Le paramètre bins agit sur les intervalles.','Il ne filtre aucune ligne et ne transforme pas les lignes en commandes.'],solution=SEA_EX,answer='Les 60 montants restent les mêmes. Trois intervalles donnent une lecture plus grossière ; le total des effectifs reste 60. On ne déduit pas de cet histogramme un nombre de commandes.')),
]

B2 = [
 dict(id='variation',title='Variation mensuelle',text='''<h2>Que s’est-il passé depuis le mois précédent ?</h2><p>Variation = (valeur actuelle / valeur précédente − 1) × 100. En février : (12 000 / 10 000 − 1) × 100 = <strong>+20 %</strong>. Le dénominateur change chaque mois.</p>''',code=VARIATION,figure='02_variation',alt='Variations : février +20 %, mars −25 %, avril +66,67 %, mai +20 %, juin −8,33 %. Janvier non défini.',reading='''<code>pct_change()</code> compare chaque ligne à la précédente et renvoie une fraction ; multiplier par 100 donne un pourcentage. Janvier vaut NaN faute de mois précédent : ce n’est pas 0 %. <code>bar</code> dessine des barres verticales et <code>axhline(0)</code> marque la séparation entre hausse et baisse.''',
 exercise=ex('Expliquer la baisse de mars','Calculez à la main la variation de mars, puis vérifiez la ligne correspondante. Quel est le dénominateur ? Interprétez la barre négative.','Un calcul et une phrase.','−25 %, calculé par rapport aux 12 000 € de février.',['Comparez 9 000 à 12 000.','(9000 / 12000 - 1) * 100.'],solution='print((9000 / 12000 - 1) * 100)\nprint(df.loc[2, "variation_pct"])',answer='Mars vend 3 000 € de moins que février, soit −25 %. Ce pourcentage ne compare pas mars à janvier.')),
 dict(id='evolution',title='Évolution depuis janvier',text='''<h2>Garder une référence fixe.</h2><p>Évolution depuis l’origine = (valeur actuelle / valeur initiale − 1) × 100. En mars : (9 000 / 10 000 − 1) × 100 = <strong>−10 %</strong>. La référence est toujours janvier.</p>''',code=EVOLUTION,figure='02_evolution',alt='Évolution depuis janvier : 0 %, 20 %, −10 %, 50 %, 80 %, 65 %.',reading='''<code>iloc[0]</code> prend la première valeur après le tri chronologique. <code>plot</code> relie les mois ; marker rend chaque observation visible. Janvier vaut 0 % car il se compare à lui-même. Cette évolution est parfois dite cumulée : elle ne consiste pas à additionner les variations mensuelles.''',
 exercise=ex('Deux constats sur juin','Retrouvez la variation de juin par rapport à mai et son évolution depuis janvier. Formulez une phrase qui contient les deux sans contradiction.','Deux valeurs et une phrase.','Environ −8,33 % sur le mois et +65 % depuis janvier.',['Les références sont 18 000 et 10 000.','Une baisse récente peut coexister avec un niveau supérieur au point de départ.'],solution='print(df.loc[5, ["variation_pct", "evolution_pct"]].round(2))',answer='Juin recule de 8,33 % par rapport à mai, mais ses ventes restent 65 % au-dessus de janvier. Additionner les variations mensuelles serait incorrect.')),
 dict(id='cumul',title='Somme cumulée',text='''<h2>Combien a-t-on vendu depuis le départ ?</h2><p>La somme cumulée additionne les montants depuis janvier jusqu’au mois observé. Fin mars : 10 000 + 12 000 + 9 000 = <strong>31 000 €</strong>. L’unité est l’euro, pas le pourcentage.</p>''',code=CUMUL,figure='02_cumul',alt='Ventes cumulées : 10 000, 22 000, 31 000, 46 000, 64 000 puis 80 500 euros.',comparison=True,reading='''<code>cumsum()</code> conserve une somme progressive dans l’ordre des lignes. Ici, les ventes sont toutes positives : le cumul augmente même quand le montant du mois diminue. Avec des montants nets négatifs, cette propriété ne serait plus garantie.''',
 exercise=ex('Auditer une conclusion','On lit : « Le cumul augmente en juin, donc les ventes de juin sont supérieures à celles de mai. » Corrigez cette phrase avec les trois montants utiles.','Une conclusion corrigée et les chiffres qui la prouvent.','16 500 € en juin contre 18 000 € en mai ; cumul de 80 500 €.',['Distinguez le montant du mois et celui depuis janvier.','Le cumul de mai vaut 64 000 €. Juin y ajoute 16 500 €.'],solution='print(df.loc[4:5, ["ventes", "ventes_cumulees"]])',answer='Le cumul passe de 64 000 à 80 500 € grâce aux ventes positives de juin. Les ventes mensuelles baissent pourtant de 18 000 à 16 500 €.')),
 dict(id='mobile',title='Moyenne mobile',text='''<h2>Lisser sans effacer les observations.</h2><p>Une moyenne mobile sur trois mois calcule la moyenne du mois courant et des deux précédents. Pour mars : (10 000 + 12 000 + 9 000) / 3 = <strong>10 333,33 €</strong>.</p>''',code=ROLL,figure='02_moyenne_mobile',alt='Ventes mensuelles et moyenne mobile sur trois mois ; lissage disponible à partir de mars.',reading='''<code>rolling(3).mean()</code> utilise trois lignes : elles correspondent ici à trois mois consécutifs. Par défaut, il faut trois valeurs ; les deux premiers résultats sont NaN. Deux appels à plot ajoutent deux séries au même Axes. <code>label</code> et <code>legend</code> les identifient ; les marqueurs et tirets complètent la couleur. Un lissage décrit le passé, ce n’est pas une prévision.''',
 exercise=ex('Vérifier la moyenne d’avril','Calculez la moyenne mobile d’avril à la main, puis vérifiez avec pandas. Expliquez pourquoi les deux premières valeurs ne doivent pas être remplacées par zéro.','Un calcul et une explication.','12 000 € : moyenne de février, mars et avril.',['La fenêtre se déplace avec le mois courant.','(12000 + 9000 + 15000) / 3.'],solution='print((12000 + 9000 + 15000) / 3)\nprint(df.loc[3, "moyenne_mobile"])',answer='Avril : 12 000 €. Janvier et février manquent d’historique pour une fenêtre complète. Zéro inventerait un niveau de ventes absent des données.')),
 dict(id='marge',title='Marge rapportée au CA',text='''<h2>Un ratio de sommes pour l’ensemble.</h2><p>Ici, profit est un montant fictif fourni par mois. Nous nommons précisément l’indicateur : <strong>profit / ventes</strong>, ou marge rapportée au chiffre d’affaires. Ce n’est pas une marge divisée par un coût d’achat.</p><p>En février : 3 000 / 12 000 × 100 = 25 %. Pour le semestre : somme des profits / somme des ventes × 100 = 18 350 / 80 500 × 100 ≈ <strong>22,80 %</strong>.</p>''',code=MARGIN,figure='02_marge',alt='Marge sur chiffre d’affaires : 20 %, 25 %, 20 %, 25 %, 25 %, 20 % selon le mois.',reading='''La division de colonnes calcule le taux de chaque mois. Le ratio des deux sommes calcule le taux global ; chaque mois y pèse selon son chiffre d’affaires. <code>mean()</code> sur les taux donne le même poids à chaque mois : la question traitée est différente.''',
 exercise=ex('Le taux depuis janvier','Calculez profit cumulé / ventes cumulées × 100, puis tracez cette série. Comparez son dernier point à la moyenne des taux mensuels. Justifiez la formule retenue pour la marge globale.','Une courbe, deux valeurs et une justification.','Dernier ratio ≈ 22,80 % ; moyenne des taux = 22,50 %.',['Appliquez cumsum() au numérateur et au dénominateur.','Réutilisez plot et les labels des exemples précédents.'],solution=MARGIN_CUM,answer='Le ratio cumulé final vaut environ 22,80 %, contre 22,50 % pour la moyenne simple des taux. Les mois n’ont pas le même chiffre d’affaires. Pour la marge globale sur CA, on divise les sommes, pas la somme des pourcentages.')),
 dict(id='synthese',title='Choisir et interpréter',text='''<h2>La question décide du calcul.</h2><p>La responsable demande si la baisse récente est compatible avec une bonne progression depuis janvier, et si le total de ventes révèle à lui seul la marge. Choisissez vos indicateurs avant d’ouvrir le graphique.</p>''',code='',reading='',
 exercise=ex('Une restitution en trois phrases','Choisissez deux graphiques déjà construits. Formulez un constat chiffré sur juin, un constat sur le semestre et une limite. Expliquez pourquoi un seul cumul ne répond pas à toutes les questions.','Deux graphiques du carnet et trois phrases.','Références et unités explicites ; pas de prévision ni de causalité inventée.',['Combinez variation mensuelle, évolution depuis janvier et marge globale.','Une courbe de ventes cumulées ne contient aucune information sur les coûts ou le profit.'],answer='Exemple : juin recule de 8,33 % sur mai tout en restant 65 % au-dessus de janvier. Le scénario totalise 80 500 € de ventes et une marge sur CA de 22,80 %. Ces six observations fictives ne permettent pas de prévoir le mois suivant ni d’expliquer les causes.')),
]

Q1=[
('Quel outil prépare les sommes par catégorie avant le tracé ?', ['pandas','Matplotlib automatiquement','Le fichier PNG','La légende'],0,'groupby et sum préparent les mesures. Matplotlib reçoit ensuite ces résultats.'),
('Quel graphique convient aux ventes quotidiennes ?', ['Une courbe dans l’ordre des dates','Des catégories triées alphabétiquement','Un camembert par ligne','Un histogramme de noms de jours'],0,'Les dates forment une chronologie. Une courbe permet d’en observer les variations.'),
('Que représente ax ?', ['Le CSV','Une zone de dessin dans la Figure','Le fichier exporté','Le total'],1,'Figure est le document ; Axes contient les marques, textes et axes d’une zone de graphique.'),
('Pourquoi trier une Series entière ?', ['Pour effacer les catégories','Pour obtenir un bénéfice','Pour garder les noms associés aux montants','Pour calculer des pourcentages'],2,'Trier seulement les valeurs peut attribuer les bons nombres aux mauvaises catégories.'),
('Une part de ventes de 25 % signifie…', ['Une hausse de 25 %','Un quart du total du périmètre choisi','Une marge de 25 %','25 commandes'],1,'Une part compare une composante à un ensemble défini, pas à une période précédente.'),
('Que comptent les hauteurs de notre histogramme ?', ['Les bénéfices','Les commandes distinctes','Les catégories','Les lignes de vente par intervalle de montant'],3,'Le grain utilisé est la ligne de vente : les 60 lignes ne sont pas 60 commandes.'),
('Quel rôle joue Seaborn ici ?', ['Remplacer le serveur PostgreSQL','Modifier le CSV','Tracer un histogramme dans un Axes Matplotlib','Calculer les coûts manquants'],2,'Seaborn s’appuie sur Matplotlib ; ax=ax permet de conserver nos réglages et notre export.'),
('Que vérifier avant de rendre le carnet ?', ['Seulement la couleur','Rejouer depuis un noyau neuf et contrôler les valeurs','Seulement le poids du PNG','Le nombre de cellules vides'],1,'Une image lisible peut être fausse. La reprise dans l’ordre et les contrôles chiffrés complètent la lecture visuelle.')]
Q2=[
('De 12 000 à 9 000 €, quelle variation ?', ['−3 %','−25 %','−10 %','+25 %'],1,'(9000 / 12000 − 1) × 100 = −25 %. La référence est le mois précédent.'),
('Mars vaut −10 % depuis janvier. Pourquoi ?', ['On additionne les variations','On divise par le cumul','On compare 9 000 à 10 000','On compare 9 000 à 12 000'],2,'La référence fixe est janvier, soit 10 000 €, et non février.'),
('Le cumul augmente en juin. Peut-on conclure que juin vend plus que mai ?', ['Oui, toujours','Oui, si le graphique est vert','Non : les ventes positives de juin ajoutent au cumul même si elles baissent','Non, car le cumul est un pourcentage'],2,'Juin ajoute 16 500 € au cumul mais reste sous les 18 000 € de mai.'),
('Quelle est la première moyenne mobile complète sur trois mois ?', ['0 € en janvier','10 333,33 € en mars','12 000 € en février','31 000 € en mars'],1,'(10000 + 12000 + 9000) / 3 = 10333,33 €. Les deux premières fenêtres sont incomplètes.'),
('Comment calculer la marge globale rapportée au CA ?', ['Moyenne simple des taux','Somme des taux','Profit de juin / ventes de janvier','Somme des profits / somme des ventes × 100'],3,'Le ratio des sommes tient compte des chiffres d’affaires différents ; il donne environ 22,80 % ici.'),
('Que faire de la première variation mensuelle NaN ?', ['La présenter comme non calculable faute de période précédente','L’afficher comme 0 % sans explication','La remplacer par 100 %','Supprimer toutes les ventes de janvier'],0,'Une référence absente ne signifie pas une variation nulle. Les ventes de janvier restent utiles aux autres indicateurs.'),
('Si avril manque, que signifie rolling(3) sur les lignes restantes ?', ['Toujours trois mois consécutifs','Trois lignes, pas forcément trois mois consécutifs','Une prévision','Un total annuel'],1,'Il faut vérifier le calendrier et le grain avant de donner un sens temporel à une fenêtre de lignes.'),
('Quel indicateur exprime les ventes de juin relativement à janvier ?', ['La somme cumulée en euros','La moyenne mobile','La part du total régional','L’évolution depuis janvier'],3,'Le rapport à une référence fixe répond à cette question : +65 % en juin.')]
FLASH1=[('Qui prépare, qui dessine ?', 'pandas prépare ; Matplotlib dessine ; Seaborn facilite certains graphiques statistiques.'),('Figure ou Axes ?', 'Figure est le document ; Axes est une zone de dessin.'),('Que conserve un tri correct ?', 'Chaque nom reste associé à sa valeur.'),('Que faut-il préciser pour une part ?', 'Le numérateur, le total du périmètre et l’unité en pourcentage.'),('Que compte notre histogramme ?', 'Des lignes de vente dans des intervalles de montants.'),('Comment vérifier un carnet ?', 'Contrôler les chiffres, redémarrer le noyau et tout exécuter.')]
FLASH2=[('Variation mensuelle : quelle référence ?', 'La valeur de la période précédente.'),('Évolution depuis janvier : quelle référence ?', 'La valeur fixe de janvier.'),('Somme cumulée : quelle unité ?', 'L’euro ici, puisque l’on additionne des ventes en euros.'),('rolling(3) : trois quoi ?', 'Trois lignes ; trois mois seulement si le calendrier est mensuel et complet.'),('Marge globale sur CA : quelle formule ?', 'Somme des profits divisée par somme des ventes, fois 100.'),('Peut-on prévoir avec une moyenne mobile ?', 'Ce lissage décrit les observations passées ; il ne constitue pas à lui seul une prévision.')]
BLOCKS=[dict(n=1,slug='01_graphiques_fiables',notebook='01_comprendre_graphiques',title='Comprendre et construire ses graphiques',hero='Observer.<br>Construire. <span>Expliquer.</span>',intro='Des rappels utiles, des exemples courts et des petits exercices à corriger ensemble.',lessons=B1,quiz=Q1,flash=FLASH1,setup=LOAD),dict(n=2,slug='02_indicateurs',notebook='02_indicateurs',title='Représenter les indicateurs de performance',hero='Calculer.<br>Représenter. <span>Interpréter.</span>',intro='Distinguer les indicateurs en les calculant, en les traçant et en les confrontant aux chiffres.',lessons=B2,quiz=Q2,flash=FLASH2,setup=MONTHS)]
