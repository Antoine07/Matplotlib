from pathlib import Path
from hashlib import sha256
from random import Random
import html, json
from discovery_content import DISCOVERY, build_discovery

ROOT = Path(__file__).resolve().parents[1]
DATA = """import pandas as pd
import matplotlib.pyplot as plt

DATA = '/workspace/data/sample_-_superstore.xls'
orders = pd.read_excel(DATA, sheet_name='Orders', engine='xlrd')
orders['Order Date'] = pd.to_datetime(orders['Order Date'])"""

PAGES = [
  dict(file='01_explorer', title='Explorer les commandes', group='Socle du matin',
       intro='Avant de tracer, identifier la ligne observée, vérifier les colonnes et comprendre ce que recouvre une commande.',
       question='Que représente une ligne du fichier, et combien de commandes distinctes contient-il ?',
       concepts=[('Le grain des données','Une ligne décrit une ligne de commande associant un produit, une quantité et un montant. Une commande peut occuper plusieurs lignes.','Cela évite de confondre nombre de lignes et nombre de commandes.'),('Vérifier avant de calculer','`shape`, `columns`, `nunique()` et `isna().sum()` décrivent la structure avant toute analyse.','Le contrôle rend visibles les colonnes disponibles, les identifiants distincts et les valeurs manquantes.')],
       example='''print('Dimensions :', orders.shape)
print('Commandes distinctes :', orders['Order ID'].nunique())
print('Années :', orders['Order Date'].dt.year.nunique())
print('Période :', orders['Order Date'].min(), '→', orders['Order Date'].max())
print(orders[['Region', 'Category', 'Sales', 'Profit']].isna().sum())''',
       reading='shape renvoie lignes et colonnes. nunique compte des identifiants distincts. dt.year extrait l’année d’une date pandas avant nunique. Le classeur Orders contient 10 194 lignes, 21 colonnes et 5 111 commandes distinctes réparties sur quatre années ; les dates couvrent 2023 à 2026 et les champs ne sont pas manquants.',
       exercises=[('Vérifier les catégories','Combien de régions, de catégories et d’années sont présentes ? Donnez les commandes pandas qui permettent de les compter.','Trois comptages et une phrase sur la différence entre lignes et commandes.','''print(orders['Region'].nunique())
print(orders['Category'].nunique())
print(orders['Order Date'].dt.year.nunique())''','4 régions, 3 catégories et 4 années. Une ligne de commande n’est pas une commande unique : Order ID se compte avec nunique().'),('Lire une ligne','Affichez les cinq premières lignes et nommez l’unité représentée par une ligne.','Une cellule de code et une phrase.','orders.head()','Chaque ligne est une ligne de commande, pas nécessairement une commande complète.')],
       errors=['Compter `len(orders)` comme nombre de commandes.','Interpréter une ligne comme un produit unique sans vérifier son grain.']),
  dict(file='02_comparer', title='Agréger et comparer', group='Socle du matin',
       intro='Pour comparer des catégories, calculer un total par catégorie avant de construire les barres.',
       question='Quelle région génère le plus de ventes dans ce jeu de données ?',
       concepts=[('Matplotlib, Figure et Axes','Matplotlib est une bibliothèque Python qui compose et exporte des figures statiques. Une Figure est le document ; un Axes est une zone de tracé.','Le couple `fig, ax` donne un contrôle précis sur titres, axes, tailles et exports. Matplotlib dessine les données préparées ; pandas calcule les agrégats.'),('Regrouper puis agréger','`groupby()` forme les groupes ; `sum()` additionne la mesure dans chaque groupe.','Le graphique compare alors des totaux de même nature.'),('Trier ensemble les étiquettes et les valeurs','`sort_values()` trie une Series en conservant son index.','Les noms de régions restent associés à leurs montants.')],
       example='''ca_categories = orders.groupby('Category')['Sales'].sum().sort_values()
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(ca_categories.index, ca_categories.values)
ax.set(title='Ventes par catégorie', xlabel='Ventes (unités monétaires)')
plt.show()''',
       reading='groupby(Category) définit les groupes. Sales est la mesure additionnée par sum(). sort_values() organise la Series entière. fig est le document ; ax est la zone de dessin. barh reçoit les étiquettes de l’index et les totaux. Les catégories totalisent 2 326 534,35 unités monétaires : Technology 839 893,28 ; Furniture 754 747,76 ; Office Supplies 731 893,31.',
       exercises=[('Comparer les régions','Construisez un graphique horizontal du total Sales par Region. Quelle région arrive en tête ?','Un graphique titré, une unité sur l’axe et deux phrases qui distinguent le constat de son explication.','''ca_regions = orders.groupby('Region')['Sales'].sum().sort_values()
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(ca_regions.index, ca_regions.values)
ax.set(title='Ventes par région', xlabel='Ventes (unités monétaires)')
plt.show()''','West arrive en tête avec 739 813,61. C’est un constat sur ce fichier ; le graphique seul n’explique pas pourquoi.'),('Auditer un tri','Corrigez l’association entre noms et totaux dans le code ci-dessous. Expliquez le risque d’un tri indépendant.','Code corrigé et une phrase.','''noms = ca_categories.index
valeurs = sorted(ca_categories.values)
# Corriger la préparation avant le tracé
''','Le tri doit conserver l’index et les valeurs dans la même Series. Ici sorted() seul sépare les étiquettes de leurs montants.')],
       errors=['Trier les montants seuls et garder les noms dans leur ordre initial.','Tracer les lignes brutes en les présentant comme des totaux par région.']),
  dict(file='03_rentabilite', title='Comparer ventes et profit', group='Socle du matin',
       intro='Un chiffre d’affaires élevé ne suffit pas à décrire le profit. Agréger ventes et profit, puis définir clairement le ratio observé.',
       question='Quelle catégorie associe ventes importantes et meilleur profit rapporté aux ventes ?',
       formula='''<h3>Profit rapporté aux ventes</h3><p><code>sommes(Profit) ÷ sommes(Sales) × 100</code>. Le numérateur et le dénominateur couvrent le même groupe et le même périmètre.</p><p>Pour Technology : <code>146 543,38 ÷ 839 893,28 × 100 ≈ 17,45 %</code>. Il s’agit du profit rapporté aux ventes du jeu, pas d’un taux de marge commerciale : le coût d’achat manque.</p>''',
       concepts=[('Profit fourni par le jeu','`Profit` est une valeur fournie par le fichier. Ses composantes de coûts ne sont pas détaillées ici.','On peut comparer Profit et Sales, sans reconstruire une marge comptable inconnue.'),('Profit rapporté aux ventes','Somme des profits / somme des ventes × 100. Ce cours nomme ce ratio « profit rapporté au CA ».','Le ratio des sommes pondère chaque ligne par son montant de ventes.'),('Trois termes à distinguer','Le taux de marge commerciale nécessite le coût d’achat ; le taux de marque rapporte la marge au CA. Ces deux bases ne sont pas fournies par Profit.','Employer le bon nom évite une interprétation comptable erronée.')],
       example='''bilan = orders.groupby('Category')[['Sales', 'Profit']].sum()
bilan['Profit_sur_Sales_pct'] = (
    bilan['Profit'].div(bilan['Sales'].replace(0, float('nan'))) * 100
)
print(bilan.round(2))''',
       reading='Les sommes sont calculées sur chaque catégorie avant la division. Le ratio global est 292 296,81 / 2 326 534,35 × 100 ≈ 12,56 %. Pour Technology : 146 543,38 / 839 893,28 × 100 ≈ 17,45 %. La moyenne simple des ratios par ligne est une autre mesure (12,22 % ici) et n’est pas le ratio global.',
       exercises=[('Comparer deux classements','Classez les catégories par Sales puis par Profit. Les classements sont-ils identiques ?','Les deux ordres et une observation sans explication causale.','''# Réutilisez bilan et classez séparément ses deux colonnes
''','Technology arrive première pour Sales et Profit ; le classement complet des profits place Office Supplies avant Furniture.'),('Représenter le ratio','Tracez Profit rapporté aux ventes par catégorie. Traitez explicitement un total Sales nul s’il se présente.','Un graphique avec unité en pourcentage et un commentaire sur le dénominateur.','''# Complétez bilan avec le ratio Profit / Sales * 100, puis tracez-le
''','Le dénominateur est la somme des ventes de la catégorie. Un total nul rend le ratio indéfini ; il ne faut pas le remplacer par 0 %.'),('Expliquer une moyenne trompeuse','Pourquoi la moyenne des ratios Profit/Sales par ligne ne remplace-t-elle pas le ratio des sommes ?','Une explication appuyée sur les deux calculs pandas.','''marge_ligne = orders['Profit'] / orders['Sales'] * 100
print('Moyenne des lignes :', marge_ligne.mean())
print('Ratio global :', orders['Profit'].sum() / orders['Sales'].sum() * 100)''','Les lignes n’ont pas le même montant de ventes. La moyenne simple leur donne le même poids ; le ratio des sommes pondère implicitement par Sales.')],
       errors=['Nommer Profit/Sales « taux de marge commerciale ».','Moyenner les taux ligne à ligne pour décrire le ratio global.','Transformer une division par zéro en taux nul.']),
  dict(file='04_temps_et_variations', title='Lire l’évolution mensuelle', group='Socle du matin',
       intro='Une série temporelle exige des dates réelles, un calendrier trié et une agrégation mensuelle avant le tracé.',
       question='Les ventes augmentent-elles à chaque mois de la période ?',
       formula='''<h3>Variation relative</h3><p><code>(valeur actuelle ÷ valeur précédente − 1) × 100</code>. <code>pct_change()</code> renvoie d’abord une proportion ; la multiplication par 100 l’exprime en pourcentage.</p><p>Exemple réel : février 2023 par rapport à janvier 2023 : <code>(4 519,89 ÷ 14 518,06 − 1) × 100 ≈ −68,87 %</code>. La variation en montant est <code>4 519,89 − 14 518,06 = −9 998,17</code> unités monétaires.</p>''',
       concepts=[('Agréger les dates par mois','`resample("MS")` forme des périodes mensuelles commençant au premier jour du mois.','L’axe représente ici des totaux mensuels, pas des lignes isolées.'),('Variation relative et variation en montant','`pct_change()` mesure la variation relative ; `diff()` mesure le changement absolu.','Une forte hausse en pourcentage n’est pas nécessairement le plus grand montant ajouté.')],
       example='''mensuel = (orders.set_index('Order Date')
                 .resample('MS')['Sales'].sum())
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(mensuel.index, mensuel.values, marker='o')
ax.set(title='Ventes mensuelles', ylabel='Ventes (unités monétaires)')
plt.show()''',
       reading='L’index datetime permet resample("MS") ; sum agrège les lignes de chaque mois. plot relie les périodes dans leur ordre. La série couvre 48 mois consécutifs. Les ventes mensuelles vont de 4 519,89 en février 2023 à 118 454,51 en novembre 2026.',
       exercises=[('Repérer deux mois','Retrouvez le mois au plus haut et celui au plus bas. Vérifiez l’ordre chronologique de la série.','Deux dates, deux montants et le code utilisé.','''print(mensuel.idxmax(), mensuel.max())
print(mensuel.idxmin(), mensuel.min())
print(mensuel.index.is_monotonic_increasing)''','Maximum : novembre 2026, 118 454,51 ; minimum : février 2023, 4 519,89. L’index est trié de façon croissante.'),('Comparer en montant et en pourcentage','Pour chaque mois, calculez la variation par rapport au mois précédent en montant et en pourcentage. Identifiez leurs plus fortes hausses.','Deux dates et deux mesures distinctes.','''variation_montant = mensuel.diff()
variation_pct = mensuel.pct_change() * 100
''','La variation en pourcentage compare au mois précédent et pct_change renvoie d’abord une fraction. La première période n’a pas de référence et reste NaN.')],
       errors=['Tracer les données sans les trier chronologiquement.','Confondre évolution relative et montant ajouté.','Lire le premier NaN comme une variation nulle.']),
  dict(file='05_cumuls', title='Approfondir les cumuls', group='Après le socle · autonome',
       intro='Ces techniques prolongent le parcours, mais ne sont pas des prérequis du TP de l’après-midi.',
       question='Que signifie une courbe cumulée quand les ventes mensuelles baissent ?',
       formula='''<h3>Trois calculs différents</h3><ul><li>Somme cumulée : <code>Σ Salesₜ</code>, unité monétaire.</li><li>Évolution à base fixe : <code>(Salesₜ ÷ Sales₀ − 1) × 100</code>, référence fixe.</li><li>Profit cumulé rapporté au CA cumulé : <code>Σ Profitₜ ÷ Σ Salesₜ × 100</code>, ratio pondéré par les ventes.</li></ul><p>Pour les cumuls, choisissez un début de période commun aux ventes et au profit. Pour une évolution à base fixe, choisissez le mois de référence et conservez-le dans chaque comparaison.</p>''',
       concepts=[('Somme cumulée des ventes','`cumsum()` additionne les périodes successives.','Un cumul de ventes positives peut progresser pendant une baisse mensuelle.'),('Évolution depuis une référence fixe','(valeur actuelle / valeur de référence − 1) × 100.','La référence est fixe ; cette mesure ne somme pas les variations.'),('Marge cumulée sur CA','Somme des profits jusqu’au mois / somme des ventes jusqu’au mois × 100.','On ne somme ni ne moyenne les taux mensuels pour obtenir ce ratio.'),('Moyenne mobile','`rolling(3, min_periods=3).mean()` calcule la moyenne des trois dernières lignes à partir de trois observations.','Elle lisse les fluctuations passées ; ce n’est pas une prévision.')],
       example='''m = orders.set_index('Order Date').resample('MS')[['Sales', 'Profit']].sum()
m['Sales_cumulees'] = m['Sales'].cumsum()
m['Sales_moyenne_mobile_3'] = m['Sales'].rolling(3, min_periods=3).mean()
m['Profit_cumule'] = m['Profit'].cumsum()
m['Profit_sur_Sales_cumule_pct'] = (
    m['Profit_cumule'].div(m['Sales_cumulees'].replace(0, float('nan'))) * 100
)''',
       reading='cumsum conserve une somme progressive ; le cumul final des ventes est égal au total du fichier, 2 326 534,35. rolling(3) utilise trois lignes ; avec un calendrier mensuel complet, il s’agit de trois mois. Les deux premiers mois ne disposent pas de trois observations. Le ratio cumulé divise le profit cumulé par les ventes cumulées au même mois.',
       exercises=[('Vérifier le cumul final','Comparez le dernier cumul au total Sales du fichier.','Deux valeurs et une phrase expliquant le grain temporel.','''# Comparez le dernier cumul au total des ventes''','Les deux montants sont égaux : le dernier cumul additionne l’ensemble des ventes mensuelles agrégées.'),('Comparer deux taux cumulés','Avec les deux mois fictifs CA 100/profit 10 puis CA 300/profit 90, comparez le ratio des sommes et la moyenne des taux mensuels.','Les deux calculs et une phrase qui justifie le ratio global.','''# Comparez les deux méthodes sur les données fictives''','Le ratio des sommes est 25 % ; la moyenne simple est 20 %. Les deux mois ont des CA différents, donc la moyenne simple attribue un poids inadapté au ratio global.'),('Contrôler une moyenne mobile','Calculez à la main la moyenne des ventes de janvier à mars 2023. Comparez avec rolling(3) et expliquez les deux premières valeurs manquantes.','Un calcul manuel, la valeur pandas et une phrase.','''# Vérifiez une fenêtre de trois mois consécutifs''','La moyenne utilise janvier, février et mars. La série commence par deux valeurs NaN car aucune fenêtre complète de trois mois n’est encore disponible.'),('Ne pas additionner les variations','Comparez l’évolution du premier au dernier mois à la somme des variations mensuelles en pourcentage. Pourquoi diffèrent-elles ?','Les deux valeurs et une explication sur la référence.','''# Comparez évolution à base fixe et somme des variations''','L’évolution à base fixe compare les deux montants extrêmes. Les variations successives ont des dénominateurs différents et ne s’additionnent généralement pas.')],
       errors=['Confondre cumul des montants et cumul des pourcentages.','Prendre la moyenne des taux comme ratio global.']),
  dict(file='06_distributions', title='Explorer les distributions', group='Après le socle · autonome',
       intro='Comparer des moyennes ne décrit pas l’étalement ni les valeurs atypiques. Le boxplot complète les indicateurs, sans remplacer l’analyse du grain.',
       question='Deux catégories aux profits moyens proches ont-elles les mêmes profits par ligne ?',
       concepts=[('Boîte à moustaches','La boîte montre les quartiles et la médiane ; les points au-delà des moustaches sont affichés séparément.','On observe dispersion, asymétrie et valeurs atypiques.'),('Respecter le grain','Ici, une observation est le profit d’une ligne de commande.','Pour analyser les commandes, agréger par Order ID avant de tracer.')],
       example='''categories = sorted(orders['Category'].dropna().unique())
series = [orders.loc[orders['Category'].eq(c), 'Profit'].dropna()
          for c in categories]
fig, ax = plt.subplots(figsize=(9, 4))
ax.boxplot(series, tick_labels=categories, showfliers=True)
ax.axhline(0, color='black', linewidth=1)
ax.set(title='Profit par ligne de commande', ylabel='Profit (unités monétaires)')
plt.show()''',
       reading='Chaque boîte résume la distribution des profits de lignes d’une catégorie. La ligne horizontale à zéro distingue profits positifs et négatifs. Le jeu contient des profits de ligne négatifs ; un boxplot ne les convertit pas en pertes par commande.',
       exercises=[('Décrire une boîte','Choisissez une catégorie. Comparez médiane, intervalle interquartile et présence de pertes.','Trois constats visibles et une phrase sur le grain.','''# Décrivez une boîte à partir du graphique de l’exemple
''','Le graphique résume le profit par ligne. Ne pas généraliser ses points atypiques à des commandes entières.'),('Changer le grain','Agrégez Profit par Order ID avant de comparer les distributions. Que change le graphique ?','Un second boxplot et une comparaison de deux phrases.','''profit_commande = orders.groupby('Order ID')['Profit'].sum()
# Tracer la distribution des profits agrégés par commande
''','L’agrégation crée une observation par commande ; pertes et dispersion peuvent alors différer des lignes individuelles.')],
       errors=['Lire la médiane comme une moyenne.','Présenter une ligne de commande comme une commande entière.'])
]

