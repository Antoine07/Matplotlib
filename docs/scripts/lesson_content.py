"""Exemples guidés et exercices complémentaires sur Orders."""


def apply_lessons(pages, solutions, make_lesson, g):
    hbar = lambda title, values, unit='': dict(
        kind='hbar', title=title, values=values, unit=unit,
        caption='Graphique calculé sur la feuille Orders du classeur Superstore.')
    group = lambda title, first, second, unit='', palette=None, reverse_rows=False: dict(
        kind='grouped', title=title, series={first[0]: first[1], second[0]: second[1]},
        unit=unit, palette=palette, reverse_rows=reverse_rows,
        caption='Les deux séries sont calculées sur le même périmètre.')
    line = lambda title, series, unit='': dict(
        kind='line', title=title, series=series, unit=unit,
        caption='Chaque point correspond à une période mensuelle de la feuille Orders.')
    diverge = lambda title, values, unit='': dict(
        kind='diverging', title=title, values=values, unit=unit,
        caption='La ligne zéro distingue les valeurs positives et négatives.')
    monthbar = lambda title, values, unit='': dict(
        kind='monthbar', title=title, values=values, unit=unit,
        caption='Les périodes restent dans l’ordre chronologique.')
    box = lambda title, summaries: dict(
        kind='box', title=title, summaries=summaries,
        caption='Repères de distribution calculés sur le jeu de données réel.')
    step = lambda name, explanation, code: (name, explanation, code)

    def add(key, items):
        page = next(p for p in pages if p['file'] == key)
        page['sequences'] = items
        page['exercises'] = [
            (s['exercise_title'], s['prompt'], s['deliverable'], s['starter'], s['answer'])
            for s in items
        ]
        solutions[key] = [s['solution'] for s in items]

    cats = {'Furniture': 754747.76, 'Office Supplies': 731893.31, 'Technology': 839893.28}
    regions = {'Central': 503170.67, 'East': 691828.17, 'South': 391721.91, 'West': 739813.61}
    profits = {'Furniture': 19730.00, 'Office Supplies': 126023.43, 'Technology': 146543.38}
    rprofits = {'Central': 39865.31, 'East': 94883.26, 'South': 46749.43, 'West': 110798.80}
    sub_sales = g['SUBCATEGORY_SALES']
    sub_profit = g['SUBCATEGORY_PROFIT']
    months = g['MONTH_SALES']
    month_profit = g['MONTH_PROFIT']
    labels = g['MONTH_LABELS']
    monthly = lambda values: dict(zip(labels, values))
    pct = [(months[i] / months[i-1] - 1) * 100 for i in range(1, len(months))]
    diff = [months[i] - months[i-1] for i in range(1, len(months))]
    cum = [sum(months[:i+1]) for i in range(len(months))]
    fixed = [(value / months[0] - 1) * 100 for value in months]
    moving = [None, None] + [sum(months[i-2:i+1]) / 3 for i in range(2, len(months))]
    margin_cum = [sum(month_profit[:i+1]) / sum(months[:i+1]) * 100 for i in range(len(months))]

    add('01_explorer', [
        make_lesson('Charger et décrire la feuille Orders', [
            step('Étape 1 — Contrôler le tableau', 'Vérifiez les dimensions et les colonnes après le chargement du classeur.', "print(orders.shape)\nprint(orders.columns.tolist())"),
            step('Étape 2 — Compter les observations', 'Comparez le nombre de lignes au nombre d’identifiants de commande distincts.', "print('Lignes :', len(orders))\nprint('Commandes distinctes :', orders['Order ID'].nunique())\nprint('Catégories :', orders['Category'].nunique())"),
        ], 'La feuille contient 10 194 lignes pour 5 111 commandes distinctes. Une ligne décrit une ligne de commande ; un même Order ID peut se répéter.', 'Compter les sous-catégories distinctes',
        'Combien de sous-catégories différentes sont présentes dans la feuille Orders ?',
        'Le nombre de sous-catégories distinctes et la ligne de code utilisée.',
        "# Écrivez ici votre calcul du nombre de sous-catégories distinctes",
        "nombre_sous_categories = orders['Sub-Category'].nunique()\nprint('Sous-catégories distinctes :', nombre_sous_categories)",
        'La feuille contient 17 sous-catégories distinctes. nunique() compte les valeurs différentes de la colonne Sub-Category.',
        None),
        make_lesson('Comparer lignes et commandes par catégorie', [
            step('Étape 1 — Calculer les deux comptages', 'Pour chaque catégorie, comptez les lignes de commande et les identifiants Order ID distincts.', '''# Regrouper les lignes par catégorie et compter les commandes
par_categorie = orders.groupby("Category")["Order ID"].agg(
    lignes="size",       # Nombre de lignes de commande
    commandes="nunique"  # Nombre de commandes distinctes
)

# Afficher les deux comptages par catégorie
print(par_categorie)'''),
            step('Étape 2 — Construire les barres groupées', 'Les deux séries partagent le même axe. Vert et lime distinguent les lignes des commandes distinctes, dont les valeurs sont affichées au bout des barres.', '''# Création d'une figure et de ses axes
# figsize définit la largeur et la hauteur en pouces
fig, ax = plt.subplots(figsize=(9, 4))

# Positions verticales des catégories : 0, 1, 2...
y = range(len(par_categorie))

# Première série : nombre de lignes par catégorie
# +0.18 décale les barres vers le haut
# height définit l'épaisseur des barres
b1 = ax.barh(
    [i + 0.18 for i in y],
    par_categorie["lignes"],
    height=0.36,
    label="Lignes",
    color="#275c47"
)

# Deuxième série : nombre de commandes distinctes
# -0.18 décale les barres vers le bas
b2 = ax.barh(
    [i - 0.18 for i in y],
    par_categorie["commandes"],
    height=0.36,
    label="Commandes distinctes",
    color="#b5cf66"
)

# Affichage des valeurs numériques au bout des barres
# padding=3 définit un espacement de 3 points
ax.bar_label(b1, padding=3)
ax.bar_label(b2, padding=3)

# Remplacement des positions 0, 1, 2...
# par les véritables noms des catégories
ax.set_yticks(list(y), par_categorie.index)

# Titre du graphique et nom de l'axe horizontal
ax.set(
    title="Lignes et commandes par catégorie",
    xlabel="Nombre"
)

# Affichage de la légende
ax.legend()

# Ajout d'une marge horizontale de 12 %
# pour laisser de la place aux valeurs affichées
ax.margins(x=0.12)

# Ajustement automatique des espacements
plt.tight_layout()

# Affichage du graphique
plt.show()''')],
            'Office Supplies compte le plus de lignes et de commandes distinctes dans cette ventilation. Les commandes peuvent apparaître dans plusieurs catégories : les comptes par catégorie ne s’additionnent donc pas au total général.',
            'Comparer les écarts par région', 'Dans quelle région l’écart entre lignes et commandes distinctes est-il le plus grand ?',
            'La région, les deux comptages, l’écart et une phrase qui interprète cet écart.',
            "par_region = orders.groupby('Region').agg(lignes=('Order ID','size'), commandes=('Order ID','nunique'))\n# Compléter avec le calcul de l'écart puis identifier le maximum",
            "par_region = orders.groupby('Region').agg(lignes=('Order ID','size'), commandes=('Order ID','nunique'))\npar_region['ecart'] = par_region['lignes'] - par_region['commandes']\nprint(par_region.loc[par_region['ecart'].idxmax()])",
            'West a le plus grand écart : 3 253 lignes contre 1 635 commandes distinctes, soit 1 618 lignes de plus. Plusieurs lignes peuvent appartenir à une même commande.',
            group('Lignes et commandes distinctes par catégorie', ('Lignes',{'Furniture':2201,'Office Supplies':6128,'Technology':1865}), ('Commandes',{'Furniture':1819,'Office Supplies':3812,'Technology':1560}), 'comptes', palette=('#275c47','#b5cf66'))),
        make_lesson('Suivre le nombre de commandes par année', [
            step('Étape 1 — Extraire l’année et compter les commandes', 'Créez une colonne année, puis comptez les identifiants Order ID distincts pour chaque année.', '''# Ajouter l'année de chaque commande
orders["annee"] = orders["Order Date"].dt.year

# Compter les commandes distinctes par année
commandes_annee = orders.groupby("annee")["Order ID"].nunique()

print(commandes_annee)'''),
            step('Étape 2 — Tracer le résultat', 'Les barres comparent le nombre de commandes distinctes par année.', "fig, ax = plt.subplots(figsize=(8,4))\nax.barh(commandes_annee.index.astype(str), commandes_annee.values)\nax.set(title='Commandes distinctes par année', xlabel='Nombre de commandes')\nplt.show()")],
            'Le nombre de commandes distinctes augmente dans le fichier au fil des années. Ce constat descriptif ne suffit pas à attribuer une cause à cette évolution.',
            'Comparer les clients par année', 'Comment le nombre de clients distincts évolue-t-il selon les années ? Représentez le résultat.',
            'Un graphique annuel, les quatre effectifs de clients et une phrase de constat.',
            '',
            'clients_annee = orders.groupby("annee")["Customer ID"].nunique()\nprint(clients_annee)\nfig, ax = plt.subplots(figsize=(8, 4))\nax.bar(clients_annee.index.astype(str), clients_annee.values, color="#275c47")\nax.set(title="Clients distincts par année", xlabel="Année", ylabel="Nombre de clients")\nplt.tight_layout()\nplt.show()',
            'Les effectifs sont 605 en 2023, 577 en 2024, 653 en 2025 et 704 en 2026. Un même client peut être compté dans plusieurs années ; les effectifs annuels ne s’additionnent pas pour compter les clients uniques du fichier.',
            hbar('Commandes distinctes par année', {'2023':995,'2024':1053,'2025':1340,'2026':1723})),
    ])

    add('02_comparer', [
        make_lesson('Comparer les ventes par catégorie', [
            step('Étape 1 — Calculer les ventes', 'groupby rassemble les lignes d’une catégorie ; sum additionne les ventes.', "ventes = orders.groupby('Category')['Sales'].sum()\nprint(ventes)"),
            step('Étape 2 — Construire le graphique', 'index contient les catégories ; values contient les montants correspondants.', "ventes = ventes.sort_values()\nfig, ax = plt.subplots(figsize=(8,4))\nax.barh(ventes.index, ventes.values)\nax.set(title='Ventes par catégorie', xlabel='Ventes (unités monétaires)')\nplt.show()")],
            'Technology réalise le total de ventes le plus élevé, environ 839 893 unités monétaires. Le graphique décrit le chiffre d’affaires, pas la rentabilité.',
            'Comparer les ventes par région', 'Quelle région réalise le plus de ventes ? Reproduisez le calcul et construisez un graphique horizontal trié.',
            'Le graphique, son titre, l’unité sur l’axe et une phrase qui distingue constat et explication.',
            "ventes_region = orders.groupby('Region')['Sales'].sum().sort_values()\nfig, ax = plt.subplots(figsize=(8,4))\n# Ajouter les barres, le titre, l'unité et l'affichage",
            "ventes_region = orders.groupby('Region')['Sales'].sum().sort_values()\nfig, ax = plt.subplots(figsize=(8,4))\nax.barh(ventes_region.index, ventes_region.values)\nax.set(title='Ventes par région', xlabel='Ventes (unités monétaires)')\nplt.show()",
            'West arrive en tête avec environ 739 814 unités monétaires. Cette comparaison n’indique pas pourquoi les régions diffèrent.',
            hbar('Ventes par catégorie', cats)),
        make_lesson('Calculer une part du total', [
            step('Étape 1 — Calculer le dénominateur', 'Le total de la colonne Sales sert de référence commune aux catégories.', "ventes = orders.groupby('Category')['Sales'].sum()\ntotal = ventes.sum()\nprint(total)"),
            step('Étape 2 — Passer en pourcentage', 'Chaque part est le total de la catégorie divisé par le total général, multiplié par 100.', "part = ventes / total * 100\npart = part.sort_values()\nfig, ax = plt.subplots(figsize=(8,4))\nax.barh(part.index, part.values)\nax.set(title='Part des ventes par catégorie', xlabel='Part des ventes (%)')\nplt.show()")],
            'Les parts des catégories totalisent 100 %. Technology pèse environ 36,1 % des ventes du fichier.',
            'Calculer les parts régionales', 'Calculez la part de chaque région dans les ventes totales et représentez les quatre parts.',
            'Quatre parts, un graphique et une phrase vérifiant leur somme.',
            "ventes_region = orders.groupby('Region')['Sales'].sum()\npart_region = ...\nfig, ax = plt.subplots(figsize=(8,4))\n# Compléter le graphique des parts",
            "ventes_region = orders.groupby('Region')['Sales'].sum()\npart_region = ventes_region / ventes_region.sum() * 100\npart_region = part_region.sort_values()\nfig, ax = plt.subplots(figsize=(8,4))\nax.barh(part_region.index, part_region.values)\nax.set(title='Part des ventes par région', xlabel='Part des ventes (%)')\nplt.show()\nprint(part_region.sum())",
            'West pèse environ 31,8 % des ventes, devant East (29,7 %), Central (21,6 %) et South (16,8 %). Les parts font 100 % à l’arrondi près.',
            hbar('Part des ventes par région', {'South':16.8,'Central':21.6,'East':29.7,'West':31.8}, '%')),
        make_lesson('Comparer le poids des catégories dans ventes et profit', [
            step('Étape 1 — Calculer la part de chaque total', 'Réutilisez le calcul d’une part du total pour deux mesures différentes : les ventes et le profit.', 'bilan = orders.groupby("Category")[["Sales", "Profit"]].sum()\nparts = pd.DataFrame(index=bilan.index)\nparts["Sales"] = bilan["Sales"] / bilan["Sales"].sum() * 100\nparts["Profit"] = bilan["Profit"] / bilan["Profit"].sum() * 100\nprint(parts.round(1))'),
            step('Étape 2 — Tracer les deux parts', 'Chaque série totalise 100 %. Les barres groupées comparent le poids relatif de chaque catégorie.', "fig, ax = plt.subplots(figsize=(8,4))\ny = range(len(parts))\nax.barh([i-.18 for i in y], parts['Sales'], height=.36, label='Part des ventes')\nax.barh([i+.18 for i in y], parts['Profit'], height=.36, label='Part du profit')\nax.set_yticks(list(y), parts.index)\nax.set(title='Part de chaque catégorie dans les totaux', xlabel='Part (%)')\nax.legend()\nplt.show()")],
            'Technology pèse environ 36,1 % des ventes et 50,1 % du profit total. Les deux séries sont exprimées en parts de leur propre total, pas en montants directement comparables.',
            'Comparer les contributions régionales', 'Quelles régions pèsent davantage dans le profit total que dans les ventes totales ? Représentez l’écart entre les deux parts pour chaque région.',
            'Un graphique des quatre écarts en points de pourcentage et une phrase qui identifie les régions concernées.',
            '',
            'bilan_region = orders.groupby("Region")[["Sales", "Profit"]].sum()\npart_ventes = bilan_region["Sales"] / bilan_region["Sales"].sum() * 100\npart_profit = bilan_region["Profit"] / bilan_region["Profit"].sum() * 100\necarts = (part_profit - part_ventes).sort_values()\nprint(ecarts)\nfig, ax = plt.subplots(figsize=(8, 4))\nax.barh(ecarts.index, ecarts.values, color="#275c47")\nax.axvline(0, color="black", linewidth=1)\nax.set(title="Part du profit moins part des ventes", xlabel="Écart (points de pourcentage)")\nplt.tight_layout()\nplt.show()',
            'East (+2,72 points) et West (+6,11 points) pèsent davantage dans le profit que dans les ventes. Les écarts sont négatifs pour Central (−7,99 points) et South (−0,84 point). Une différence entre deux pourcentages s’exprime en points.',
            group('Part de chaque catégorie dans les totaux', ('Ventes',{'Furniture':32.5,'Office Supplies':31.5,'Technology':36.1}), ('Profit',{'Furniture':6.7,'Office Supplies':43.1,'Technology':50.1}))),
        make_lesson('Repérer les sous-catégories les plus vendues', [
            step('Étape 1 — Agréger et sélectionner', 'nlargest conserve les huit sous-catégories aux ventes les plus élevées.', "ventes_sous_cat = orders.groupby('Sub-Category')['Sales'].sum()\ntop8 = ventes_sous_cat.nlargest(8).sort_values()\nprint(top8)"),
            step('Étape 2 — Représenter un classement lisible', 'Les barres horizontales affichent les noms longs sans les incliner.', "fig, ax = plt.subplots(figsize=(9,5))\nax.barh(top8.index, top8.values)\nax.set(title='Huit premières sous-catégories', xlabel='Ventes (unités monétaires)')\nplt.show()")],
            'Chairs et Phones sont les sous-catégories les plus vendues parmi les huit affichées. Le classement ne dit pas lesquelles sont les plus profitables.',
            'Construire le classement des clients', 'Quels sont les cinq clients, identifiés par Customer ID, qui réalisent le plus de ventes ? Représentez leur classement.',
            'Un graphique trié des cinq clients, leurs montants de ventes et une phrase de constat.',
            '',
            'ventes_clients = orders.groupby("Customer ID")["Sales"].sum()\ntop5 = ventes_clients.nlargest(5).sort_values()\nprint(top5)\nfig, ax = plt.subplots(figsize=(9, 4))\nax.barh(top5.index, top5.values, color="#275c47")\nax.set(title="Les cinq clients réalisant le plus de ventes", xlabel="Ventes (unités monétaires)")\nplt.tight_layout()\nplt.show()',
            'Les cinq premiers clients sont SM-20320 (25 043,05), TC-20980 (19 052,22), RB-19360 (15 117,34), TA-21385 (14 595,62) et AB-10105 (14 473,57). Le classement porte sur les ventes cumulées par client dans le fichier.',
            hbar('Ventes des huit premières sous-catégories', {k:sub_sales[k] for k in ['Bookcases','Copiers','Accessories','Binders','Tables','Storage','Phones','Chairs']})),
    ])

    # Chaque démonstration est suivie d’un exercice autonome sur un autre périmètre.
    add('03_rentabilite', [
        make_lesson('Calculer le profit rapporté aux ventes', [
            step('Étape 1 — Agréger avant de diviser', 'Les deux sommes doivent porter sur la même catégorie et le même périmètre.', "bilan = orders.groupby('Category')[['Sales','Profit']].sum()\nbilan['Taux'] = bilan['Profit'] / bilan['Sales'] * 100\nprint(bilan.round(2))"),
            step('Étape 2 — Comparer les taux', 'Le graphique présente le profit rapporté aux ventes, en pourcentage.', "taux = bilan['Taux'].sort_values()\nfig, ax = plt.subplots(figsize=(8,4))\nax.barh(taux.index, taux.values)\nax.set(title='Profit rapporté aux ventes', xlabel='Profit / ventes (%)')\nplt.show()")],
            'Technology présente le ratio le plus élevé, environ 17,45 %. Ce ratio ne constitue pas un taux de marge commerciale : le coût d’achat n’est pas fourni.',
            'Comparer les taux des sous-catégories', 'Quelle sous-catégorie présente le plus fort ratio profit/ventes ? Calculez les ratios et représentez les sous-catégories sur un graphique trié.',
            'Un graphique en pourcentage et le nom de la sous-catégorie présentant le ratio le plus élevé, avec sa valeur.',
            '',
            'bilan_sous_categories = orders.groupby("Sub-Category")[["Sales", "Profit"]].sum()\nbilan_sous_categories["Taux"] = bilan_sous_categories["Profit"] / bilan_sous_categories["Sales"] * 100\ntaux = bilan_sous_categories["Taux"].sort_values()\nprint(taux)\nprint("Ratio le plus élevé :", taux.idxmax(), taux.max())\nfig, ax = plt.subplots(figsize=(9, 6))\nax.barh(taux.index, taux.values, color="#275c47")\nax.axvline(0, color="black", linewidth=1)\nax.set(title="Profit rapporté aux ventes par sous-catégorie", xlabel="Profit / ventes (%)")\nplt.tight_layout()\nplt.show()',
            'Labels présente le ratio le plus élevé, environ 43,90 %. Les ventes et les profits sont additionnés par sous-catégorie avant la division. Certains ratios sont négatifs car les profits agrégés correspondants sont négatifs.',
            hbar('Profit rapporté aux ventes par catégorie', {'Furniture':2.6,'Office Supplies':17.2,'Technology':17.4}, '%')),
        make_lesson('Comparer montant et ratio par région', [
            step('Étape 1 — Préparer le bilan régional', 'Une même table contient les ventes et les profits agrégés par région.', "bilan_region = orders.groupby('Region')[['Sales','Profit']].sum()\nbilan_region['Taux'] = bilan_region['Profit'] / bilan_region['Sales'] * 100\nprint(bilan_region.round(2))"),
            step('Étape 2 — Comparer les taux', 'L’axe en pourcentage permet de comparer les ratios régionaux.', "taux = bilan_region['Taux'].sort_values()\nfig, ax = plt.subplots(figsize=(8,4))\nax.barh(taux.index, taux.values)\nax.set(title='Profit rapporté aux ventes par région', xlabel='Profit / ventes (%)')\nplt.show()")],
            'West a le profit total et le ratio les plus élevés dans ce fichier. Un ratio et un montant sont deux indicateurs distincts.',
            'Comparer les segments de clientèle', 'Le segment qui génère le plus de profit total présente-t-il aussi le plus fort ratio profit/ventes ? Comparez les segments avec deux graphiques.',
            'Un graphique des profits, un graphique des ratios et une conclusion chiffrée.',
            '',
            'bilan_segment = orders.groupby("Segment")[["Sales", "Profit"]].sum()\nbilan_segment["Taux"] = bilan_segment["Profit"] / bilan_segment["Sales"] * 100\nprint(bilan_segment.round(2))\nprofits = bilan_segment["Profit"].sort_values()\nfig, ax = plt.subplots(figsize=(8, 4))\nax.barh(profits.index, profits.values, color="#275c47")\nax.set(title="Profit total par segment", xlabel="Profit (unités monétaires)")\nplt.tight_layout()\nplt.show()\ntaux = bilan_segment["Taux"].sort_values()\nfig, ax = plt.subplots(figsize=(8, 4))\nax.barh(taux.index, taux.values, color="#275c47")\nax.set(title="Profit rapporté aux ventes par segment", xlabel="Profit / ventes (%)")\nplt.tight_layout()\nplt.show()',
            'Consumer génère le plus de profit total (136 371,45), tandis que Home Office présente le plus fort ratio profit/ventes (14,02 %). Les deux indicateurs conduisent ici à des premières places différentes.',
            hbar('Profit rapporté aux ventes par région', {'Central':7.9,'South':11.9,'East':13.7,'West':15.0}, '%')),
        make_lesson('Afficher les profits négatifs', [
            step('Étape 1 — Totaliser par sous-catégorie', 'Après l’agrégation, loc[condition] sélectionne les sous-catégories dont le profit total est négatif.', 'profit_sous_cat = orders.groupby("Sub-Category")["Profit"].sum().sort_values()\nprint(profit_sous_cat.loc[profit_sous_cat < 0])'),
            step('Étape 2 — Tracer autour de zéro', 'La ligne verticale de référence distingue les deux signes.', "fig, ax = plt.subplots(figsize=(9,6))\nax.barh(profit_sous_cat.index, profit_sous_cat.values)\nax.axvline(0, color='black', linewidth=1)\nax.set(title='Profit par sous-catégorie', xlabel='Profit (unités monétaires)')\nplt.show()")],
            'Bookcases, Supplies et Tables ont un profit total négatif. Le graphique montre le résultat fourni par le jeu et n’en explique pas la cause.',
            'Analyser les pertes de la région West', 'Dans la région West, quelles sous-catégories ont un profit total négatif ? Représentez leurs pertes.',
            'Un graphique des sous-catégories concernées, leurs profits et une phrase précisant le périmètre étudié.',
            '',
            'orders_west = orders.loc[orders["Region"] == "West"]\nprofits_west = orders_west.groupby("Sub-Category")["Profit"].sum()\npertes = profits_west.loc[profits_west < 0].sort_values()\nprint(pertes)\nfig, ax = plt.subplots(figsize=(8, 4))\nax.barh(pertes.index, pertes.values, color="#275c47")\nax.axvline(0, color="black", linewidth=1)\nax.set(title="Sous-catégories à profit négatif dans West", xlabel="Profit (unités monétaires)")\nplt.tight_layout()\nplt.show()',
            'Dans West, Bookcases totalise −1 608,43 et Machines −541,71. Le résultat diffère de celui calculé sur l’ensemble du fichier : les profits sont agrégés après sélection de la région.',
            diverge('Profit total par sous-catégorie', sub_profit)),
        make_lesson('Comprendre le poids des lignes dans une moyenne', [
            step('Étape 1 — Calculer deux indicateurs différents', 'Le ratio des sommes pondère implicitement les taux par le montant des ventes ; la moyenne ligne à ligne ne le fait pas.', "lignes = orders.assign(taux=orders['Profit']/orders['Sales']*100)\nratio = orders.groupby('Region')[['Sales','Profit']].sum()\nratio['Ratio des sommes'] = ratio['Profit']/ratio['Sales']*100\nratio['Moyenne des taux'] = lignes.groupby('Region')['taux'].mean()\nprint(ratio[['Ratio des sommes','Moyenne des taux']].round(2))"),
            step('Étape 2 — Visualiser l’écart', 'Comparer les deux méthodes côte à côte permet d’observer les différences de pondération.', "comparaison = ratio[['Ratio des sommes','Moyenne des taux']]\ny = range(len(comparaison))\nfig, ax = plt.subplots(figsize=(8,4))\nax.barh([i-.18 for i in y], comparaison['Ratio des sommes'], height=.36, label='Ratio des sommes')\nax.barh([i+.18 for i in y], comparaison['Moyenne des taux'], height=.36, label='Moyenne par ligne')\nax.set_yticks(list(y), comparaison.index)\nax.axvline(0, color='black', linewidth=1)\nax.set(title='Deux calculs par région', xlabel='Pourcentage')\nax.legend()\nplt.show()")],
            'Dans Central, le ratio des sommes est positif alors que la moyenne des taux ligne à ligne est négative. Les deux agrégations ne répondent pas à la même question.',
            'Comparer les méthodes par catégorie', 'Dans quelle catégorie le ratio des sommes et la moyenne des taux par ligne s’écartent-ils le plus ? Comparez les deux indicateurs sur un graphique.',
            'Un graphique comparatif, la catégorie concernée, les deux taux et leur écart en points.',
            '',
            'orders["taux_ligne"] = orders["Profit"] / orders["Sales"] * 100\ncomparaison_categorie = orders.groupby("Category")[["Sales", "Profit"]].sum()\ncomparaison_categorie["Ratio des sommes"] = comparaison_categorie["Profit"] / comparaison_categorie["Sales"] * 100\ncomparaison_categorie["Moyenne des taux"] = orders.groupby("Category")["taux_ligne"].mean()\necarts = (comparaison_categorie["Ratio des sommes"] - comparaison_categorie["Moyenne des taux"]).abs()\nprint(comparaison_categorie[["Ratio des sommes", "Moyenne des taux"]].round(2))\nprint("Écart maximal :", ecarts.idxmax(), ecarts.max())\ny = range(len(comparaison_categorie))\nfig, ax = plt.subplots(figsize=(9, 4))\nax.barh([i + 0.18 for i in y], comparaison_categorie["Ratio des sommes"], height=0.36, label="Ratio des sommes", color="#275c47")\nax.barh([i - 0.18 for i in y], comparaison_categorie["Moyenne des taux"], height=0.36, label="Moyenne des taux", color="#b5cf66")\nax.set_yticks(list(y), comparaison_categorie.index)\nax.set(title="Deux méthodes de calcul par catégorie", xlabel="Taux (%)")\nax.legend()\nplt.tight_layout()\nplt.show()',
            'Office Supplies présente le plus grand écart : environ 17,22 % pour le ratio des sommes et 14,00 % pour la moyenne des taux, soit 3,22 points. La moyenne simple donne le même poids à chaque ligne, quel que soit son montant de ventes.',
            group('Ratio des sommes et moyenne des taux par ligne', ('Ratio des sommes',{'Central':7.9,'East':13.7,'South':11.9,'West':15.0}), ('Moyenne par ligne',{'Central':-10.5,'East':17.1,'South':16.4,'West':22.0}), '%')),
    ])

    add('04_temps_et_variations', [
        make_lesson('Agréger les ventes par mois', [
            step('Étape 1 — Utiliser une date comme index', 'resample crée des périodes mensuelles sur un index datetime. Une fois les mois calculés, loc["2023"] sélectionne les valeurs de cette année.', 'mensuel = orders.set_index("Order Date").resample("MS")["Sales"].sum()\nprint(mensuel.loc["2023"])'),
            step('Étape 2 — Tracer la série chronologique', 'Une courbe convient à une mesure ordonnée dans le temps.', "fig, ax = plt.subplots(figsize=(10,4))\nax.plot(mensuel.index, mensuel.values, marker='o')\nax.set(title='Ventes mensuelles', ylabel='Ventes (unités monétaires)')\nax.grid(axis='y', alpha=.25)\nplt.show()")],
            'La série contient 48 mois consécutifs. Le tracé montre des variations mensuelles ; il ne permet pas d’en déduire une cause.',
            'Étudier les commandes mensuelles de 2026', 'Quel mois de 2026 compte le plus de commandes distinctes ? Construisez le graphique du nombre de commandes pour les douze mois de cette année.',
            'Un graphique mensuel, le mois recherché et son nombre de commandes distinctes.',
            '',
            'commandes_mois = orders.set_index("Order Date").resample("MS")["Order ID"].nunique()\ncommandes_2026 = commandes_mois.loc["2026"]\nprint(commandes_2026)\nprint("Mois au plus haut :", commandes_2026.idxmax(), commandes_2026.max())\nfig, ax = plt.subplots(figsize=(10, 4))\nax.bar(commandes_2026.index, commandes_2026.values, width=20, color="#275c47")\nax.set(title="Commandes distinctes par mois en 2026", ylabel="Nombre de commandes")\nplt.tight_layout()\nplt.show()',
            'Novembre 2026 compte le plus de commandes distinctes : 262. Le comptage porte sur les identifiants Order ID distincts de chaque mois, et non sur le nombre de lignes.',
            line('Évolution des ventes mensuelles', {'Ventes':months}, 'unités monétaires')),
        make_lesson('Calculer une variation en pourcentage', [
            step('Étape 1 — Comparer deux périodes', 'pct_change mesure une variation relative par rapport à la période précédente.', "variation_pct = mensuel.pct_change() * 100\nprint(variation_pct.head())"),
            step('Étape 2 — Afficher les hausses et les baisses', 'La ligne zéro sépare les variations positives des négatives.', "variation_pct = variation_pct.dropna()\nfig, ax = plt.subplots(figsize=(10,4))\nax.bar(variation_pct.index, variation_pct.values, width=20)\nax.axhline(0, color='black', linewidth=1)\nax.set(title='Variation relative des ventes', ylabel='Variation (%)')\nplt.show()")],
            'pct_change renvoie une proportion ; ×100 l’exprime en pourcentage. Le premier mois est NaN, car aucune période précédente ne sert de référence.',
            'Repérer les hausses et les baisses', 'Quel mois présente la plus forte hausse relative ? Quel mois présente la plus forte baisse relative ?',
            'Les deux dates, leurs pourcentages et la référence utilisée.',
            "variation_pct = mensuel.pct_change() * 100\n# Identifier le maximum et le minimum en ignorant le premier NaN",
            "variation_pct = mensuel.pct_change() * 100\nprint(variation_pct.idxmax(), variation_pct.max())\nprint(variation_pct.idxmin(), variation_pct.min())",
            'Les pourcentages dépendent de la base du mois précédent. Une hausse élevée en pourcentage peut porter sur un montant modeste.',
            monthbar('Variation relative des ventes par mois', pct, '%')),
        make_lesson('Calculer une variation en montant', [
            step('Étape 1 — Soustraire le mois précédent', 'diff mesure le changement dans l’unité originale de Sales.', "variation_montant = mensuel.diff()\nprint(variation_montant.head())"),
            step('Étape 2 — Tracer les écarts', 'La même ligne zéro distingue les augmentations des diminutions.', "variation_montant = variation_montant.dropna()\nfig, ax = plt.subplots(figsize=(10,4))\nax.bar(variation_montant.index, variation_montant.values, width=20)\nax.axhline(0, color='black', linewidth=1)\nax.set(title='Écart de ventes d’un mois à l’autre', ylabel='Unités monétaires')\nplt.show()")],
            'diff et pct_change utilisent la même période de référence, mais diff s’exprime en unités monétaires alors que pct_change est relatif.',
            'Comparer deux façons de mesurer la hausse', 'Le mois de plus forte hausse en montant est-il aussi celui de plus forte hausse en pourcentage ?',
            'Les deux mois, leurs variations et une phrase qui compare leurs unités.',
            "variation_montant = mensuel.diff()\nvariation_pct = mensuel.pct_change() * 100\n# Identifier les deux hausses maximales",
            "variation_montant = mensuel.diff()\nvariation_pct = mensuel.pct_change() * 100\nprint(variation_montant.idxmax(), variation_montant.max())\nprint(variation_pct.idxmax(), variation_pct.max())",
            'Les maxima peuvent survenir à des dates différentes : l’un mesure un montant ajouté, l’autre un taux rapporté au mois précédent.',
            monthbar('Variation en montant des ventes par mois', diff, '')),
    ])

    # Les blocs facultatifs gardent le même format de démonstration et d’essai.
    add('05_cumuls', [
        make_lesson('Construire un cumul des ventes', [
            step('Étape 1 — Agréger les mois', 'Le cumul se calcule après avoir ordonné et totalisé les périodes.', "m = orders.set_index('Order Date').resample('MS')[['Sales','Profit']].sum()\nm['Sales_cumulees'] = m['Sales'].cumsum()\nprint(m[['Sales','Sales_cumulees']].head())"),
            step('Étape 2 — Tracer la progression', 'La courbe représente le total accumulé depuis le début.', "fig, ax = plt.subplots(figsize=(10,4))\nax.plot(m.index, m['Sales_cumulees'])\nax.set(title='Ventes cumulées', ylabel='Unités monétaires cumulées')\nplt.show()")],
            'Le cumul continue généralement à progresser même si un mois isolé baisse, car il ajoute les ventes de la période au total précédent.',
            'Contrôler le cumul final', 'Comparez le cumul du dernier mois à la somme de Sales dans le fichier.',
            'Deux montants et une phrase sur le périmètre couvert.',
            "m['Sales_cumulees'] = m['Sales'].cumsum()\nprint(m['Sales_cumulees'].iloc[-1], orders['Sales'].sum())",
            "m['Sales_cumulees'] = m['Sales'].cumsum()\nprint(m['Sales_cumulees'].iloc[-1], orders['Sales'].sum())",
            'Les montants sont égaux à l’arrondi près : le dernier cumul comprend toutes les ventes mensuelles.',
            line('Cumul des ventes', {'Cumul':cum}, 'unités monétaires')),
        make_lesson('Mesurer une évolution depuis une base fixe', [
            step('Étape 1 — Choisir la référence', 'Chaque montant mensuel est divisé par le montant de janvier 2023.', "evolution_base = (m['Sales'] / m['Sales'].iloc[0] - 1) * 100\nprint(evolution_base.head())"),
            step('Étape 2 — Représenter les écarts à la base', 'La ligne zéro correspond au mois de référence.', "fig, ax = plt.subplots(figsize=(10,4))\nax.plot(m.index, evolution_base)\nax.axhline(0, color='black', linewidth=1)\nax.set(title='Évolution par rapport au premier mois', ylabel='Évolution (%)')\nplt.show()")],
            'La base reste fixe. Cette mesure compare les montants mensuels entre eux ; elle ne représente pas le cumul des ventes.',
            'Changer l’année de référence', 'Comment les ventes évoluent-elles au cours de 2024 si janvier 2024 sert de référence ? Tracez l’évolution en pourcentage et interprétez la valeur de décembre.',
            'Une courbe sur les douze mois de 2024, la variation de décembre et une phrase qui nomme la référence.',
            '',
            'ventes_2024 = m.loc["2024", "Sales"]\nevolution_2024 = (ventes_2024 / ventes_2024.iloc[0] - 1) * 100\nprint(evolution_2024)\nfig, ax = plt.subplots(figsize=(10, 4))\nax.plot(evolution_2024.index, evolution_2024.values, color="#275c47")\nax.axhline(0, color="black", linewidth=1)\nax.set(title="Ventes de 2024, référence janvier 2024", ylabel="Évolution (%)")\nplt.tight_layout()\nplt.show()',
            'Le point de janvier 2024 vaut 0 %. En décembre, les ventes sont environ 309,13 % au-dessus de celles de janvier 2024. La référence est le montant mensuel de janvier 2024, sans cumul des ventes.',
            line('Évolution mensuelle, base initiale', {'Évolution':fixed}, '%')),
        make_lesson('Lisser une série avec rolling', [
            step('Étape 1 — Calculer une fenêtre mobile', 'Une fenêtre de trois observations calcule la moyenne des trois derniers mois.', "m['mobile_3'] = m['Sales'].rolling(3, min_periods=3).mean()\nprint(m[['Sales','mobile_3']].head())"),
            step('Étape 2 — Comparer les deux courbes', 'Le lissage atténue une partie des fluctuations observées.', "fig, ax = plt.subplots(figsize=(10,4))\nax.plot(m.index, m['Sales'], alpha=.5, label='Ventes mensuelles')\nax.plot(m.index, m['mobile_3'], label='Moyenne mobile 3 mois')\nax.set(title='Ventes et moyenne mobile', ylabel='Unités monétaires')\nax.legend()\nplt.show()")],
            'Les deux premières valeurs sont absentes avec une fenêtre complète de trois mois. La moyenne mobile décrit les observations passées ; elle n’est pas une prévision.',
            'Vérifier une moyenne mobile à la main', 'Calculez la moyenne des ventes de janvier à mars 2023 puis comparez-la à rolling(3).',
            'Le calcul manuel, la valeur calculée et le nombre d’observations de la fenêtre.',
            "m['mobile_3'] = m['Sales'].rolling(3, min_periods=3).mean()\nprint(m.loc['2023-03-01','mobile_3'])",
            "print(m['Sales'].iloc[:3].mean())\nprint(m.loc['2023-03-01','mobile_3'])",
            'Les deux valeurs coïncident : la moyenne de mars 2023 comprend janvier, février et mars.',
            line('Ventes et moyenne mobile 3 mois', {'Ventes':months,'Moyenne mobile':moving}, 'unités monétaires')),
        make_lesson('Calculer un ratio sur des cumuls', [
            step('Étape 1 — Cumuler les deux mesures', 'Le profit cumulé et les ventes cumulées doivent couvrir les mêmes mois.', "m['Profit_cumule'] = m['Profit'].cumsum()\nm['Sales_cumulees'] = m['Sales'].cumsum()\nm['Taux_cumule'] = m['Profit_cumule'] / m['Sales_cumulees'] * 100\nprint(m[['Profit_cumule','Sales_cumulees','Taux_cumule']].tail())"),
            step('Étape 2 — Tracer le ratio', 'Le graphique montre un taux calculé sur les cumuls, pas une moyenne de taux mensuels.', "fig, ax = plt.subplots(figsize=(10,4))\nax.plot(m.index, m['Taux_cumule'])\nax.set(title='Profit cumulé rapporté aux ventes cumulées', ylabel='Profit / ventes (%)')\nplt.show()")],
            'Le ratio cumulé rapporte le profit accumulé aux ventes accumulées sur la même période. Chaque mois contribue selon son montant de ventes ; une moyenne de taux mensuels donne le même poids à tous les mois.',
            'Recommencer les cumuls en janvier 2024', 'Comment le ratio profit cumulé/ventes cumulées évolue-t-il pendant 2024 ? Tracez-le en recommençant les cumuls en janvier, puis comparez sa valeur de décembre à la moyenne des taux mensuels de 2024.',
            'Une courbe du ratio cumulé sur 2024, les deux taux de fin d’analyse et une explication de leur différence.',
            '',
            'bilan_2024 = m.loc["2024", ["Sales", "Profit"]].copy()\nbilan_2024["Sales_cumulees"] = bilan_2024["Sales"].cumsum()\nbilan_2024["Profit_cumule"] = bilan_2024["Profit"].cumsum()\nbilan_2024["Taux_cumule"] = bilan_2024["Profit_cumule"] / bilan_2024["Sales_cumulees"] * 100\nbilan_2024["Taux_mensuel"] = bilan_2024["Profit"] / bilan_2024["Sales"] * 100\nprint("Ratio cumulé en décembre :", bilan_2024["Taux_cumule"].iloc[-1])\nprint("Moyenne des taux mensuels :", bilan_2024["Taux_mensuel"].mean())\nfig, ax = plt.subplots(figsize=(10, 4))\nax.plot(bilan_2024.index, bilan_2024["Taux_cumule"], color="#275c47")\nax.set(title="Profit cumulé / ventes cumulées en 2024", ylabel="Ratio (%)")\nplt.tight_layout()\nplt.show()',
            'Le ratio cumulé atteint environ 13,11 % en décembre 2024, contre 12,25 % pour la moyenne des taux mensuels. Les cumuls commencent en janvier 2024. Le premier calcul pondère les mois par leurs ventes, tandis que le second donne le même poids à chaque mois.',
            line('Profit cumulé / ventes cumulées', {'Ratio cumulé':margin_cum}, '%')),
    ])

    add('06_distributions', [
        make_lesson('Lire les quartiles d’un boxplot', [
            step('Étape 1 — Préparer une observation par ligne', 'Ici le grain reste la ligne de commande ; les profits sont comparés par catégorie.', "categories = sorted(orders['Category'].unique())\nseries = [orders.loc[orders['Category'].eq(c),'Profit'].dropna() for c in categories]\nprint([s.median() for s in series])"),
            step('Étape 2 — Construire le boxplot', 'La boîte décrit les quartiles ; les points éloignés restent des observations à vérifier.', "fig, ax = plt.subplots(figsize=(9,4))\nax.boxplot(series, tick_labels=categories, orientation='horizontal', showfliers=True)\nax.axvline(0, color='black', linewidth=1)\nax.set(title='Profit par ligne de commande', xlabel='Profit (unités monétaires)')\nplt.show()")],
            'La médiane de Technology est plus élevée, mais le boxplot montre aussi l’étalement et les valeurs atypiques. Chaque observation reste une ligne de commande.',
            'Décrire une catégorie', 'Choisissez une catégorie et relevez sa médiane, ses quartiles et le nombre de lignes à profit négatif.',
            'Quatre valeurs ou constats et une phrase qui nomme le grain.',
            "s = orders.loc[orders['Category'].eq('Technology'),'Profit']\nprint(s.median(), s.quantile([.25,.75]), (s<0).sum())",
            "s = orders.loc[orders['Category'].eq('Technology'),'Profit']\nprint('Médiane :',s.median())\nprint('Quartiles :',s.quantile([.25,.75]))\nprint('Lignes négatives :',(s<0).sum())",
            'Les indicateurs décrivent les profits par ligne de commande. Ils ne donnent pas directement le profit par commande complète.',
            box('Profit par ligne : min, quartiles et max', {'Furniture':[-1862.31,-12.75,8.04,33.73,1013.13],'Office Supplies':[-3701.89,2.13,6.89,19.31,4946.37],'Technology':[-6599.98,5.22,25.02,74.81,8399.98]})),
        make_lesson('Changer le grain : une observation par commande', [
            step('Étape 1 — Additionner les lignes d’une commande', 'Order ID regroupe toutes les lignes d’une commande avant de tracer sa distribution.', "profit_commande = orders.groupby('Order ID')['Profit'].sum()\nprint(profit_commande.describe())"),
            step('Étape 2 — Comparer les distributions', 'Le boxplot porte maintenant sur les commandes agrégées.', "fig, ax = plt.subplots(figsize=(7,4))\nax.boxplot([profit_commande], tick_labels=['Commandes'], orientation='horizontal', showfliers=True)\nax.axvline(0, color='black', linewidth=1)\nax.set(title='Profit par commande', xlabel='Profit (unités monétaires)')\nplt.show()")],
            'Le grain change : chaque observation résume désormais un Order ID. Une commande peut réunir des lignes positives et négatives.',
            'Comparer les profits négatifs', 'Combien de commandes ont un profit total négatif ? Quelle part des lignes a un profit négatif ?',
            'Deux comptes et deux proportions calculés au bon grain.',
            "profit_commande = orders.groupby('Order ID')['Profit'].sum()\nprint((profit_commande<0).sum())\nprint((orders['Profit']<0).mean()*100)",
            "profit_commande = orders.groupby('Order ID')['Profit'].sum()\nprint('Commandes négatives :',(profit_commande<0).sum())\nprint('Part des commandes :',(profit_commande<0).mean()*100)\nprint('Part des lignes :',(orders['Profit']<0).mean()*100)",
            'Environ 1 040 commandes sur 5 111 ont un profit négatif (20,3 %). La part des lignes négatives est différente, car le grain change.',
            box('Profit par commande : min, quartiles et max', {'Commandes':[-6892.37,2.05,16.24,68.67,8762.39]})),
        make_lesson('Comparer médiane et moyenne', [
            step('Étape 1 — Calculer les deux repères', 'La médiane résiste davantage aux valeurs extrêmes ; la moyenne les intègre.', "resume = orders.groupby('Category')['Profit'].agg(mediane='median', moyenne='mean')\nprint(resume)"),
            step('Étape 2 — Représenter les résultats', 'Une comparaison côte à côte fait apparaître les écarts entre les deux indicateurs.', "fig, ax = plt.subplots(figsize=(8,4))\ny = range(len(resume))\nax.barh([i-.18 for i in y], resume['mediane'], height=.36, label='Médiane')\nax.barh([i+.18 for i in y], resume['moyenne'], height=.36, label='Moyenne')\nax.set_yticks(list(y), resume.index)\nax.set(title='Profit moyen et médian par ligne', xlabel='Unités monétaires')\nax.legend()\nplt.show()")],
            'Un écart important entre moyenne et médiane peut signaler une distribution asymétrique ou influencée par des valeurs extrêmes ; il ne prouve pas une erreur.',
            'Calculer un écart moyen-médian', 'Dans quelle catégorie la moyenne est-elle la plus éloignée de la médiane ?',
            'La catégorie, les deux valeurs et une interprétation sans attribuer de cause.',
            "resume = orders.groupby('Category')['Profit'].agg(mediane='median', moyenne='mean')\n# Comparer l'écart absolu entre moyenne et médiane",
            "resume = orders.groupby('Category')['Profit'].agg(mediane='median', moyenne='mean')\nresume['ecart'] = (resume['moyenne']-resume['mediane']).abs()\nprint(resume.loc[resume['ecart'].idxmax()])",
            'La moyenne est sensible aux valeurs extrêmes et peut s’éloigner de la médiane. Les deux statistiques décrivent les profits des lignes de commande.',
            group('Profit moyen et médian par ligne', ('Médiane',{'Furniture':8.04,'Office Supplies':6.89,'Technology':25.02}), ('Moyenne',{'Furniture':8.96,'Office Supplies':20.57,'Technology':78.58}))),
    ])
