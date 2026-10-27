"""Bloc de présentation : cinq graphiques, sans fichier ni exercice.

Les cellules Pandas, les tableaux HTML et les illustrations SVG partagent les
mêmes données fictives. Le générateur web ne dépend pas de Matplotlib.
"""
import html
from statistics import quantiles


GREEN = '#275c47'
LIME = '#b5cf66'
DISCOVERY = dict(
    file='00_decouvrir_graphiques',
    title='Découvrir cinq graphiques',
    intro='Cinq questions, cinq petits DataFrames et cinq représentations pour choisir un graphique avant de travailler sur Superstore.',
)

EXAMPLES = [
    dict(
        id='barres', title='Barres horizontales : comparer des catégories',
        question='Quel produit réalise le plus de ventes ?',
        variable='produits',
        data={'Produit': ['Clavier', 'Souris', 'Écran', 'Casque'],
              'Ventes': [1200, 800, 2100, 1100]},
        grain='Une ligne représente un produit ; Ventes contient son total de ventes en euros.',
        chart_title='Ventes par produit', xlabel='Ventes (€)', ylabel='Produit',
        plotting='''# Créer une figure de 8 × 4 pouces, à 100 DPI
fig, ax = plt.subplots(figsize=(8, 4), dpi=100)

# Les noms placent les barres ; les montants fixent leur longueur
barres = ax.barh(produits["Produit"], produits["Ventes"], color="#275c47")
ax.bar_label(barres, padding=3)

# Nommer le graphique et laisser de la place aux valeurs
ax.set(title="Ventes par produit", xlabel="Ventes (€)", ylabel="Produit")
ax.margins(x=0.15)
plt.tight_layout()
plt.show()''',
        reading='Écran réalise le plus de ventes : 2 100 €. La longueur des barres compare les montants ; l’axe numérique commence à zéro.',
        use='Comparer des catégories ou lire un classement, notamment lorsque les noms sont longs.',
        bridge='Dans Power BI : graphique en barres groupées, avec une seule mesure.',
    ),
    dict(
        id='colonnes', title='Colonnes groupées : comparer deux séries',
        question='Quel magasin gagne le plus de chiffre d’affaires entre 2024 et 2025 ?',
        variable='magasins',
        data={'Magasin': ['Centre', 'Nord', 'Sud'],
              'CA_2024': [80, 65, 90], 'CA_2025': [100, 95, 105]},
        grain='Une ligne représente un magasin ; les deux colonnes de chiffre d’affaires sont exprimées en milliers d’euros (k€).',
        chart_title='Chiffre d’affaires par magasin', xlabel='Magasin', ylabel='Chiffre d’affaires (k€)',
        plotting='''fig, ax = plt.subplots(figsize=(8, 4), dpi=100)

# Une position par magasin : 0, 1, 2
x = range(len(magasins))

# Décaler les deux séries pour les afficher côte à côte
ax.bar([i - 0.18 for i in x], magasins["CA_2024"],
       width=0.36, color="#275c47", label="2024")
ax.bar([i + 0.18 for i in x], magasins["CA_2025"],
       width=0.36, color="#b5cf66", label="2025")

# Remplacer les positions par les noms des magasins
ax.set_xticks(list(x), magasins["Magasin"])
ax.set(title="Chiffre d’affaires par magasin",
       xlabel="Magasin", ylabel="Chiffre d’affaires (k€)")
ax.legend()
plt.tight_layout()
plt.show()''',
        reading='Nord passe de 65 à 95 k€, soit un gain de 30 k€, le plus élevé des trois magasins. Sud reste celui qui réalise le plus de chiffre d’affaires en 2025.',
        use='Comparer plusieurs séries dans les mêmes catégories, avec la même unité.',
        bridge='Dans Power BI : graphique en colonnes groupées.',
    ),
    dict(
        id='courbe', title='Courbe : suivre une évolution',
        question='Les ventes augmentent-elles chaque mois ?',
        variable='mensuel',
        data={'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin'],
              'Ventes': [10, 12, 9, 15, 18, 16.5]},
        grain='Une ligne représente un mois ; les ventes sont exprimées en milliers d’euros. Les mois sont déjà dans l’ordre chronologique.',
        chart_title='Ventes mensuelles', xlabel='Mois', ylabel='Ventes (k€)',
        plotting='''fig, ax = plt.subplots(figsize=(8, 4), dpi=100)

# Relier les mois dans leur ordre ; un point marque chaque observation
ax.plot(mensuel["Mois"], mensuel["Ventes"],
        color="#275c47", marker="o")

ax.set(title="Ventes mensuelles", xlabel="Mois", ylabel="Ventes (k€)")
ax.set_ylim(0, 20)
ax.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.show()''',
        reading='Les ventes passent de 10 à 16,5 k€ entre janvier et juin, mais elles diminuent en mars et en juin. Une hausse sur l’ensemble de la période n’implique pas une hausse chaque mois.',
        use='Suivre une mesure dans le temps. L’ordre chronologique est essentiel pour interpréter la ligne.',
        bridge='Dans Power BI : graphique en courbes.',
    ),
    dict(
        id='nuage', title='Nuage de points : explorer une relation',
        question='Les magasins ayant un budget publicitaire élevé vendent-ils davantage ?',
        variable='publicite',
        data={'Magasin': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
              'Budget': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              'Ventes': [18, 25, 20, 35, 31, 45, 39, 50, 43, 58]},
        grain='Une ligne représente un magasin observé sur la même période ; Budget et Ventes sont exprimés en milliers d’euros.',
        chart_title='Budget publicitaire et ventes', xlabel='Budget publicitaire (k€)', ylabel='Ventes (k€)',
        plotting='''fig, ax = plt.subplots(figsize=(8, 4), dpi=100)

# Chaque ligne du DataFrame devient un point : budget en x, ventes en y
ax.scatter(publicite["Budget"], publicite["Ventes"],
           color="#275c47", s=65)

ax.set(title="Budget publicitaire et ventes",
       xlabel="Budget publicitaire (k€)", ylabel="Ventes (k€)")
ax.set_xlim(0, 11)
ax.set_ylim(0, 65)
ax.grid(alpha=0.25)
plt.tight_layout()
plt.show()''',
        reading='Les points suggèrent une relation positive : les budgets élevés s’accompagnent souvent de ventes élevées. Cela ne prouve pas que la publicité cause cette différence ; la taille des magasins pourrait aussi intervenir.',
        use='Explorer la relation entre deux mesures numériques. Chaque point doit représenter une observation identifiée.',
        bridge='Dans Power BI : graphique en nuages de points, avec un magasin par point.',
    ),
    dict(
        id='boxplot', title='Boxplot : comparer des distributions',
        question='Quel magasin présente les montants de commandes les plus dispersés ?',
        variable='commandes',
        data={'Centre': [90, 95, 100, 105, 110, 115, 120, 125, 130, 135],
              'Nord': [40, 60, 75, 90, 110, 130, 155, 180, 210, 350],
              'Sud': [80, 85, 90, 95, 100, 105, 110, 115, 120, 125]},
        grain='Chaque colonne contient les montants de dix commandes distinctes d’un magasin, en euros. Les commandes placées sur une même ligne n’ont pas de lien entre magasins.',
        chart_title='Montants des commandes par magasin', xlabel='Magasin', ylabel='Montant d’une commande (€)',
        plotting='''fig, ax = plt.subplots(figsize=(8, 4), dpi=100)

# Fournir plusieurs montants pour chaque boîte, pas un total par magasin
series = [commandes["Centre"], commandes["Nord"], commandes["Sud"]]

# La boîte contient la moitié centrale des montants ; le trait est la médiane
ax.boxplot(
    series,
    tick_labels=["Centre", "Nord", "Sud"],
    patch_artist=True,
    boxprops={"facecolor": "#b5cf66", "edgecolor": "#275c47"},
    medianprops={"color": "#275c47", "linewidth": 2}
)

ax.set(title="Montants des commandes par magasin",
       xlabel="Magasin", ylabel="Montant d’une commande (€)")
ax.set_ylim(0, 400)
plt.tight_layout()
plt.show()''',
        reading='Nord présente la boîte la plus étendue : ses montants sont plus dispersés. Le point isolé à 350 € est une valeur atypique selon la règle du boxplot ; il ne constitue pas automatiquement une erreur.',
        use='Comparer une médiane, une dispersion et des valeurs atypiques. La lecture des quartiles et des moustaches sera approfondie dans le bloc sur les distributions.',
        bridge='Dans Power BI : un boxplot peut être ajouté avec un visuel personnalisé. Dans Matplotlib, ax.boxplot() est disponible directement.',
        source='https://marketplace.microsoft.com/en-gb/product/power-bi-visuals/wa104380831?tab=overview',
    ),
]