# Le premier bloc sert de modèle pédagogique : exemple, exercice, puis mise en
# commun pour chaque notion. Le graphique compare deux comptages au même grain.
PAGES[0]['concepts'] = [
    ('Matplotlib et Seaborn', 'Matplotlib est une bibliothèque Python pour créer des graphiques. Seaborn s’appuie sur Matplotlib et propose des outils de visualisation statistique. Dans ce parcours, nous préparons les données avec pandas et dessinons avec Matplotlib.', 'Un graphique dépend autant de la question et de la préparation des données que de la bibliothèque choisie.'),
    ('Le grain des données', 'Une ligne de Orders décrit une ligne de commande. Une commande peut donc occuper plusieurs lignes.', 'Le nombre de lignes et le nombre de commandes répondent à deux questions différentes.'),
    ('La Figure et les Axes', 'Une Figure contient le graphique ; un objet Axes porte le tracé, son titre et ses axes. `plt.subplots()` crée les deux.', 'Le couple `fig, ax` permet de construire et régler un graphique de façon explicite.'),
]
PAGES[0]['sequences'] = [
    dict(
        title='Compter les lignes et les commandes',
        example="""print('Lignes :', len(orders))
print('Commandes distinctes :', orders['Order ID'].nunique())""",
        reading='len compte les lignes du tableau. nunique compte les identifiants Order ID différents. Ici, 10 194 lignes correspondent à 5 111 commandes distinctes.',
        exercise_title='Compter les catégories',
        prompt='Combien de catégories différentes contient la feuille Orders ?',
        deliverable='Une valeur et la commande pandas utilisée.',
        solution="print(orders['Category'].nunique())",
        answer='La feuille contient trois catégories distinctes.',
    ),
    dict(
        title='Comparer deux comptages par catégorie',
        example="""par_categorie = orders.groupby('Category').agg(
    lignes=('Order ID', 'size'),
    commandes=('Order ID', 'nunique')
).sort_values('lignes')

fig, ax = plt.subplots(figsize=(8, 4))
positions = range(len(par_categorie))
hauteur = 0.36
ax.barh([p - hauteur / 2 for p in positions], par_categorie['lignes'],
        height=hauteur, label='Lignes de commande')
ax.barh([p + hauteur / 2 for p in positions], par_categorie['commandes'],
        height=hauteur, label='Commandes distinctes')
ax.set_yticks(list(positions), par_categorie.index)
ax.set(title='Lignes et commandes distinctes par catégorie',
       xlabel='Nombre')
ax.legend()
plt.show()""",
        reading='Chaque paire de barres compare, pour une catégorie, le nombre de lignes et le nombre d’identifiants Order ID distincts. Une même commande peut contenir des produits de plusieurs catégories : elle peut donc être comptée une fois dans chacune de ces catégories.',
        exercise_title='Lire les commandes distinctes',
        prompt='Quelle catégorie compte le plus de commandes distinctes ? Vérifiez votre réponse avec pandas.',
        deliverable='Un nom de catégorie et le calcul utilisé pour le vérifier.',
        solution="commandes_par_categorie = orders.groupby('Category')['Order ID'].nunique()\nprint(commandes_par_categorie.idxmax())",
        answer='Office Supplies compte le plus de commandes distinctes par catégorie : 3 812. Le comptage se fait séparément dans chaque catégorie.',
    ),
]
PAGES[0]['exercises'] = [
    (s['exercise_title'], s['prompt'], s['deliverable'], '', s['answer'])
    for s in PAGES[0]['sequences']
]

# Figures SVG rendues dans les supports HTML : elles utilisent les agrégats du
# classeur Orders vérifiés dans VALIDATION.md. Les cellules restent exécutables
# dans le notebook étudiant et produisent leurs propres figures Matplotlib.
CATEGORY_SALES = {'Furniture': 754747.76, 'Office Supplies': 731893.31, 'Technology': 839893.28}
CATEGORY_PROFIT = {'Furniture': 19730.00, 'Office Supplies': 126023.43, 'Technology': 146543.38}
REGION_SALES = {'Central': 503170.67, 'East': 691828.17, 'South': 391721.91, 'West': 739813.61}
REGION_PROFIT = {'Central': 39865.31, 'East': 94883.26, 'South': 46749.43, 'West': 110798.80}
SUBCATEGORY_SALES = {
 'Accessories':167380.32,'Appliances':108213.18,'Art':27659.01,'Binders':207354.90,
 'Bookcases':115361.20,'Chairs':335768.20,'Copiers':150745.30,'Envelopes':16528.36,
 'Fasteners':8532.24,'Furnishings':95598.13,'Labels':12695.04,'Machines':189925.00,
 'Paper':79540.54,'Phones':331842.60,'Storage':224644.60,'Supplies':46725.50,'Tables':208020.20}
SUBCATEGORY_PROFIT = {
 'Accessories':41936.64,'Appliances':18329.48,'Art':6653.20,'Binders':31426.10,
 'Bookcases':-3632.07,'Chairs':27223.53,'Copiers':56093.94,'Envelopes':6988.03,
 'Fasteners':2428.64,'Furnishings':13891.74,'Labels':5572.78,'Machines':3461.98,
 'Paper':34511.51,'Phones':45050.83,'Storage':21285.11,'Supplies':-1171.40,'Tables':-17753.21}
MONTH_LABELS = ['Jan 23','Fév 23','Mar 23','Avr 23','Mai 23','Juin 23','Juil 23','Août 23','Sep 23','Oct 23','Nov 23','Déc 23',
 'Jan 24','Fév 24','Mar 24','Avr 24','Mai 24','Juin 24','Juil 24','Août 24','Sep 24','Oct 24','Nov 24','Déc 24',
 'Jan 25','Fév 25','Mar 25','Avr 25','Mai 25','Juin 25','Juil 25','Août 25','Sep 25','Oct 25','Nov 25','Déc 25',
 'Jan 26','Fév 26','Mar 26','Avr 26','Mai 26','Juin 26','Juil 26','Août 26','Sep 26','Oct 26','Nov 26','Déc 26']
MONTH_SALES = [14518.05,4519.89,56933.91,28295.34,26319.77,34669.48,33946.39,28918.34,82670.43,32413.34,78826.96,72008.31,
 18461.92,11951.41,39978.63,34195.21,30246.95,24797.29,28765.32,37057.00,64627.05,31407.13,75972.56,75532.56,
 18830.33,22978.82,53031.07,38829.16,57042.84,40937.15,40300.50,31716.81,73521.66,59831.00,79411.97,97502.28,
 44259.21,20301.13,60728.48,36779.04,45155.48,53056.08,45989.50,64129.76,88064.53,83474.78,118454.51,85175.03]
MONTH_PROFIT = [2539.39,862.31,693.45,3488.84,3196.39,4999.76,-841.48,5765.23,8593.63,3469.18,9362.96,9554.66,
 -3189.80,2813.85,9930.61,4187.50,4677.14,3335.56,3288.65,5371.63,8220.03,2817.97,12474.79,8093.06,
 2916.02,5004.58,3707.89,2991.66,8676.70,4926.32,4559.88,2317.50,9370.10,16256.84,4011.41,17926.30,
 7231.64,1613.87,15013.09,957.53,6299.81,8246.57,7006.50,9488.07,11050.80,10670.53,9692.10,8655.83]

