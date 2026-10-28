"""Questions autonomes après le bloc 04 : aucun corrigé ni code de solution."""
import html


MATH_BLOCK = {
    'file': 'questions_maths',
    'title': 'Questions maths',
    'intro': 'Six calculs appliqués à Superstore : des parts et des taux jusqu’aux indicateurs temporels.',
}

QUESTIONS = [
    {
        'id': 'part-region',
        'title': 'La part du chiffre d’affaires par région',
        'question': 'Quelle proportion des ventes totales représente chaque région ?',
        'tasks': [
            'Calculez la part du chiffre d’affaires de chaque région, en pourcentage.',
            'Représentez les quatre parts avec un graphique à barres horizontales.',
            'Vérifiez que la somme des parts est égale à 100 %, avant l’arrondi d’affichage.',
        ],
        'deliverable': 'La formule, un tableau des parts, le graphique et une phrase de comparaison.',
    },
    {
        'id': 'taux-profit',
        'title': 'Le taux de profit sur ventes',
        'question': 'Quelle catégorie transforme le mieux son chiffre d’affaires en profit ?',
        'tasks': [
            'Calculez les ventes totales, le profit total et le taux de profit sur ventes de chaque catégorie.',
            'Comparez les trois taux avec un graphique à barres.',
            'La catégorie qui vend le plus a-t-elle aussi le taux de profit sur ventes le plus élevé ? Justifiez votre réponse.',
        ],
        'deliverable': 'La formule, un tableau par catégorie, le graphique et une réponse chiffrée.',
    },
    {
        'id': 'evolution-annuelle',
        'title': 'Le taux d’évolution annuel',
        'question': 'De combien les ventes augmentent-elles ou diminuent-elles chaque année ?',
        'tasks': [
            'Calculez le chiffre d’affaires de chaque année, puis son taux d’évolution par rapport à l’année précédente.',
            'Identifiez l’année présentant la plus forte croissance et celle présentant la croissance la plus faible, parmi les années comparables.',
            'Expliquez comment vous traitez la première année du fichier.',
        ],
        'deliverable': 'La formule, un tableau annuel et les deux années identifiées avec leurs taux.',
    },
    {
        'id': 'panier-moyen',
        'title': 'Le panier moyen',
        'question': 'Quel est le montant moyen dépensé par commande dans chaque région ?',
        'tasks': [
            'Calculez le panier moyen pour l’ensemble du fichier, puis pour chaque région.',
            'Comparez les résultats régionaux avec un graphique à barres.',
            'Indiquez quelle région présente le panier moyen le plus élevé et expliquez ce que mesure cet indicateur.',
        ],
        'deliverable': 'La formule, le panier moyen global, un tableau régional, le graphique et votre interprétation.',
    },
    {
        'id': 'profit-cumule',
        'title': 'Le taux de profit cumulé',
        'question': 'Comment évolue le profit rapporté à l’ensemble des ventes accumulées au fil des années ?',
        'tasks': [
            'Calculez, à la fin de chaque année, le taux de profit sur toutes les ventes accumulées depuis le début du fichier.',
            'Représentez ce taux cumulé avec une courbe et décrivez son évolution.',
            'Expliquez en une phrase ce qui distingue cet indicateur d’un taux de croissance.',
        ],
        'deliverable': 'La formule, un tableau annuel, la courbe et deux phrases d’interprétation.',
    },
    {
        'id': 'moyenne-mobile',
        'title': 'La moyenne mobile',
        'question': 'Comment lire la tendance générale des ventes en réduisant les fluctuations mensuelles ?',
        'tasks': [
            'Calculez les ventes mensuelles, puis leur moyenne mobile sur trois mois.',
            'Superposez les ventes mensuelles et la moyenne mobile dans un même graphique, avec une légende.',
            'Expliquez pourquoi la courbe de moyenne mobile est généralement moins irrégulière que celle des ventes mensuelles.',
        ],
        'deliverable': 'La formule, le graphique avec les deux courbes et une explication du lissage.',
    },
]


def build_math_questions(root, head, foot, blocks_nav):
    sections = []
    for index, question in enumerate(QUESTIONS, 1):
        level = 'Fondamentaux' if index <= 4 else 'Approfondissement facultatif'
        tasks = ''.join(f'<li>{html.escape(task)}</li>' for task in question['tasks'])
        sections.append(f'''<section class="course-section" id="{question['id']}">
<p class="eyebrow">Question {index:02} · {level}</p>
<h2>{html.escape(question['title'])}</h2>
<p><strong>{html.escape(question['question'])}</strong></p>
<ol>{tasks}</ol>
<p><strong>À rendre :</strong> {html.escape(question['deliverable'])}</p>
</section>''')
    sections.append('''<section class="course-section" id="suite"><p class="eyebrow">Suite du parcours</p><h2>QCM de synthèse</h2><p>Poursuivez avec les questions sur les notions des blocs 01 à 04.</p><a class="button primary" href="../qcm/qcm_matin.html">Faire le QCM →</a></section>''')
    nav = ''.join(f'<a href="#{q["id"]}">{i:02} · {html.escape(q["title"])}</a>' for i, q in enumerate(QUESTIONS, 1))
    main = f'''<main class="course-main" id="contenu">
<div class="course-intro"><p class="eyebrow">Après le bloc 04 · Avant le QCM de synthèse</p><h1>{MATH_BLOCK['title']}</h1><p>{MATH_BLOCK['intro']}</p></div>
<div class="course-layout">
<nav class="course-nav" aria-label="Navigation des questions"><p class="eyebrow">Dans ce bloc</p>{nav}<a href="#suite">QCM de synthèse</a><hr><p class="eyebrow">Le parcours</p>{blocks_nav(MATH_BLOCK['file'])}</nav>
<div class="course-content"><section class="course-section" id="consignes"><p class="eyebrow">Superstore · Feuille Orders</p><h2>Formuler, calculer et interpréter</h2><p>Utilisez le DataFrame <code>orders</code> du cours. Pour chaque question, écrivez d’abord la formule mathématique, puis traduisez votre calcul en Pandas et réalisez la représentation demandée avec Matplotlib. Les montants restent exprimés dans l’unité monétaire du fichier.</p><p>Les questions 01 à 04 constituent les fondamentaux. Les questions 05 et 06 sont des approfondissements facultatifs, que vous pouvez reprendre après le bloc 05 sur les cumuls et la moyenne mobile.</p></section>{''.join(sections)}</div>
<aside class="notebook-panel"><p class="eyebrow">Atelier Jupyter</p><h2>Poursuivre votre notebook</h2><p>Réalisez vos calculs et vos graphiques dans votre notebook de travail.</p><a class="button primary" href="http://localhost:8890/lab" target="_blank" rel="noopener">Ouvrir JupyterLab →</a></aside>
</div></main>'''
    (root / 'supports' / f'{MATH_BLOCK["file"]}.html').write_text(head(MATH_BLOCK['title'], 1) + main + foot(1), encoding='utf8')