def dataframe_code(example):
    """Créer le code affiché à partir des mêmes valeurs que le tableau et le SVG."""
    columns = ',\n'.join(f'    {name!r}: {values!r}' for name, values in example['data'].items())
    return f'{example["variable"]} = pd.DataFrame({{\n{columns}\n}})\n\nprint({example["variable"]})'


def _number(value):
    return f'{value:g}'.replace('.', ',') if isinstance(value, float) else str(value)


def _text(x, y, value, **attrs):
    options = ' '.join(f'{key.replace("_", "-")}="{html.escape(str(val), quote=True)}"' for key, val in attrs.items())
    return f'<text x="{x:.2f}" y="{y:.2f}" {options}>{html.escape(str(value))}</text>'


def _line(x1, y1, x2, y2, color='#ccd5ca', width=1):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{color}" stroke-width="{width}"/>'


def box_summary(values):
    """Quartiles linéaires et moustaches à 1,5 IQR, comme le boxplot Matplotlib."""
    q1, med, q3 = quantiles(values, n=4, method='inclusive')
    iqr = q3 - q1
    inside = [v for v in values if q1 - 1.5 * iqr <= v <= q3 + 1.5 * iqr]
    outside = [v for v in values if v not in inside]
    return min(inside), q1, med, q3, max(inside), outside