def _num(value, decimals=0):
    rendered=f'{value:,.{decimals}f}'
    return rendered.replace(',', ' ').replace('.', ',')

def _svg_start(title, width, height):
    return [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title, quote=True)}" xmlns="http://www.w3.org/2000/svg"><title>{html.escape(title)}</title>',
            '<style>text{font-family:Arial,sans-serif;fill:#263a34}.axis{stroke:#ccd5ca;stroke-width:1}.bar{fill:#719276}.bar2{fill:#b69ad9}.positive{fill:#719276}.negative{fill:#d48669}.line{fill:none;stroke:#527a61;stroke-width:3}.line2{fill:none;stroke:#8b70b3;stroke-width:3}.grid{stroke:#e7ebe3;stroke-width:1}</style>',
            f'<rect width="{width}" height="{height}" rx="14" fill="#fff"/><text x="20" y="28" font-size="15" font-weight="700">{html.escape(title)}</text>']

def svg_hbars(title, values, unit=''):
    items=sorted(values.items(), key=lambda item:item[1], reverse=True)
    width=790; top=52; row=34; height=top+row*len(items)+38; left=185; plot=500
    vmax=max([abs(v) for _,v in items] or [1]) or 1
    out=_svg_start(title,width,height)
    for i,(label,value) in enumerate(items):
        y=top+i*row
        out.append(f'<text x="{left-12}" y="{y+18}" text-anchor="end" font-size="12">{html.escape(str(label))}</text>')
        out.append(f'<rect class="bar" x="{left}" y="{y+3}" width="{plot*max(value,0)/vmax:.2f}" height="22" rx="4"/>')
        out.append(f'<text x="{left+plot*max(value,0)/vmax+7:.2f}" y="{y+19}" font-size="11">{_num(value,0)} {html.escape(unit)}</text>')
    out.extend([f'<line class="axis" x1="{left}" y1="{top+row*len(items)+4}" x2="{left+plot}" y2="{top+row*len(items)+4}"/>','</svg>'])
    return ''.join(out)

def svg_diverging(title, values, unit=''):
    items=sorted(values.items(), key=lambda item:item[1], reverse=True); width=820; left=190; plot=540; top=50; row=31; height=top+row*len(items)+32
    bound=max([abs(v) for _,v in items] or [1]) or 1; zero=left+plot/2
    out=_svg_start(title,width,height); out.append(f'<line class="axis" x1="{zero}" y1="{top-4}" x2="{zero}" y2="{top+row*len(items)}"/>')
    for i,(label,value) in enumerate(items):
        y=top+i*row; barw=plot/2*abs(value)/bound; x=zero if value>=0 else zero-barw; cls='positive' if value>=0 else 'negative'
        out.append(f'<text x="{left-12}" y="{y+17}" text-anchor="end" font-size="11">{html.escape(str(label))}</text><rect class="{cls}" x="{x:.1f}" y="{y+2}" width="{barw:.1f}" height="20" rx="3"/><text x="{zero+plot/2+8}" y="{y+17}" font-size="10">{_num(value,1)} {html.escape(unit)}</text>')
    out.append('</svg>'); return ''.join(out)

def svg_grouped(title, series, unit='%', palette=None, reverse_rows=False):
    labels=list(reversed(list(next(iter(series.values())).keys()))); width=790; left=190; plot=500; top=54; row=46; height=top+row*len(labels)+30
    all_values=[v for vals in series.values() for v in vals.values()]
    vmin=min(0,min(all_values)); vmax=max(0,max(all_values)); span=(vmax-vmin) or 1; zero=left+plot*(-vmin)/span
    out=_svg_start(title,width,height)
    if palette:
        out.insert(1, f'<style>.bar{{fill:{palette[0]}}}.bar2{{fill:{palette[1]}}}</style>')
    out.append(f'<line class="axis" x1="{zero:.1f}" y1="{top-6}" x2="{zero:.1f}" y2="{top+row*len(labels)}"/>')
    for j,(name,color) in enumerate(zip(series,('bar','bar2'))):
        out.append(f'<rect class="{color}" x="{left+j*135}" y="{height-20}" width="12" height="12" rx="2"/><text x="{left+17+j*135}" y="{height-10}" font-size="10">{html.escape(name)}</text>')
    for i,label in enumerate(labels):
        y=top+i*row; out.append(f'<text x="{left-12}" y="{y+26}" text-anchor="end" font-size="12">{html.escape(str(label))}</text>')
        for j,(name,vals) in enumerate(series.items()):
            value=vals[label]; barw=plot*abs(value)/span; color='bar' if j==0 else 'bar2'; yy=y+((1-j) if reverse_rows else j)*18
            x=zero if value>=0 else zero-barw
            label_x=x+barw+5 if value>=0 else x-5
            anchor='start' if value>=0 else 'end'
            out.append(f'<rect class="{color}" x="{x:.1f}" y="{yy}" width="{barw:.1f}" height="13" rx="3"/><text x="{label_x:.1f}" y="{yy+11}" text-anchor="{anchor}" font-size="9">{_num(value,1)} {unit}</text>')
    out.append('</svg>'); return ''.join(out)

def svg_lines(title, series, unit=''):
    labels=MONTH_LABELS; width=900; height=310; left=58; right=18; top=50; bottom=48; plotw=width-left-right; ploth=height-top-bottom
    vals=[v for arr in series.values() for v in arr if v is not None]; lo=min(vals); hi=max(vals); span=(hi-lo) or 1; out=_svg_start(title,width,height)
    for k in range(5):
        y=top+ploth*k/4; value=hi-span*k/4
        out.append(f'<line class="grid" x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}"/><text x="{left-6}" y="{y+4:.1f}" text-anchor="end" font-size="9">{_num(value,0)}</text>')
    for j,(name,arr) in enumerate(series.items()):
        points=[]
        for i,val in enumerate(arr):
            if val is None: continue
            x=left+plotw*i/(len(arr)-1); y=top+ploth*(hi-val)/span; points.append(f'{x:.1f},{y:.1f}')
        out.append(f'<polyline class="{"line" if j==0 else "line2"}" points="{" ".join(points)}"/>')
        out.append(f'<text x="{left+j*120}" y="{height-8}" font-size="10" fill="{"#527a61" if j==0 else "#8b70b3"}">● {html.escape(name)}</text>')
    for i in range(0,48,6):
        x=left+plotw*i/47; out.append(f'<text x="{x:.1f}" y="{height-bottom+18}" text-anchor="middle" font-size="9">{labels[i]}</text>')
    out.append(f'<text x="12" y="{top+5}" font-size="9">{html.escape(unit)}</text></svg>'); return ''.join(out)