def graphic(example):
    """Illustration autonome, responsive, calculée sur les données de l’exemple."""
    left, right, top, bottom = 95, 755, 60, 330
    data = example['data']
    kind = example['id']
    title_id = 'graphique-' + kind
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" role="img" aria-labelledby="{title_id}" style="font-family:Arial,sans-serif;font-size:12px;fill:#263a34">',
           f'<title id="{title_id}">{html.escape(example["chart_title"])}</title>',
           f'<desc>{html.escape(example["reading"])}</desc>',
           '<rect width="800" height="400" fill="white"/>',
           _text(400, 25, example['chart_title'], text_anchor='middle', font_size=17, font_weight=700),
           _text(425, 381, example['xlabel'], text_anchor='middle', font_size=13),
           _text(20, 195, example['ylabel'], text_anchor='middle', font_size=13, transform='rotate(-90 20 195)')]

    if kind == 'barres':
        x = lambda value: left + value / 2415 * (right - left)
        for value in range(0, 2401, 400):
            out.append(_text(x(value), bottom + 22, value, text_anchor='middle'))
        for i, (label, value) in enumerate(zip(data['Produit'], data['Ventes'])):
            y = bottom - (i + 0.5) * (bottom - top) / 4
            out.extend([_text(left - 10, y + 4, label, text_anchor='end'),
                        f'<rect x="{left}" y="{y-22:.2f}" width="{x(value)-left:.2f}" height="44" fill="{GREEN}"/>',
                        _text(x(value) + 6, y + 4, value)])
    else:
        maximum = {'colonnes': 110.25, 'courbe': 20, 'nuage': 65, 'boxplot': 400}[kind]
        y = lambda value: bottom - value / maximum * (bottom - top)
        ticks = {'colonnes': range(0, 101, 20), 'courbe': range(0, 21, 5),
                 'nuage': range(0, 61, 10), 'boxplot': range(0, 401, 100)}[kind]
        for value in ticks:
            if kind in ('courbe', 'nuage'):
                out.append(_line(left, y(value), right, y(value), '#e7ebe3'))
            out.append(_text(left - 10, y(value) + 4, value, text_anchor='end'))

        if kind == 'colonnes':
            # Matplotlib ajoute une marge de 5 % autour des deux séries.
            x = lambda value: left + (value + 0.503) / 3.006 * (right - left)
            width = 0.36 / 3.006 * (right - left)
            for i, label in enumerate(data['Magasin']):
                out.append(_text(x(i), bottom + 22, label, text_anchor='middle'))
                for field, offset, color in [('CA_2024', -0.18, GREEN), ('CA_2025', 0.18, LIME)]:
                    value = data[field][i]
                    out.append(f'<rect x="{x(i+offset)-width/2:.2f}" y="{y(value):.2f}" width="{width:.2f}" height="{bottom-y(value):.2f}" fill="{color}"/>')
            for j, (label, color) in enumerate([('2024', GREEN), ('2025', LIME)]):
                out.extend([f'<rect x="{535+j*95}" y="45" width="14" height="10" fill="{color}"/>',
                            _text(554 + j * 95, 54, label)])
        elif kind == 'courbe':
            x = lambda i: left + (i + 0.25) / 5.5 * (right - left)
            points = ' '.join(f'{x(i):.2f},{y(v):.2f}' for i, v in enumerate(data['Ventes']))
            out.append(f'<polyline points="{points}" fill="none" stroke="{GREEN}" stroke-width="2"/>')
            for i, (label, value) in enumerate(zip(data['Mois'], data['Ventes'])):
                out.extend([f'<circle cx="{x(i):.2f}" cy="{y(value):.2f}" r="4" fill="{GREEN}"/>',
                            _text(x(i), bottom + 22, label, text_anchor='middle')])
        elif kind == 'nuage':
            x = lambda value: left + value / 11 * (right - left)
            for value in range(0, 11, 2):
                out.extend([_line(x(value), top, x(value), bottom, '#e7ebe3'),
                            _text(x(value), bottom + 22, value, text_anchor='middle')])
            for budget, ventes in zip(data['Budget'], data['Ventes']):
                out.append(f'<circle cx="{x(budget):.2f}" cy="{y(ventes):.2f}" r="5" fill="{GREEN}"/>')
        elif kind == 'boxplot':
            for i, (label, values) in enumerate(data.items()):
                x = left + (i + 0.5) / 3 * (right - left)
                lo, q1, med, q3, hi, fliers = box_summary(values)
                out.extend([_text(x, bottom + 22, label, text_anchor='middle'),
                            _line(x, y(lo), x, y(q1), '#000'),
                            _line(x, y(q3), x, y(hi), '#000'),
                            _line(x-16.5, y(lo), x+16.5, y(lo), '#000'),
                            _line(x-16.5, y(hi), x+16.5, y(hi), '#000'),
                            f'<rect x="{x-33}" y="{y(q3):.2f}" width="66" height="{y(q1)-y(q3):.2f}" fill="{LIME}" stroke="{GREEN}"/>',
                            _line(x-33, y(med), x+33, y(med), GREEN, 2)])
                for value in fliers:
                    out.append(f'<circle cx="{x}" cy="{y(value):.2f}" r="4" fill="none" stroke="#000"/>')

    out.extend([_line(left, top, left, bottom), _line(left, bottom, right, bottom), '</svg>'])
    return ''.join(out)


def build_discovery(root, head, foot, code, blocks_nav):
    sections = [('reperes', 'Avant de regarder les graphiques', '''<h2>Une question guide le choix du graphique</h2><p>Ces exemples utilisent de petits jeux de données fictives, indépendants de Superstore. Les tableaux sont déjà prêts à tracer : aucun fichier à charger et aucune agrégation à effectuer.</p><p>Pandas organise les données dans un <code>DataFrame</code>. Matplotlib les représente : <code>fig</code> désigne la figure et <code>ax</code> la zone de tracé. <code>figsize=(8, 4)</code> donne une figure de 8 × 4 pouces, soit 800 × 400 pixels à 100 DPI.</p><p>Les imports suivants sont communs aux cinq exemples.</p>''' + code('import pandas as pd\nimport matplotlib.pyplot as plt'))]
    for example in EXAMPLES:
        headers = ''.join(f'<th scope="col">{html.escape(name)}</th>' for name in example['data'])
        rows = ''.join('<tr>' + ''.join(f'<td>{html.escape(_number(value))}</td>' for value in row) + '</tr>'
                       for row in zip(*example['data'].values()))
        table = f'<div class="figsize-table-wrap"><table><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table></div>'
        content = f'''<h2>{html.escape(example['title'])}</h2><p><strong>Question :</strong> {html.escape(example['question'])}</p><h3>Les données</h3><p>{html.escape(example['grain'])}</p>{code(dataframe_code(example))}{table}<h3>Construire le graphique</h3>{code(example['plotting'])}<figure class="course-graphic">{graphic(example)}<figcaption>Données pédagogiques fictives · {html.escape(example['chart_title'])}</figcaption></figure><h3>Lire le résultat</h3><p>{html.escape(example['reading'])}</p><p><strong>Quand l’utiliser :</strong> {html.escape(example['use'])}</p><p class="small">{html.escape(example['bridge'])}</p>'''
        if example.get('source'):
            content += f'<p class="small"><a href="{html.escape(example["source"], quote=True)}">Exemple de boxplot dans le catalogue Power BI ↗</a></p>'
        sections.append((example['id'], example['title'].split(' : ')[0], content))
    sections.append(('suite', 'Passer aux données Superstore', '<h2>Passer aux données Superstore</h2><p>Dans les blocs suivants, vous préparerez vous-mêmes les données à représenter : choisir le grain, regrouper les lignes et calculer les indicateurs. Vous retrouverez ces graphiques au fil des exemples et des exercices.</p><a class="button primary" href="01_explorer.html">Explorer les commandes →</a>'))
    nav = ''.join(f'<a href="#{sid}">{html.escape(label)}</a>' for sid, label, _ in sections)
    body = ''.join(f'<section class="course-section" id="{sid}"><p class="eyebrow">Découverte · {html.escape(label)}</p>{content}</section>' for sid, label, content in sections)
    main = f'''<main class="course-main" id="contenu"><div class="course-intro"><p class="eyebrow">Après le QCM de réactivation · Présentation</p><h1>{DISCOVERY['title']}</h1><p>{DISCOVERY['intro']}</p></div><div class="course-layout"><nav class="course-nav" aria-label="Navigation du cours"><p class="eyebrow">Dans ce bloc</p>{nav}<hr><p class="eyebrow">Le parcours</p>{blocks_nav(DISCOVERY['file'])}</nav><div class="course-content">{body}</div><aside class="notebook-panel"><p class="eyebrow">Pour essayer les exemples</p><h2>Ouvrir JupyterLab</h2><p>Vous pouvez créer un notebook Python 3 et exécuter les exemples. Aucun fichier de données n’est nécessaire pour cette présentation.</p><a class="button primary" href="http://localhost:8890/lab" target="_blank" rel="noopener">Ouvrir JupyterLab →</a></aside></div></main>'''
    (root / 'supports' / f'{DISCOVERY["file"]}.html').write_text(head(DISCOVERY['title'], 1) + main + foot(1), encoding='utf8')