def svg_month_bars(title, values, unit=''):
    width=900; height=300; left=48; right=16; top=52; bottom=48; plotw=width-left-right; ploth=height-top-bottom
    lo=min(0,min(values)); hi=max(0,max(values)); span=hi-lo or 1; zero=top+ploth*hi/span
    out=_svg_start(title,width,height)
    for k in range(5):
        value=hi-(hi-lo)*k/4; y=top+ploth*k/4
        out.append(f'<line class="grid" x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}"/><text x="{left-5}" y="{y+3:.1f}" text-anchor="end" font-size="8">{_num(value,0)}</text>')
    gap=plotw/len(values); barw=max(2,gap*.68)
    for i,value in enumerate(values):
        x=left+i*gap+(gap-barw)/2; y=top+ploth*(hi-max(0,value))/span; h=ploth*abs(value)/span
        out.append(f'<rect class="{"positive" if value>=0 else "negative"}" x="{x:.1f}" y="{y:.1f}" width="{barw:.1f}" height="{max(h,1):.1f}"/>')
    tick_step=max(1,len(values)//8)
    tick_labels=MONTH_LABELS[1:] if len(values)==47 else MONTH_LABELS[:len(values)]
    for i in range(0,len(values),tick_step):
        x=left+plotw*i/max(len(values)-1,1); out.append(f'<text x="{x:.1f}" y="{height-14}" text-anchor="middle" font-size="9">{tick_labels[i]}</text>')
    out.append(f'<line class="axis" x1="{left}" y1="{zero:.1f}" x2="{width-right}" y2="{zero:.1f}"/><text x="12" y="{top+5}" font-size="9">{html.escape(unit)}</text></svg>'); return ''.join(out)

def svg_boxplot(title, summaries):
    width=850; height=250; left=180; plot=620; top=70; row=48
    allvals=[v for vals in summaries.values() for v in vals]; lo=min(allvals); hi=max(allvals); span=hi-lo or 1; out=_svg_start(title,width,height)
    x=lambda v:left+plot*(v-lo)/span
    for i,(label,(mn,q1,med,q3,mx)) in enumerate(reversed(list(summaries.items()))):
        y=top+i*row; out.append(f'<text x="{left-12}" y="{y+5}" text-anchor="end" font-size="12">{html.escape(label)}</text><line class="axis" x1="{x(mn):.1f}" y1="{y}" x2="{x(mx):.1f}" y2="{y}"/><rect class="bar2" x="{x(q1):.1f}" y="{y-11}" width="{max(x(q3)-x(q1),2):.1f}" height="22" rx="3"/><line stroke="#263a34" stroke-width="2" x1="{x(med):.1f}" y1="{y-12}" x2="{x(med):.1f}" y2="{y+12}"/><circle cx="{x(mn):.1f}" cy="{y}" r="3" fill="#527a61"/><circle cx="{x(mx):.1f}" cy="{y}" r="3" fill="#527a61"/>')
    out.append('</svg>'); return ''.join(out)

def chart_html(spec):
    kind=spec['kind']; title=spec['title']
    if kind=='hbar': svg=svg_hbars(title,spec['values'],spec.get('unit',''))
    elif kind=='diverging': svg=svg_diverging(title,spec['values'],spec.get('unit',''))
    elif kind=='grouped': svg=svg_grouped(title,spec['series'],spec.get('unit','%'),spec.get('palette'),spec.get('reverse_rows',False))
    elif kind=='line': svg=svg_lines(title,spec['series'],spec.get('unit',''))
    elif kind=='monthbar': svg=svg_month_bars(title,spec['values'],spec.get('unit',''))
    elif kind=='box': svg=svg_boxplot(title,spec['summaries'])
    else: return ''
    return f'<figure class="course-graphic">{svg}<figcaption>{html.escape(spec["caption"])}</figcaption></figure>'

from tp_content import TP

QUIZZES = {
 'reactivation_00': ('Réactivation — premiers repères Pandas et Matplotlib', [
  ('Quel objet Pandas organise des données en lignes et colonnes ?', ['DataFrame','Figure','Axes','Liste de fichiers'],0,'Un DataFrame est un tableau de données composé de lignes et de colonnes.'),
  ('Quel type d’objet renvoie df["ventes"] ?', ['Une Series','Un DataFrame à deux colonnes','Une Figure','Une liste Python'],0,'Sélectionner une colonne avec df["ventes"] renvoie une Series : une suite de valeurs associées à un index.'),
  ('Quel type d’objet renvoie df[["ventes", "profit"]] ?', ['Un DataFrame contenant les deux colonnes','Une Series contenant la somme des deux colonnes','Un dictionnaire Python','Deux graphiques Matplotlib'],0,'La sélection avec une liste de colonnes conserve un tableau à deux dimensions : un DataFrame. Elle ne calcule ni somme ni graphique.'),
  ('Que renvoie df.head() par défaut ?', ['Les premières lignes','Les dernières colonnes','Le nombre de valeurs distinctes','Un graphique'],0,'head() affiche les cinq premières lignes par défaut.'),
  ('Que calcule len(df) ?', ['Le nombre de lignes','Le nombre de colonnes','La somme d’une colonne','Le nombre de valeurs uniques'],0,'len(df) compte les lignes du DataFrame.'),
  ('Que calcule df["ville"].nunique() ?', ['Le nombre de valeurs distinctes de ville','Le nombre total de lignes','La moyenne des villes','Le nombre de colonnes'],0,'nunique() compte les valeurs distinctes présentes dans la colonne.'),
  ('Quel appel additionne les valeurs de la colonne ventes ?', ['df["ventes"].sum()','df["ventes"].head()','df.sum("ventes")','df["ventes"].plot()'],0,'sum() additionne les valeurs de la Series sélectionnée.'),
  ('À quoi sert groupby("categorie") ?', ['À former des groupes par catégorie','À ouvrir un fichier','À supprimer une colonne','À dessiner un histogramme'],0,'groupby() permet ensuite de calculer une mesure séparément dans chaque groupe.'),
  ('Que calcule df.groupby(["Region", "Category"])["Sales"].sum() ?', ['Un total Sales pour chaque couple région-catégorie','Un total Sales par région seulement','Un total Sales par catégorie seulement','Deux totaux indépendants, l’un par région et l’autre par catégorie'],0,'La liste de deux champs forme un groupe pour chaque combinaison région-catégorie présente dans les données. sum() additionne ensuite Sales à l’intérieur de chaque groupe.'),
  ('Quelle bibliothèque fournit pyplot pour tracer des graphiques ?', ['Matplotlib','Pandas','NumPy uniquement','Jupyter'],0,'matplotlib.pyplot fournit les fonctions courantes de création de graphiques.'),
  ('Dans fig, ax = plt.subplots(), que représente ax ?', ['La zone de tracé','Le tableau de données','Le nom du fichier','Le total calculé'],0,'ax désigne l’Axes où l’on dessine le graphique.'),
  ('Dans figsize=(8, 4), quelle unité utilisent les valeurs 8 et 4 ?', ['Les pouces','Les pixels','Les centimètres','Les points typographiques'],0,'figsize indique la largeur et la hauteur de la figure en pouces. La conversion en pixels dépend du nombre de points par pouce, ou DPI.'),
  ('À 100 DPI, quelles sont les dimensions d’une figure figsize=(8, 4) ?', ['800 × 400 pixels','80 × 40 pixels','8 × 4 pixels','400 × 800 pixels'],0,'Multipliez chaque dimension en pouces par le DPI : 8 × 100 = 800 pixels de large et 4 × 100 = 400 pixels de haut. Le rendu affiché dans Jupyter peut être redimensionné.'),
  ('D’après les repères du cours, quel figsize est proposé pour un graphique détaillé ?', ['(12, 6)','(5, 3)','(3, 5)','(4, 4)'],0,'Le repère proposé pour un graphique détaillé est figsize=(12, 6), soit 1 200 × 600 pixels à 100 DPI. Il laisse davantage de place aux libellés et aux éléments du graphique ; la taille reste à adapter au contenu.'),
  ('Quel graphique compare des montants entre catégories ?', ['Un graphique à barres','Une courbe chronologique','Un tableau de dates seulement','Un nuage de points sans variables'],0,'Les barres facilitent la comparaison de valeurs entre catégories.'),
  ('Que faut-il ajouter pour rendre un graphique plus lisible ?', ['Un titre et des libellés d’axes','Des lignes supplémentaires au hasard','Un second jeu de données obligatoire','Une légende même sans séries'],0,'Le titre et les libellés d’axes expliquent ce qui est représenté et dans quelle unité.')]),
 'qcm_comparaisons': ('Vérifier les agrégations et les graphiques de comparaison', [
  ('Que renvoie groupby("Category")["Sales"].sum() ?', ['Un total Sales par catégorie','Une ligne par commande','Une moyenne par région','Un graphique'],0,'groupby forme les groupes et sum additionne Sales dans chaque catégorie.'),
  ('Dans une Series agrégée, que contient index ?', ['Les étiquettes des catégories','Les montants uniquement','Les valeurs manquantes','Les titres du graphique'],0,'index conserve les étiquettes associées à chaque valeur.'),
  ('Quel est l’intérêt de trier une Series avec sort_values() ?', ['Trier les montants en gardant leurs étiquettes liées','Trier uniquement les étiquettes','Convertir les ventes en pourcentage','Supprimer les petites catégories'],0,'Le tri de la Series garde ensemble les valeurs et leur index.'),
  ('Comment calculer la part des ventes d’une catégorie ?', ['Ventes de la catégorie / ventes totales × 100','Ventes totales / nombre de régions','Profit de la catégorie / ventes de la catégorie','Nombre de lignes / commandes'],0,'Le numérateur et le dénominateur portent sur Sales et le même périmètre.'),
  ('À quoi doivent s’additionner les parts de toutes les catégories ?', ['100 %','Le total des lignes','Le profit total','Le nombre de commandes'],0,'Les parts de catégories couvrent le total complet des ventes, donc leur somme vaut 100 % à l’arrondi près.'),
  ('Pourquoi comparer les parts de Sales et de Profit ?', ['Les deux mesures ont des échelles différentes','Les parts suppriment les catégories','Profit est une date','Sales ne peut pas être additionné'],0,'Rapporter chaque mesure à son propre total permet de comparer les contributions relatives.')]),
 'qcm_marges': ('Vérifier les agrégations et les ratios', [
  ('Quel calcul décrit le profit rapporté aux ventes global ?', ['sum(Profit) / sum(Sales) × 100','mean(Profit / Sales) × 100','sum(Profit / Sales)','sum(Sales) / sum(Profit)'],0,'Le ratio des sommes répond à la question du profit total rapporté aux ventes totales.'),
  ('Quelle colonne contient le profit dans ce fichier ?', ['Profit','La différence connue entre CA et coût d’achat','Discount seulement','Aucune'],0,'Profit est fourni par le classeur. Ses coûts constitutifs ne sont pas détaillés.'),
  ('Quelle base manque pour le taux de marge commerciale ?', ['Le coût d’achat','Le nombre de régions','La date de commande','La catégorie'],0,'Le taux de marge commerciale rapporte la marge commerciale au coût d’achat ; cette base n’est pas fournie par Sales et Profit.'),
  ('Que devient un ratio lorsque Sales total vaut zéro ?', ['Indéfini','Toujours 0 %','Toujours 100 %','Identique à Profit'],0,'Une division par zéro ne définit pas un taux ; la présenter comme 0 % inventerait une information.'),
  ('Pourquoi la moyenne des taux par ligne peut-elle différer du ratio global ?', ['Les lignes ont des ventes de tailles différentes','Les catégories sont alphabétiques','Sales est une date','Profit ne peut jamais être négatif'],0,'La moyenne simple donne le même poids aux lignes, alors que le ratio des sommes pondère selon les ventes.'),
  ('Comment préserver les étiquettes en triant une Series ?', ['sort_values() sur la Series','sorted(values) séparément','Inverser les seuls labels','Trier par ordre de saisie'],0,'Le tri de la Series conserve l’association entre son index et ses valeurs.')]),
 'qcm_synthese': ('Vérifier les acquis avant le TP', [
  ('Que mesure pct_change() × 100 ?', ['Variation relative en pourcentage','Différence en unités monétaires','Somme cumulée','Moyenne des valeurs'],0,'pct_change renvoie une proportion ; multiplier par 100 l’affiche en pourcentage.'),
  ('Pourquoi janvier peut-il être NaN après pct_change ?', ['Pas de période antérieure','Les ventes sont forcément nulles','Les dates ne sont pas numériques','nunique manque'],0,'La première ligne n’a aucune valeur précédente servant de référence.'),
  ('Quel calcul mesure le montant ajouté par rapport au mois précédent ?', ['diff()','pct_change()','nunique()','cumsum()'],0,'diff soustrait la valeur précédente ; pct_change rapporte cette différence à la valeur précédente.'),
  ('Que faut-il vérifier avant resample("MS") ?', ['Un index datetime','Des catégories triées','Un total égal à zéro','Aucune valeur Profit'],0,'resample opère sur un index temporel adapté ; convertir et vérifier les dates avant.'),
  ('Que prouve une hausse mensuelle ?', ['Une observation, pas sa cause','Une saisonnalité certaine','Une prévision','Une hausse du profit'],0,'Les données montrent une évolution observée, pas la cause ni le profit si seul Sales est tracé.'),
  ('Le TP exige-t-il rolling ou boxplot ?', ['Non, ce sont des approfondissements','Oui, dans chaque figure','Oui, pour le ratio global','Seulement pour charger le fichier'],0,'Le TP mobilise les notions du socle du matin ; les approfondissements sont facultatifs.')]),
 'qcm_avance': ('Vérifier les approfondissements', [
  ('Que mesure Sales.cumsum() ?', ['Les ventes additionnées depuis le début','La variation du mois précédent','La moyenne des ventes','Le profit rapporté aux ventes'],0,'cumsum additionne progressivement les valeurs dans leur ordre.'),
  ('Une évolution depuis une base fixe compare quoi ?', ['La valeur courante à la première période','Chaque mois au précédent','Le profit au coût d’achat','La somme cumulée à la moyenne mobile'],0,'La base reste la première période choisie.'),
  ('Comment calculer le profit cumulé rapporté au CA ?', ['Somme des profits / somme des ventes','Moyenne des taux mensuels','Somme des taux mensuels','Profit courant / ventes du premier mois'],0,'Le ratio utilise les deux cumuls sur le même périmètre temporel.'),
  ('Que représente rolling(3).mean() ?', ['Une moyenne sur trois lignes successives','La moyenne des trois meilleures valeurs','Une prévision sur trois mois','Une somme cumulée'],0,'rolling(3) prend trois lignes. Elles ne représentent trois mois que si le calendrier est complet et ordonné.'),
  ('Pourquoi les premières fenêtres rolling peuvent-elles être NaN ?', ['Elles n’ont pas encore trois observations','Les valeurs sont nécessairement nulles','Les dates sont des chaînes','mean renvoie toujours NaN'],0,'Avec une fenêtre complète, les premières lignes manquent d’historique.'),
  ('Que montre un boxplot de Profit tracé directement depuis Orders ?', ['La distribution par ligne de commande','La distribution par commande unique','La marge commerciale','Les ventes mensuelles'],0,'Chaque observation vient d’une ligne du tableau ; il faut agréger Order ID pour changer le grain.'),
  ('Un point éloigné sur un boxplot prouve-t-il une erreur ?', ['Non, c’est une observation à examiner','Oui, toujours','Il prouve une cause commerciale','Il s’agit forcément d’un doublon'],0,'Une valeur atypique mérite vérification, mais sa présence ne prouve ni erreur ni cause.'),
  ('Un cumul de ventes est-il toujours croissant ?', ['Non, pas si des montants négatifs sont présents','Oui, quelle que soit la donnée','Seulement pour une courbe','Seulement si rolling est utilisé'],0,'Des valeurs négatives peuvent faire diminuer une somme cumulée.')])
}

# QCM de synthèse placé après les quatre blocs du socle.
QUIZZES['qcm_matin'] = ('Synthèse — Pandas, graphiques et indicateurs',
    QUIZZES['qcm_comparaisons'][1][:5] +
    QUIZZES['qcm_marges'][1][:5] +
    QUIZZES['qcm_synthese'][1][:5])

# Corrigés exécutables gardés hors des carnets étudiants.
SOLUTIONS = {
 '01_explorer': [
  "print('Régions :', orders['Region'].nunique())\nprint('Catégories :', orders['Category'].nunique())\nprint('Années :', orders['Order Date'].dt.year.nunique())",
  'orders.head()'],
 '02_comparer': [
  "ca_regions = orders.groupby('Region')['Sales'].sum().sort_values()\nfig, ax = plt.subplots(figsize=(8, 4))\nax.barh(ca_regions.index, ca_regions.values)\nax.set(title='Ventes par région', xlabel='Ventes (unités monétaires)')\nplt.show()",
  "ca_categories = orders.groupby('Category')['Sales'].sum().sort_values()\nfig, ax = plt.subplots(figsize=(8, 4))\nax.barh(ca_categories.index, ca_categories.values)\nax.set(title='Ventes par catégorie', xlabel='Ventes (unités monétaires)')\nplt.show()"],
 '03_rentabilite': [
  "print(bilan['Sales'].sort_values(ascending=False))\nprint(bilan['Profit'].sort_values(ascending=False))",
  "ratio = bilan['Profit'].div(bilan['Sales'].replace(0, float('nan'))) * 100\nfig, ax = plt.subplots(figsize=(8, 4))\nax.barh(ratio.sort_values().index, ratio.sort_values().values)\nax.set(title='Profit rapporté aux ventes par catégorie', xlabel='Profit / ventes (%)')\nplt.show()",
  "marge_ligne = orders['Profit'] / orders['Sales'] * 100\nratio_global = orders['Profit'].sum() / orders['Sales'].sum() * 100\nprint('Moyenne simple des taux ligne à ligne :', marge_ligne.mean())\nprint('Ratio des sommes :', ratio_global)"],
 '04_temps_et_variations': [
  "print(mensuel.idxmax(), mensuel.max())\nprint(mensuel.idxmin(), mensuel.min())\nprint('Dates ordonnées :', mensuel.index.is_monotonic_increasing)",
  "variation_montant = mensuel.diff()\nvariation_pct = mensuel.pct_change() * 100\nprint('Plus forte hausse relative :', variation_pct.idxmax(), variation_pct.max())\nprint('Plus forte baisse relative :', variation_pct.idxmin(), variation_pct.min())\nprint('Plus forte hausse en montant :', variation_montant.idxmax(), variation_montant.max())"],
 '05_cumuls': [
  "m = orders.set_index('Order Date').resample('MS')[['Sales', 'Profit']].sum()\nm['Sales_cumulees'] = m['Sales'].cumsum()\nprint(m['Sales_cumulees'].iloc[-1], orders['Sales'].sum())",
  "ratio_sommes = (10 + 90) / (100 + 300) * 100\nmoyenne_taux = ((10 / 100) + (90 / 300)) / 2 * 100\nprint('Ratio des sommes :', ratio_sommes, '%')\nprint('Moyenne simple :', moyenne_taux, '%')",
  "print(m.loc['2023-01-01':'2023-03-01', ['Sales', 'Sales_moyenne_mobile_3']])\nprint('Calcul manuel mars :', m['Sales'].iloc[:3].mean())",
  "variation_mensuelle = m['Sales'].pct_change() * 100\nevolution_base_fixe = (m['Sales'].iloc[-1] / m['Sales'].iloc[0] - 1) * 100\nprint('Évolution à base fixe :', evolution_base_fixe)\nprint('Somme des variations :', variation_mensuelle.sum())"],
 '06_distributions': [
  "s = orders.loc[orders['Category'].eq('Technology'), 'Profit']\nprint('Médiane :', s.median())\nprint('Quartiles :', s.quantile([0.25, 0.75]).to_dict())\nprint('Lignes à profit négatif :', (s < 0).sum())",
  "profit_commande = orders.groupby('Order ID')['Profit'].sum()\nfig, ax = plt.subplots(figsize=(6, 4))\nax.boxplot([profit_commande.dropna()], tick_labels=['Commande'], showfliers=True)\nax.axhline(0, color='black', linewidth=1)\nax.set(title='Profit par commande', ylabel='Profit (unités monétaires)')\nplt.show()"],
 'tp_binomes': [TP.get('setup_solution',''), '']
}
SOLUTIONS['01_explorer'] = [s['solution'] for s in PAGES[0]['sequences']]

def lesson(title, steps, interpretation, exercise_title, prompt, deliverable,
           starter, solution, answer, chart):
    example='\n\n'.join(code for _,_,code in steps if code)
    return dict(title=title, steps=steps, interpretation=interpretation,
                reading=interpretation, example=example,
                exercise_title=exercise_title, prompt=prompt,
                deliverable=deliverable, starter=starter,
                solution=solution, answer=answer, chart=chart)

from lesson_content import apply_lessons
apply_lessons(PAGES, SOLUTIONS, lesson, globals())

REVIEW_QUESTIONS = {
 '01_explorer': ['Que décrit une ligne de Orders ?','Pourquoi len(orders) ne compte-t-il pas les commandes ?','Quelle méthode compte les identifiants distincts ?','Comment repérer les valeurs manquantes ?','Quel type de vérification faire avant un calcul ?'],
 '02_comparer': ['Que fait groupby avant sum ?','Quel est le grain du graphique par région ?','Pourquoi garder la Series entière pendant le tri ?','Que représente une Figure ?','Que règle un Axes ?'],
 '03_rentabilite': ['Quelle est la formule du profit rapporté aux ventes ?','Pourquoi diviser les sommes plutôt que moyenner les ratios ?','Quelle information manque pour le taux de marge commerciale ?','Que signifie un profit négatif ?','Comment traiter un dénominateur nul ?'],
 '04_temps_et_variations': ['Pourquoi créer un index datetime ?','Que produit resample("MS") ?','Que renvoie pct_change avant la multiplication par 100 ?','Quelle référence utilise la variation mensuelle ?','Comment distinguer une hausse en montant d’une hausse en pourcentage ?'],
 '05_cumuls': ['Que calcule cumsum ?','Pourquoi un cumul peut-il progresser pendant une baisse mensuelle ?','Quelle est la référence d’une évolution à base fixe ?','Comment calcule-t-on le profit cumulé rapporté au CA ?','Que signifie rolling(3) ?','Pourquoi les premières fenêtres complètes sont-elles absentes ?'],
 '06_distributions': ['Que représente la médiane dans une boîte ?','À quoi correspondent les quartiles ?','Quel est le grain du boxplot direct ?','Comment passer à une observation par commande ?','Une valeur atypique prouve-t-elle une erreur ?']
}
SUMMARIES = {
 '01_explorer': 'Une ligne est une ligne de commande ; un identifiant Order ID peut se répéter. Vérifiez les colonnes et les dates avant d’agréger.',
 '02_comparer': 'Regroupez d’abord Sales au niveau demandé. Triez la Series entière pour conserver le lien entre nom et montant.',
 '03_rentabilite': 'Le ratio du jeu est le profit total divisé par les ventes totales. Il ne révèle pas les coûts d’achat.',
 '04_temps_et_variations': 'Agrégez dans un index datetime trié. Une variation relative compare deux périodes et n’est pas une variation en montant.',
 '05_cumuls': 'Cumul, évolution fixe, moyenne mobile et ratio des cumuls ont des références et des unités différentes.',
 '06_distributions': 'La boîte décrit une distribution au grain choisi. Une ligne de commande et une commande sont deux unités d’analyse.'
}

def head(title, depth=0, scripts=''):
    pre='../'*depth
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f7f8f2"><title>{html.escape(title)} — Le labo Matplotlib</title><link rel="stylesheet" href="{pre}assets/site.css"><link rel="stylesheet" href="{pre}assets/tableau.css"><link rel="stylesheet" href="{pre}assets/course.css">{scripts}</head><body><a class="skip-link" href="#contenu">Aller au contenu</a><header class="site-header"><a class="brand" href="{pre}index.html"><span class="brand-icon" aria-hidden="true">mp.</span> Le labo Matplotlib</a><a class="back-link" href="{pre}index.html">← Le parcours</a></header>'''

def foot(depth=1): return f'<footer class="site-footer"><span>Le labo Matplotlib / NEXA</span><a href="{"../"*depth}index.html">Comprendre, puis pratiquer.</a></footer></body></html>'

def code(s): return '<div class="code-block"><span class="code-label">Python · notebook sandbox</span><pre tabindex="0"><code>'+html.escape(s)+'</code></pre></div>'

def blocks_nav(active=None):
    discovery_link=f'<a href="{DISCOVERY["file"]}.html"'+(' aria-current="page"' if active==DISCOVERY['file'] else '')+f'>Découverte · {DISCOVERY["title"]}</a>'
    items=''.join(f'<a href="{p["file"]}.html"'+(' aria-current="page"' if p['file']==active else '')+f'>{i:02} · {p["title"]}</a>' for i,p in enumerate(PAGES,1))
    return discovery_link+items+'<a href="tp_binomes.html">TP en binômes</a>'

def build_page(page, i):
    title=page['title']; file=page['file']; qcm=page.get('qcm')
    sections=[]
    sections.append(('question','Question métier',f'<h2>{html.escape(page["question"])}</h2><p>{html.escape(page["intro"])}</p>'))
    if file == '01_explorer':
        loader='''# %pip install xlrd
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel(
    "/workspace/data/sample_-_superstore.xls",
    sheet_name="Orders"
)

df.info()

# Nom du tableau utilisé dans la suite du cours
orders = df'''
        sections.append(('chargement','Charger les données',f'<h2>Charger la feuille Orders</h2><p>Exécutez cette cellule pour lire le fichier fourni et vérifier les colonnes et les types de données.</p>{code(loader)}'))
    if not page.get('sequences'):
        sections.append(('objectif','Objectif',f'<h2>Ce que vous allez savoir faire</h2><p>À la fin, vous pourrez répondre à cette question avec un calcul vérifiable, un graphique adapté et une interprétation prudente.</p>'))
        sections.append(('resume','Résumé général',f'<h2>Repère du bloc</h2><p>{html.escape(SUMMARIES[file])}</p>'))
    concepts='<h2>Notions à mobiliser</h2>'+''.join(f'<article class="concept"><h3>{html.escape(n)}</h3><p>{html.escape(d)}</p><p class="small">Pourquoi c’est utile : {html.escape(w)}</p></article>' for n,d,w in page.get('concepts',[]))
    sections.append(('notions','Notions',concepts))
    if file == '01_explorer':
        sizes=[('(5, 3)','500 × 300 px','Petit graphique'),('(8, 4)','800 × 400 px','Graphique standard'),('(10, 5)','1 000 × 500 px','Courbe temporelle'),('(12, 6)','1 200 × 600 px','Graphique détaillé'),('(12, 8)','1 200 × 800 px','Figure avec plusieurs graphiques')]
        rows=''.join(f'<tr><td><code>{shape}</code></td><td>{pixels}</td><td>{use}</td></tr>' for shape,pixels,use in sizes)
        table=f'<h2>Repères pratiques pour Matplotlib</h2><p><code>figsize=(largeur, hauteur)</code> règle la taille de la figure en pouces. À 100 DPI, multipliez chaque valeur par 100 pour obtenir les dimensions en pixels. La taille affichée dans Jupyter peut dépendre du navigateur et du moteur graphique.</p><div class="figsize-table-wrap"><table><thead><tr><th scope="col">figsize</th><th scope="col">À 100 DPI</th><th scope="col">Utilisation</th></tr></thead><tbody>{rows}</tbody></table></div>'
        sections.append(('figsize','Choisir la taille d’une figure',table))
    if page.get('formula'):
        sections.append(('formule','Lecture des formules',page['formula']))
    if qcm and i==1 and not page.get('sequences'):
        sections.append(('verification','QCM de réactivation',f'<h2>Avant de charger les données</h2><p>Réactivez vos repères sur le grain, pandas et les graphiques. Le bilan s’affichera uniquement après la soumission.</p><a class="button primary" href="../qcm/{qcm}.html">Faire le QCM →</a>'))
    exlink=[]
    if not page.get('sequences'):
        example=f'<h2>Exemple guidé</h2><p>Exécutez le code et observez les objets et l’unité affichés.</p>{code(page["example"])}<h3>Lecture du code</h3><p>{html.escape(page["reading"])}</p>'
        sections.append(('exemple','Exemple',example))
    milestone={
     '01_explorer':'Préparer la base de travail : identifier ce que représente une ligne et vérifier les identifiants.',
     '02_comparer':'Construire un premier graphique de comparaison à partir d’un total agrégé.',
     '03_rentabilite':'Ajouter au même rapport un indicateur de profit rapporté aux ventes.',
     '04_temps_et_variations':'Compléter la note par une série mensuelle et ses variations.',
     '05_cumuls':'Prolonger l’analyse temporelle avec des mesures cumulées et lissées.',
     '06_distributions':'Ajouter une lecture de la dispersion au niveau ligne puis commande.'}[file]
    project=f'<h2>Projet fil rouge · note visuelle commerciale</h2><p>La responsable commerciale a besoin d’une note vérifiable sur les ventes et le profit de la feuille Orders. À ce jalon : {html.escape(milestone)}</p><p>Les livrables s’assemblent dans le <a href="tp_binomes.html">TP en binômes</a> ; le TP n’exige que les notions du socle du matin.</p>'
    if not page.get('sequences'):
        sections.append(('projet','Projet fil rouge',project))
    if page.get('sequences'):
        paired=''
        for j,s in enumerate(page['sequences'],1):
            aid=f'exercice-{j}'; exlink.append((aid,s['exercise_title']))
            guided=''
            for step_title,step_text,step_code in s.get('steps',[]):
                guided+=f'<h4>{html.escape(step_title)}</h4><p>{html.escape(step_text)}</p>'
                if step_code:
                    guided+=code(step_code)
            if not guided:
                guided=f'<h3>Exemple guidé</h3>{code(s["example"])}<p>{html.escape(s["reading"])}</p>'
            graphic=chart_html(s['chart']) if s.get('chart') else ''
            interpretation=s.get('interpretation',s.get('reading',''))
            interpretation_html=('<h4>Étape 3 — Interpréter</h4><p>'+html.escape(interpretation)+'</p>') if s.get('steps') else ''
            starter=''
            paired+=f'''<article class="learning-sequence">
<p class="eyebrow">Notion {j:02}</p><h2>{html.escape(s['title'])}</h2>
{guided}{graphic}{interpretation_html}
<div class="exercise" id="{aid}"><p class="eyebrow">Exercice {j:02}</p><h3>{html.escape(s['exercise_title'])}</h3><p>{html.escape(s['prompt'])}</p>{starter}<p><strong>À rendre :</strong> {html.escape(s['deliverable'])}</p></div>
</article>'''
        sections.append(('sequences','Exemples et exercices', '<h2>Exemples guidés, graphiques et exercices</h2>'+paired))
    else:
        exercises=''
        for j,(name,prompt,deliverable,starter,solution) in enumerate(page['exercises'],1):
            aid=f'exercice-{j}'; exlink.append((aid,name))
            shown=''
            exercises+=f'<article class="exercise" id="{aid}"><p class="eyebrow">Exercice {j:02}</p><h3>{html.escape(name)}</h3><p>{html.escape(prompt)}</p>{shown}<p><strong>À rendre :</strong> {html.escape(deliverable)}</p></article>'
        exercises='<h2>À vous de pratiquer</h2><p>Faites les exercices dans le notebook du bloc. Les corrections sont sur une page séparée.</p>'+exercises
        sections.append(('exercices','Exercices',exercises))
    if not page.get('sequences'):
        error='<h2>Points de vigilance</h2><ul>'+''.join('<li>'+html.escape(e)+'</li>' for e in page.get('errors',[]))+'</ul>'
        sections.append(('vigilance','Erreurs fréquentes',error))
        review='<h2>Questions de révision</h2><ol>'+''.join(f'<li>{html.escape(q)}</li>' for q in REVIEW_QUESTIONS[file])+'</ol>'
        sections.append(('revision','Questions de révision',review))
    if qcm and i!=1 and not page.get('sequences'): sections.append(('verification','Vérifier ses choix',f'<h2>Fin du jalon</h2><p>Le QCM arrive après les exemples et les exercices. Répondez d’abord à toutes les questions ; le score et les explications seront affichés à la soumission.</p><a class="button primary" href="../qcm/{qcm}.html">Ouvrir le QCM →</a>'))
    if not page.get('sequences'):
        sections.append(('resume-final','Résumé final','<h2>Rendre le résultat vérifiable</h2><p>Nommer le grain et l’unité, vérifier la valeur sur la table, puis séparer l’observation de son explication.</p>'))
    if qcm == 'qcm_avance' and page.get('sequences'):
        sections.append(('verification','QCM du bloc',f'<h2>Vérifier les notions du bloc</h2><p>Répondez aux questions. Le score et les explications apparaissent après la soumission.</p><a class="button primary" href="../qcm/{qcm}.html">Faire le QCM →</a>'))
    nav=''.join(f'<a href="#{sid}">{n}</a>' for sid,n,_ in sections)+f'<hr><a href="../corrections/{file}.html">Corrigés du bloc</a>'
    body=''.join(f'<section class="course-section{" qcm-section" if sid == "verification" and qcm else ""}" id="{sid}"><p class="eyebrow">{i:02} · {label}</p>{content}</section>' for sid,label,content in sections)
    notebook='http://localhost:8890/lab'
    hero=f'<main class="course-main" id="contenu"><div class="course-intro"><p class="eyebrow">{page["group"]}</p><h1>{html.escape(title)}</h1><p>{html.escape(page["intro"])}</p><p class="layout-note">Le cours à gauche. Le notebook à droite.</p></div><div class="course-layout"><nav class="course-nav" aria-label="Navigation du cours"><p class="eyebrow">Dans ce bloc</p>{nav}<hr><p class="eyebrow">Le parcours</p>{blocks_nav(file)}</nav><div class="course-content">{body}</div><aside class="notebook-panel"><p class="eyebrow">Atelier Jupyter</p><h2>Créer un notebook</h2><p>Créez un notebook Python 3 dans JupyterLab, puis réalisez les exemples et exercices avec le jeu de données fourni.</p><a class="button primary" href="{notebook}" target="_blank" rel="noopener">Ouvrir JupyterLab →</a><p class="small">Le fichier Superstore est disponible dans <code>/workspace/data</code>. Enregistrez vos figures dans <code>/workspace/resultats</code>.</p></aside></div></main>'
    (ROOT/'supports'/f'{file}.html').write_text(head(title,1)+hero+foot(1),encoding='utf8')
    corr=''.join(f'<article class="exercise correction" id="{aid}"><p class="eyebrow">Correction · {j:02}</p><h2>{html.escape(name)}</h2><p><strong>Consigne :</strong> {html.escape(page["exercises"][j-1][1])}</p>{code(SOLUTIONS[file][j-1])}<h3>Résultat attendu et interprétation</h3><p>{html.escape(page["exercises"][j-1][4])}</p><a href="../supports/{file}.html#{aid}">Retour au bloc</a></article>' for j,(aid,name) in enumerate(exlink,1))
    ch=f'<main class="course-main" id="contenu"><div class="course-intro"><p class="eyebrow">Corrigé formateur</p><h1>{html.escape(title)}</h1><p>Résultats calculés sur la feuille Orders du classeur source.</p></div><div class="course-content">{corr}</div></main>'
    (ROOT/'corrections'/f'{file}.html').write_text(head(title,1)+ch+foot(1),encoding='utf8')
    return sections

def nb_cell(kind, source):
    c={'cell_type':kind,'metadata':{},'source':source.splitlines(keepends=True)}
    if kind=='code':c.update(execution_count=None,outputs=[])
    return c

def build_notebook(page, corrected=False):
    cells=[]
    title=page['title']; cells.append(nb_cell('markdown',f'# {title}\n\n{page["intro"]}\n\n**Question métier :** {page["question"]}\n\nLes données sont montées en lecture seule. Enregistrez vos figures dans `/workspace/resultats`.'))
    if page is TP:
        cells.append(nb_cell('code',page['data_code']))
        cells.append(nb_cell('code',page['data_check']))
    elif page['file'] == '01_explorer':
        cells.append(nb_cell('code','''# %pip install xlrd
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel(
    "/workspace/data/sample_-_superstore.xls",
    sheet_name="Orders"
)

df.info()'''))
        cells.append(nb_cell('code',"orders = df\norders['Order Date'] = pd.to_datetime(orders['Order Date'])"))
    else:
        cells.append(nb_cell('code',DATA))
    if not page.get('sequences') and page is not TP:
        cells.append(nb_cell('code','orders.shape, orders.columns.tolist(), orders["Order ID"].nunique(), orders.isna().sum()'))
    if page.get('sequences'):
        for j,s in enumerate(page['sequences'],1):
            cells.append(nb_cell('markdown',f'## Notion {j} — {s["title"]}\n'))
            if s.get('steps'):
                for step_title,step_text,step_code in s['steps']:
                    cells.append(nb_cell('markdown',f'### {step_title}\n\n{step_text}'))
                    if step_code: cells.append(nb_cell('code',step_code))
                cells.append(nb_cell('markdown','### Étape 3 — Interpréter\n\n'+s.get('interpretation',s.get('reading',''))))
            else:
                cells.append(nb_cell('markdown',f'### Exemple guidé\n\n{s["reading"]}'))
                cells.append(nb_cell('code',s['example']))
            cells.append(nb_cell('markdown',f'### Exercice {j} — {s["exercise_title"]}\n\n{s["prompt"]}\n\n**À rendre :** {s["deliverable"]}'))
            cells.append(nb_cell('code',s['solution'] if corrected else ''))
            if corrected:
                cells.append(nb_cell('markdown',f'### Mise en commun\n\n{s["answer"]}'))
        nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},'nbformat':4,'nbformat_minor':5}
        folder=ROOT/'formateur'/'notebooks' if corrected else ROOT/'notebooks'
        folder.mkdir(parents=True,exist_ok=True)
        name=page.get('notebook',page['file']+'.ipynb')
        if corrected:name=name.removesuffix('.ipynb')+'_corrige.ipynb'
        (folder/name).write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n',encoding='utf8')
        return
    setup=page.get('setup_solution' if corrected else 'setup_student')
    if corrected and page is TP:
        setup=None
    if setup:
        cells.append(nb_cell('markdown','## Graphiques du projet' if page is TP else '## Préparation'))
        cells.append(nb_cell('code',setup))
    cells += [nb_cell('markdown','## Exemple guidé\n\n'+page['reading']),nb_cell('code',page['example'])]
    for j,(name,prompt,deliverable,starter,solution) in enumerate(page['exercises'],1):
        cells.append(nb_cell('markdown',f'## Exercice {j} — {name}\n\n{prompt}\n\n**À rendre :** {deliverable}'))
        cells.append(nb_cell('code',SOLUTIONS[page['file']][j-1] if corrected else ''))
        if corrected: cells.append(nb_cell('markdown','### Correction expliquée\n\n'+solution+'\n\n'+page.get('reading','')))
    if not corrected and page['exercises']:
        cells.append(nb_cell('markdown','## Bilan des exercices\n\nRassemblez ici les résultats et interprétations à présenter pour ce bloc.'))
    if corrected and page is TP and page.get('optional_question'):
        optional=page['optional_question']
        cells.append(nb_cell('markdown',f'## Question facultative — {optional["title"]}\n\n{optional["prompt"]}'))
        cells.append(nb_cell('code',optional['solution']))
        cells.append(nb_cell('markdown',optional['answer']))
    nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},'nbformat':4,'nbformat_minor':5}
    folder=ROOT/'formateur'/'notebooks' if corrected else ROOT/'notebooks'
    folder.mkdir(parents=True,exist_ok=True)
    name=page.get('notebook',page['file']+'.ipynb')
    if corrected:name=name.removesuffix('.ipynb')+'_corrige.ipynb'
    (folder/name).write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n',encoding='utf8')

def distribute_quiz_answers(key, questions):
    rng=Random(sha256(key.encode('utf8')).hexdigest())
    positions=list(range(4))*(len(questions)//4)+rng.sample(range(4),len(questions)%4)
    for _ in range(100):
        rng.shuffle(positions)
        if all(not positions[i]==positions[i-1]==positions[i-2] for i in range(2,len(positions))):
            break
    else:
        raise ValueError(f'Impossible de répartir les réponses du QCM {key}')
    prepared=[]
    for (question,options,answer,why),position in zip(questions,positions):
        if len(options)!=4 or len(set(options))!=4 or answer not in range(4):
            raise ValueError(f'Choix invalides dans le QCM {key} : {question}')
        reordered=[option for i,option in enumerate(options) if i!=answer]
        rng.shuffle(reordered)
        reordered.insert(position,options[answer])
        prepared.append((question,reordered,position,why))
    return prepared


def build_quiz(key, item):
    title, questions=item
    questions=distribute_quiz_answers(key,questions)
    fields=''
    for i,(q,opts,answer,why) in enumerate(questions,1):
        fields+=f'<fieldset{" hidden" if i>1 else ""} data-answer="{answer}" data-why="{html.escape(why,quote=True)}"><legend>{i}. {html.escape(q)}</legend>'+''.join(f'<label class="quiz-option"><input type="radio" name="q{i}" value="{j}"><span><b>{"ABCD"[j]}.</b> {html.escape(o)}</span></label>' for j,o in enumerate(opts))+'<p class="quiz-feedback" aria-live="polite" hidden></p></fieldset>'
    form=f'<main class="course-main quiz-main quiz-page" id="contenu"><div class="course-intro"><p class="eyebrow">QCM · Réactivation formative</p><h1>{html.escape(title)}</h1><p>Une question à la fois. Choisissez une réponse pour afficher la correction détaillée, puis passez à la suivante.</p></div><form id="quiz" class="quiz-sheet qcm-form"><p id="quiz-progress" class="quiz-progress" aria-live="polite">Question 1 sur {len(questions)}</p>{fields}<p id="quiz-score" aria-live="polite" hidden></p><div class="quiz-controls"><button class="button primary" id="quiz-next" type="button" hidden>Question suivante →</button><button class="button" id="quiz-restart" type="reset" hidden>Recommencer</button></div></form></main>'
    js='<script src="../assets/quiz.js" defer></script>'
    (ROOT/'qcm'/f'{key}.html').write_text(head(title,1,js)+form+foot(1),encoding='utf8')

def build_tp():
    page=TP; file='tp_binomes'
    fields=''.join(f'<tr><td><code>{html.escape(name)}</code></td><td>{html.escape(description)}</td></tr>' for name,description in page['fields'])
    visuals=''.join(f'<li><strong>{html.escape(title)}</strong><br>{html.escape(task)}</li>' for title,task in page['visuals'])
    sections=[
        ('mission','Mission',f'<h2>{page["question"]}</h2><p>Votre notebook constitue une maquette analytique pour un futur tableau de bord Power BI destiné à la responsable commerciale.</p>'),
        ('donnees','Données',f'<h2>Ventes du réseau Nova</h2><p>Utilisez le fichier <code>/workspace/data/{page["data_file"]}</code>, également disponible en <a href="../data/{page["data_file"]}" download>téléchargement CSV</a>.</p><p>Ces données pédagogiques sont fictives et couvrent l’année 2025. Une ligne correspond à une ligne de commande ; une commande peut contenir plusieurs produits. Les montants sont exprimés en euros hors taxes.</p><div class="table-wrap"><table><thead><tr><th scope="col">Colonne</th><th scope="col">Signification</th></tr></thead><tbody>{fields}</tbody></table></div><p>La marge commerciale est la différence entre le chiffre d’affaires et le coût d’achat. Le pourcentage demandé rapporte cette marge au chiffre d’affaires. Les autres charges de l’entreprise ne sont pas décrites.</p>'),
        ('travail','Travail demandé',f'<h2>Quatre graphiques au total</h2><ol>{visuals}</ol><p>Chaque graphique doit comporter un titre, des axes lisibles et les unités appropriées.</p><h3>Deux insights</h3><p>Rédigez exactement deux insights portant sur des constats différents et appuyés sur les graphiques. Chaque insight présente un constat métier précis, les chiffres qui le justifient et une implication ou une piste d’action.</p>'),
        ('livrables','Livrables','<h2>À rendre</h2><ul><li>Un notebook créé par votre binôme, contenant les calculs, les quatre graphiques et les deux insights.</li><li>Les quatre figures exportées en PNG dans <code>/workspace/resultats</code>.</li></ul><p>Le notebook doit pouvoir s’exécuter de haut en bas après redémarrage du noyau.</p>'),
        ('facultatif','Question facultative',f'<h2>Question facultative · {html.escape(page["optional_question"]["title"])}</h2><p>{html.escape(page["optional_question"]["prompt"])}</p>'),
    ]
    nav=''.join(f'<a href="#{a}">{b}</a>' for a,b,_ in sections)
    body=''.join(f'<section class="course-section" id="{a}"><p class="eyebrow">TP en binômes · {b}</p>{c}</section>' for a,b,c in sections)
    main=f'<main class="course-main" id="contenu"><div class="course-intro"><p class="eyebrow">Sujet du TP</p><h1>{page["title"]}</h1><p>{page["intro"]}</p></div><div class="course-layout tp-layout"><nav class="course-nav"><p class="eyebrow">Dans le sujet</p>{nav}</nav><div class="course-content">{body}</div></div></main>'
    (ROOT/'supports'/'tp_binomes.html').write_text(head(page['title'],1)+main+foot(1),encoding='utf8')
    build_notebook(page,True)
    insights=''.join(f'<li>{html.escape(text)}</li>' for text in page['insights'])
    optional=page['optional_question']
    solution=f'<main class="course-main" id="contenu"><div class="course-intro"><p class="eyebrow">Corrigé formateur</p><h1>Préparer un tableau de bord Power BI</h1><p>Exemple de réalisation sur le jeu fictif Nova ; les deux insights proposés peuvent être remplacés par d’autres constats étayés.</p></div><div class="course-content"><h2>Chargement des données</h2>{code(page["data_code"])}<h2>Quatre graphiques</h2>{code(page["setup_solution"])}<h2>Deux insights possibles</h2><ol>{insights}</ol><h2>Question facultative · {html.escape(optional["title"])}</h2>{code(optional["solution"])}<p>{html.escape(optional["answer"])}</p></div></main>'
    (ROOT/'corrections'/'tp_binomes.html').write_text(head('Correction du TP',1)+solution+foot(1),encoding='utf8')

def main():
    build_discovery(ROOT, head, foot, code, blocks_nav)
    index=[]
    for i,p in enumerate(PAGES,1):
        p['notebook']={1:'01_exploration.ipynb',2:'02_comparaisons.ipynb',3:'03_rentabilite.ipynb',4:'04_serie_temporelle.ipynb',5:'05_cumuls_avance.ipynb',6:'06_boxplots_avance.ipynb'}[i]
        if i==4:p['qcm']='qcm_matin'
        if i==6:p['qcm']='qcm_avance'
        build_page(p,i); build_notebook(p,True)
        index.append(p)
    demarrage={'file':'00_demarrage','title':'Démarrer avec Orders','group':'Socle du matin','intro':'Charger le classeur Superstore et contrôler ses données avant l’analyse.','question':'Que contient la feuille Orders ?','example':'''print('Lignes :', len(orders))\nprint('Commandes distinctes :', orders['Order ID'].nunique())\nprint('Ventes totales :', orders['Sales'].sum())\norders.head()''','reading':'Le nombre de lignes compte les observations du fichier ; nunique compte les commandes distinctes ; la somme additionne Sales.','exercises':[]}
    build_notebook(demarrage,True)
    build_tp()
    for k in ('reactivation_00','qcm_matin','qcm_avance'):
        build_quiz(k,QUIZZES[k])
    for old_quiz in ('qcm_comparaisons','qcm_marges','qcm_synthese'):
        (ROOT/'qcm'/f'{old_quiz}.html').unlink(missing_ok=True)
    (ROOT/'assets'/'quiz.js').write_text('''"use strict";
const form=document.querySelector('#quiz');
if(form){
  const questions=[...form.querySelectorAll('fieldset')];
  const progress=form.querySelector('#quiz-progress');
  const next=form.querySelector('#quiz-next');
  const scoreBox=form.querySelector('#quiz-score');
  const restart=form.querySelector('#quiz-restart');
  let current=0, correct=0;
  questions.forEach((fieldset,index)=>{
    fieldset.hidden=index!==0;
    fieldset.querySelectorAll('input[type="radio"]').forEach(input=>input.addEventListener('change',()=>{
      if(index!==current||fieldset.dataset.answered)return;
      const answer=fieldset.querySelector('input:checked');
      const expected=fieldset.querySelector(`input[value="${fieldset.dataset.answer}"]`);
      const feedback=fieldset.querySelector('.quiz-feedback');
      const isCorrect=answer.value===fieldset.dataset.answer;
      if(isCorrect)correct++;
      fieldset.dataset.answered='true';
      fieldset.querySelectorAll('input').forEach(option=>option.disabled=true);
      feedback.hidden=false;
      feedback.className=`quiz-feedback ${isCorrect?'correct':'incorrect'}`;
      feedback.textContent=isCorrect
        ?`Bonne réponse : ${expected.nextElementSibling.textContent}. ${fieldset.dataset.why}`
        :`Votre réponse : ${answer.nextElementSibling.textContent}. Réponse attendue : ${expected.nextElementSibling.textContent}. ${fieldset.dataset.why}`;
      next.hidden=false;
      next.textContent=index===questions.length-1?'Voir mon résultat':'Question suivante →';
      progress.textContent=`Question ${index+1} sur ${questions.length} · correction affichée`;
    }));
  });
  next.addEventListener('click',()=>{
    if(!questions[current]||!questions[current].dataset.answered)return;
    questions[current].hidden=true;
    current++;
    next.hidden=true;
    if(current<questions.length){
      questions[current].hidden=false;
      progress.textContent=`Question ${current+1} sur ${questions.length}`;
      questions[current].querySelector('input[type="radio"]').focus();
      return;
    }
    progress.hidden=true;
    scoreBox.hidden=false;
    restart.hidden=false;
    const percent=Math.round(correct/questions.length*100);
    scoreBox.textContent=`Résultat : ${correct} / ${questions.length} (${percent} %). ${percent<70?'Reprenez les exemples du cours avant de poursuivre.':'Vous pouvez revoir les explications en recommençant le QCM.'}`;
  });
  form.addEventListener('reset',()=>setTimeout(()=>{
    current=0;correct=0;
    progress.hidden=false;
    progress.textContent=`Question 1 sur ${questions.length}`;
    scoreBox.hidden=true;scoreBox.textContent='';
    restart.hidden=true;
    next.hidden=true;
    questions.forEach((fieldset,index)=>{
      delete fieldset.dataset.answered;
      fieldset.hidden=index!==0;
      fieldset.querySelectorAll('input').forEach(input=>input.disabled=false);
      const feedback=fieldset.querySelector('.quiz-feedback');
      feedback.hidden=true;feedback.className='quiz-feedback';feedback.textContent='';
    });
  },0));
}
''',encoding='utf8')
    (ROOT/'assets'/'tp.js').unlink(missing_ok=True)
    hero='''<main class="home" id="contenu"><section class="hero"><div><p class="eyebrow"><span class="status-dot"></span> De Superstore aux indicateurs</p><h1>Vos données.<br>Une figure.<br><span>Une réponse.</span></h1><p class="hero-description">Un parcours Python et Matplotlib pour vérifier les données, calculer les indicateurs commerciaux et défendre une conclusion.</p><div class="actions"><a class="button primary" href="qcm/reactivation_00.html">Réactiver les bases →</a><a class="button" href="supports/00_decouvrir_graphiques.html">Découvrir les graphiques</a><a class="button" href="supports/tp_binomes.html">Voir le TP en binômes</a></div><p class="hero-note">Pandas · Matplotlib · feuille Orders · exercices sur notebook</p></div><div class="hero-illustration"><div class="diagram-heading"><span class="mini-label">Du fichier à la décision</span><span class="pill">Orders</span></div><div class="flow-step"><span class="flow-index">01</span><div><small>VÉRIFIER</small><strong>Le grain et les données</strong></div></div><div class="flow-connector">↓</div><div class="flow-step treatment"><span class="flow-index">02</span><div><small>CALCULER</small><strong>Une mesure pertinente</strong></div></div><div class="flow-connector">↓</div><div class="flow-step"><span class="flow-index">03</span><div><small>EXPLIQUER</small><strong>Un constat et sa limite</strong></div></div></div></section>'''
    groups=[]
    for group,label in [('Socle du matin','Power BI avec Matplotlib'),('Après le socle · autonome','Approfondissements facultatifs')]:
        arr=[(i,p) for i,p in enumerate(PAGES,1) if p['group']==group]
        if arr:
            path_cards=[]
            if group == 'Socle du matin':
                path_cards.append(f'<article class="path-card qcm-path-card"><div class="qcm-card-content"><span class="card-top"><span class="step-number">00</span><span class="pill">Avant de commencer</span></span><h3>QCM de réactivation</h3><p>Retrouvez les premiers repères de Pandas et Matplotlib.</p><span class="card-bottom">{len(QUIZZES["reactivation_00"][1])} questions</span></div><a class="qcm-inline-link" href="qcm/reactivation_00.html">Faire le QCM <span aria-hidden="true">→</span></a></article>')
                path_cards.append(f'<a class="path-card" href="supports/{DISCOVERY["file"]}.html"><span class="card-top"><span class="step-number">↗</span><span class="pill">Découverte</span></span><h3>{html.escape(DISCOVERY["title"])}</h3><p>{html.escape(DISCOVERY["intro"])}</p><span class="card-bottom">Voir les cinq exemples ↗</span></a>')
            for i,p in arr:
                card=f'<a class="path-card" href="supports/{p["file"]}.html"><span class="card-top"><span class="step-number">{i:02}</span><span class="pill">{html.escape(p["group"])}</span></span><h3>{html.escape(p["title"])}</h3><p>{html.escape(p["intro"])}</p><span class="card-bottom">Ouvrir ↗</span></a>'
                if p.get('qcm') and p['qcm'] == 'qcm_avance':
                    card=f'<article class="path-card qcm-path-card"><a class="qcm-course-link" href="supports/{p["file"]}.html"><span class="card-top"><span class="step-number">{i:02}</span><span class="pill">{html.escape(p["group"])}</span></span><h3>{html.escape(p["title"])}</h3><p>{html.escape(p["intro"])}</p><span class="card-bottom">Ouvrir le bloc ↗</span></a><a class="qcm-inline-link" href="qcm/{p["qcm"]}.html">QCM de ce bloc <span aria-hidden="true">→</span></a></article>'
                path_cards.append(card)
                if p.get('qcm') == 'qcm_matin':
                    path_cards.append('<article class="path-card qcm-path-card"><div class="qcm-card-content"><span class="card-top"><span class="step-number">05</span><span class="pill">Synthèse du socle</span></span><h3>QCM de synthèse</h3><p>Vérifiez les acquis des blocs 01 à 04.</p><span class="card-bottom">15 questions</span></div><a class="qcm-inline-link" href="qcm/qcm_matin.html">Faire le QCM <span aria-hidden="true">→</span></a></article>')
            groups.append(f'<section class="home-path-section"><div class="section-heading"><div><p class="eyebrow">Parcours</p><h2>{label}</h2></div></div><nav class="path-grid">'+''.join(path_cards)+'</nav></section>')
    groups.append('<section class="home-path-section"><div class="section-heading"><div><p class="eyebrow">Sujet</p><h2>TP en binômes</h2></div></div><a class="path-card" href="supports/tp_binomes.html"><h3>Préparer un tableau de bord Power BI</h3><p>Un nouveau jeu de données, quatre graphiques et deux insights chiffrés.</p><span class="card-bottom">Ouvrir le TP ↗</span></a></section>')
    extra='''</main>'''
    (ROOT/'index.html').write_text(head('Du Superstore aux indicateurs')+hero+''.join(groups)+extra+foot(0),encoding='utf8')
    (ROOT/'assets'/'course.css').write_text('''.course-main{max-width:1560px;margin:auto;padding:0 4% 60px}.course-intro{padding:54px 0 42px;max-width:900px}.course-intro h1{font-size:clamp(2.5rem,5vw,4.5rem);margin-bottom:20px}.course-intro>p:not(.eyebrow){color:var(--muted);font-size:1.05rem}.layout-note{font-size:.83rem!important;color:var(--green)!important;font-weight:700}.course-layout{display:grid;grid-template-columns:195px minmax(0,1fr) 230px;gap:24px;align-items:start}.course-nav{position:sticky;top:20px;max-height:calc(100vh - 40px);overflow:auto;padding:12px 0}.course-nav>a{display:block;padding:8px 10px;text-decoration:none;border-radius:8px;font-size:.76rem;color:var(--muted)}.course-nav>a:hover,.course-nav>a[aria-current]{background:var(--soft);color:var(--green)}.course-nav hr{border:0;border-top:1px solid var(--line);margin:16px 0}.course-content{min-width:0}.notebook-panel{position:sticky;top:20px;padding:20px;background:#edf1e3;border:1px solid #d9e0cc;border-radius:18px}.notebook-panel h2{font-size:1.2rem}.notebook-panel p{font-size:.82rem;line-height:1.7}.notebook-panel .button{width:100%;padding:11px 12px;font-size:.8rem}.course-section,.exercise{padding:30px;margin-bottom:18px;border:1px solid var(--line);border-radius:20px;background:white}.course-section h2{font-size:clamp(1.5rem,2.3vw,2rem)}.course-section p,.course-section li,.exercise p{line-height:1.8;font-size:.93rem}.concept{padding:16px 18px;margin:12px 0;border:1px solid var(--line);border-radius:12px;background:#fafbf6}.concept h3{font-size:1.08rem;margin-bottom:8px}.small{font-size:.8rem!important;color:var(--muted)}.code-block{border-radius:13px;background:#203730;color:#f1f5e9;margin:18px 0 22px;overflow:hidden}.code-label{display:block;padding:8px 18px;border-bottom:1px solid #ffffff17;color:#b6c9b2;font-size:.62rem;letter-spacing:.1em;text-transform:uppercase}.code-block pre{margin:0;padding:18px 20px;overflow:auto;font-size:.82rem;line-height:1.8}.code-block code{color:inherit;background:transparent}.exercise{background:#fbfcf8;border-top:4px solid #b5cf66}.exercise h3{margin-top:0}.correction{border-top-color:var(--green)}.quiz-option{display:flex;gap:10px;padding:12px;margin:8px 0;border:1px solid var(--line);border-radius:10px;background:white}.quiz-feedback{padding:12px;background:var(--soft);border-radius:10px}.quiz-feedback.incorrect{background:var(--orange-bg)}fieldset{border:0;border-bottom:1px solid var(--line);padding:18px 0}legend{font-weight:650}#oral input{max-width:100px;padding:8px;border:1px solid var(--line);border-radius:8px}.flashcard{margin:8px 0;background:white}@media(max-width:1180px){.course-layout{grid-template-columns:175px minmax(0,1fr)}.notebook-panel{grid-column:2;position:static;display:grid;grid-template-columns:1fr 1fr;gap:10px 18px;align-items:center}.notebook-panel .eyebrow,.notebook-panel h2{grid-column:1/-1}.notebook-panel .small{margin:0}}@media(max-width:820px){.course-layout{display:block}.course-nav{position:static;display:flex;flex-wrap:wrap;gap:4px;max-height:none}.course-nav .eyebrow{width:100%}.course-nav hr{display:none}.notebook-panel{margin:15px 0;display:block}.course-intro{padding-top:32px}}@media(max-width:560px){.course-main{padding:0 4% 32px}.course-intro h1{font-size:2.5rem}.course-section,.exercise{padding:20px 16px}.code-block pre{font-size:.72rem;padding:14px}.concept{padding:14px}}''',encoding='utf8')
    with (ROOT/'assets'/'course.css').open('a',encoding='utf8') as css:
        css.write('''
/* Séquences guidées du premier bloc */
.course-layout.tp-layout{grid-template-columns:195px minmax(0,1fr)}
.learning-sequence{padding:22px;margin:16px 0 24px;border:1px solid var(--line);border-radius:16px;background:#fff}
.learning-sequence>h2{margin-top:0}
.learning-sequence>h3{margin-bottom:6px}
.learning-sequence>.exercise{margin:18px 0 12px}
.learning-sequence h4{margin:20px 0 7px;font-size:1rem;color:var(--green)}
.course-graphic{margin:22px 0;padding:18px;border:1px solid #d9e0d3;border-radius:14px;background:#fff}
.course-graphic svg{display:block;width:100%;height:auto}
.course-graphic figcaption{margin-top:10px;color:var(--muted);font-size:.78rem;line-height:1.5}
.figsize-table-wrap{max-width:100%;overflow-x:auto;margin:18px 0}
.figsize-table-wrap table{width:100%;min-width:0;table-layout:fixed;border-collapse:collapse}
.figsize-table-wrap th,.figsize-table-wrap td{padding:10px 12px;border:1px solid var(--line);text-align:left;overflow-wrap:anywhere}
.figsize-table-wrap th{background:#edf1e3;font-size:.78rem}
.figsize-table-wrap td{font-size:.82rem}
.qcm-section{background:#e8def6;border:1px solid #b7a2d6;border-top:7px solid #66518f;box-shadow:0 8px 24px #66518f20}
.qcm-section h2,.qcm-section h3,.qcm-section .eyebrow{color:#514071}
.qcm-section .button.primary{background:#66518f;border-color:#66518f;color:white}
.qcm-form{padding:0;border:0;border-radius:0;background:transparent;box-shadow:none}
.quiz-page{max-width:960px;min-width:0;padding:0 5% 60px}
.quiz-page .course-intro{width:100%;max-width:900px;margin:0 auto;padding-left:0;padding-right:0}
.quiz-page .qcm-form{box-sizing:border-box;width:100%;max-width:900px;margin:0 auto;padding:0}
.quiz-page #quiz-progress{font-size:.8rem;font-weight:700;color:var(--green);margin:0 0 18px}
.quiz-page .qcm-form fieldset{box-sizing:border-box;width:100%;min-width:0;max-width:100%;min-height:0;margin:0;padding:16px 0 20px;border:0;border-radius:0;background:transparent}
.quiz-page .qcm-form legend{display:block;width:100%;font-size:1.12rem;line-height:1.5;padding:0 0 14px;white-space:normal;overflow-wrap:anywhere}
.quiz-page .qcm-form .quiz-option{box-sizing:border-box;width:100%;align-items:flex-start;min-width:0;max-width:100%;margin:8px 0;padding:14px;border-color:var(--line);border-radius:11px;background:#fff}
.quiz-page .qcm-form .quiz-option:hover{background:var(--soft);border-color:var(--green)}
.qcm-form .quiz-option input{flex:0 0 17px;margin-top:.25em}
.quiz-page .qcm-form .quiz-option span{flex:1 1 0;min-width:0;overflow-wrap:anywhere}
.quiz-page .qcm-form .quiz-feedback{box-sizing:border-box;max-width:100%;padding:16px 18px;line-height:1.7;border:0;overflow-wrap:anywhere}
.qcm-form .quiz-feedback.correct{background:var(--soft)}
.qcm-form .quiz-feedback.incorrect{background:var(--orange-bg)}
.quiz-page .quiz-controls{display:flex;align-items:center;flex-wrap:wrap;gap:12px;margin-top:18px}
.quiz-controls .button{min-width:150px}
.qcm-form .quiz-option:has(input:checked){background:var(--soft);border-color:var(--green)}
.qcm-form .button.primary{background:var(--ink);border-color:var(--ink);color:white}
.qcm-form .button.primary:hover{background:var(--green);border-color:var(--green)}
.qcm-form .quiz-feedback{background:var(--soft)}
.qcm-path-card{display:flex;flex-direction:column;padding:0!important;overflow:hidden;background:#e8def6;border-color:#b7a2d6;box-shadow:0 6px 18px #66518f20}
.qcm-card-content,.qcm-course-link{display:flex;flex:1;flex-direction:column;padding:24px;text-decoration:none;color:inherit}
.qcm-inline-link{display:flex;justify-content:space-between;align-items:center;padding:13px 24px;background:#66518f;color:white;font-weight:700;font-size:.78rem;text-decoration:none}
.qcm-inline-link:hover{background:#514071}
.home-path-section{min-width:0}
.home-path-section>.path-grid{grid-template-columns:repeat(4,minmax(0,1fr));align-items:stretch}
.home-path-section .path-card{min-width:0;max-width:100%;overflow-wrap:anywhere}
.home-path-section .path-card>*{min-width:0;max-width:100%}
.home-path-section .card-top{align-items:flex-start;flex-wrap:wrap}
.home-path-section .pill{max-width:100%;white-space:normal;overflow-wrap:anywhere}
.home-path-section .path-card h3,.home-path-section .path-card p{overflow-wrap:anywhere}
.home-path-section .qcm-card-content,.home-path-section .qcm-course-link{width:100%;min-width:0;box-sizing:border-box}
.home-path-section .qcm-inline-link{gap:8px;flex-wrap:wrap;overflow-wrap:anywhere}
.qcm-form fieldset,.qcm-form legend,.qcm-form .quiz-option,.qcm-form .quiz-option>span{min-width:0;max-width:100%;overflow-wrap:anywhere}
@media(max-width:1100px){.home-path-section>.path-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:760px){.home-path-section>.path-grid{grid-template-columns:minmax(0,1fr)}}
@media(max-width:560px){.learning-sequence{padding:16px 12px}.quiz-page{padding:0 4% 32px}.quiz-page .course-intro{padding-top:32px}.quiz-page .qcm-form legend{font-size:1rem}.quiz-page .quiz-controls .button{min-width:0;flex:1 1 100%}}
''')
    (ROOT/'README.md').write_text('''# Le labo Matplotlib — parcours Superstore\n\nLe support source est [l’accueil du parcours](index.html). Il reprend les couleurs, la typographie et les composants TABLEAU (`site.css` et `tableau.css`, copiés sans modification), sans en reprendre les leçons. Le style complémentaire reste dans `assets/course.css`.\n\n## Données\n\nLe classeur utilisé est `data/sample_-_superstore.xls`, feuille `Orders`. Il contient 10 194 lignes et 21 colonnes ; une ligne décrit une ligne de commande, et un même Order ID peut se répéter.\n\n## Parcours\n\n- QCM de réactivation, puis [découverte de cinq graphiques](supports/00_decouvrir_graphiques.html) sur de petits DataFrames fictifs.\n- Blocs 01 à 04 : socle du matin, de la vérification des données à la variation mensuelle.\n- TP en binômes : 14 h–15 h 30.\n- Cumuls, moyenne mobile et boxplots : approfondissements autonomes.\n\nLes cours ne lient pas de notebook prérempli. Les apprenants ouvrent JupyterLab et créent leur propre notebook. Les corrections formateur restent dans `formateur/notebooks/`, hors de la sandbox.\n\n## Lancer JupyterLab avec Docker\n\nDepuis la racine du dépôt :\n\n```bash\ncd sandbox-notebook\ndocker compose up --build -d\ndocker compose logs notebook\n```\n\nOuvrir http://localhost:8890/lab et utiliser le jeton affiché dans les journaux. Le classeur Superstore est monté en lecture seule sous `/workspace/data`; les exports vont dans `/workspace/resultats`. Le lecteur `xlrd` est nécessaire à la lecture du `.xls`.\n\n## Régénérer les supports\n\n```bash\npython scripts/construire.py\n```\n\nLa feuille CSS `site.css` et la feuille de thème `tableau.css` sont conservées à l’identique.\n''',encoding='utf8')
    with (ROOT/'README.md').open('a',encoding='utf8') as readme:
        readme.write('''\n## Progression des exercices\n\nLe parcours conserve 21 exercices autonomes. Le bloc 01 travaille les comptages annuels ; les regroupements mensuels commencent au bloc 04. Dans le bloc 02, une part du total précède la comparaison de deux contributions. Les exercices du bloc 03 appliquent les indicateurs à des sous-catégories, des segments et une région filtrée. Le bloc 05 fait changer de référence et recommencer les cumuls sur une année réelle. Les consignes étudiantes ne contiennent ni amorce de code ni correction sous les exercices.\n''')
        readme.write('''\n## Données du TP Power BI\n\nLe TP utilise un autre jeu, fictif : [ventes_reseau_powerbi.csv](data/ventes_reseau_powerbi.csv). Il décrit les ventes 2025 du réseau Nova par date, région, canal, catégorie et produit. Le chiffre d’affaires et le coût d’achat, exprimés en euros HT, permettent de calculer une marge commerciale. Les apprenants créent quatre graphiques avec Pandas et Matplotlib et rédigent exactement deux insights chiffrés pour préparer un futur tableau de bord Power BI.\n\nLes données se régénèrent avec `python scripts/generer_donnees_tp.py` (graine fixe `20261027`). `python scripts/construire.py` copie le CSV dans la sandbox et régénère le sujet et les corrections formateur.\n''')
    shared=ROOT.parent/'sandbox-notebook'
    for filename in ('sample_-_superstore.xls',TP['data_file']):
        (shared/'data'/filename).write_bytes((ROOT/'data'/filename).read_bytes())
    print('Cours généré ; les notebooks étudiants se créent directement dans JupyterLab.')

if __name__=='__main__':main()
