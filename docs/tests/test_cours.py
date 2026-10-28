"""Vérifications reproductibles du classeur Superstore et des supports."""
from pathlib import Path
from collections import Counter
import importlib.util
import json
import sys
import unittest
from html.parser import HTMLParser
from urllib.parse import urlsplit

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'sample_-_superstore.xls'
REQUIRED = {'Order ID', 'Order Date', 'Region', 'Category', 'Sub-Category', 'Sales', 'Profit', 'Discount', 'Quantity'}


@unittest.skipUnless(importlib.util.find_spec('xlrd'), 'xlrd est requis pour lire le classeur .xls')
class SuperstoreDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.orders = pd.read_excel(DATA, sheet_name='Orders', engine='xlrd')
        cls.orders['Order Date'] = pd.to_datetime(cls.orders['Order Date'])

    def test_schema_and_observation_grain(self):
        self.assertTrue(REQUIRED.issubset(self.orders.columns))
        self.assertEqual(self.orders.shape, (10194, 21))
        self.assertEqual(self.orders['Order ID'].nunique(), 5111)
        self.assertGreater(len(self.orders), self.orders['Order ID'].nunique())
        self.assertEqual(int(self.orders.isna().sum().sum()), 0)

    def test_sales_profit_aggregates(self):
        self.assertAlmostEqual(self.orders['Sales'].sum(), 2326534.354, places=2)
        self.assertAlmostEqual(self.orders['Profit'].sum(), 292296.81, places=2)
        by_category = self.orders.groupby('Category')[['Sales', 'Profit']].sum()
        self.assertEqual(by_category['Sales'].idxmax(), 'Technology')
        self.assertEqual(self.orders['Region'].nunique(), 4)

    def test_months_and_percent_change(self):
        monthly = self.orders.set_index('Order Date').resample('MS')['Sales'].sum()
        self.assertEqual(len(monthly), 48)
        self.assertTrue(monthly.index.is_monotonic_increasing)
        change = monthly.pct_change() * 100
        self.assertTrue(pd.isna(change.iloc[0]))
        self.assertAlmostEqual(monthly.iloc[-1] / monthly.iloc[0] - 1, 4.866835, places=5)

class PowerBITPDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = ROOT / 'data' / 'ventes_reseau_powerbi.csv'
        cls.ventes = pd.read_csv(cls.path, parse_dates=['Date'])

    def test_dataset_grain_dimensions_and_sandbox_copy(self):
        ventes = self.ventes
        self.assertEqual(set(ventes.columns), {'Ligne', 'Commande', 'Date', 'Region', 'Canal', 'Categorie', 'Produit', 'Quantite', 'Chiffre_affaires', 'Cout_achat'})
        self.assertEqual(ventes['Ligne'].nunique(), len(ventes))
        self.assertGreater(len(ventes), ventes['Commande'].nunique())
        self.assertFalse(ventes.isna().any().any())
        self.assertEqual(set(ventes['Date'].dt.year), {2025})
        self.assertEqual(ventes['Date'].dt.to_period('M').nunique(), 12)
        self.assertEqual(set(ventes['Canal']), {'En ligne', 'Magasin'})
        self.assertEqual(ventes['Region'].nunique(), 4)
        self.assertEqual(ventes['Categorie'].nunique(), 4)
        self.assertTrue((ventes['Quantite'] > 0).all())
        by_order = ventes.groupby('Commande')[['Date', 'Region', 'Canal']].nunique()
        self.assertTrue((by_order == 1).all().all())
        self.assertEqual(self.path.read_bytes(), (ROOT.parent / 'sandbox-notebook' / 'data' / self.path.name).read_bytes())

    def test_sales_costs_and_margin_survive_aggregation(self):
        ventes = self.ventes.copy()
        self.assertTrue((ventes[['Chiffre_affaires', 'Cout_achat']] >= 0).all().all())
        ventes['Marge'] = ventes['Chiffre_affaires'] - ventes['Cout_achat']
        self.assertAlmostEqual(ventes['Chiffre_affaires'].sum(), 405188.35, places=2)
        self.assertAlmostEqual(ventes['Marge'].sum(), 109813.35, places=2)
        for dimension in ['Region', 'Categorie', 'Canal']:
            grouped = ventes.groupby(dimension)[['Chiffre_affaires', 'Cout_achat', 'Marge']].sum()
            self.assertAlmostEqual(grouped['Chiffre_affaires'].sum(), ventes['Chiffre_affaires'].sum(), places=8)
            self.assertAlmostEqual(grouped['Marge'].sum(), ventes['Marge'].sum(), places=8)
            self.assertTrue((grouped['Chiffre_affaires'] > 0).all())
            self.assertTrue((grouped['Marge'] - (grouped['Chiffre_affaires'] - grouped['Cout_achat'])).abs().max() < 1e-8)


class TeachingAssetTests(unittest.TestCase):
    def test_discovery_follows_reactivation_with_five_distinct_graphics(self):
        import re
        from xml.etree import ElementTree

        index = (ROOT / 'index.html').read_text(encoding='utf8')
        # Examiner les cartes du parcours, sans confondre les liens du bandeau.
        cards = index[index.index('<nav class="path-grid">'):]
        positions = [cards.index(f'href="{link}"') for link in [
            'qcm/reactivation_00.html', 'supports/00_decouvrir_graphiques.html', 'supports/01_explorer.html']]
        self.assertEqual(positions, sorted(positions))
        page = (ROOT / 'supports' / '00_decouvrir_graphiques.html').read_text(encoding='utf8')
        graphics = re.findall(r'<svg\b.*?</svg>', page, re.S)
        self.assertEqual(len(graphics), 5)
        self.assertEqual(len(set(graphics)), 5)
        for graphic in graphics:
            svg = ElementTree.fromstring(graphic)
            self.assertEqual(svg.attrib['role'], 'img')
            self.assertIsNotNone(svg.find('{http://www.w3.org/2000/svg}title'))
        self.assertEqual(page.count('<div class="code-block">'), 11)
        self.assertNotIn('class="exercise"', page)
        self.assertNotIn('<fieldset', page)
        self.assertNotIn('Mise en commun', page)
        self.assertIn('href="01_explorer.html"', page)

    def test_discovery_data_support_the_displayed_interpretations(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            from discovery_content import EXAMPLES, dataframe_code, box_summary
        finally:
            sys.path.pop(0)
        frames = {}
        for example in EXAMPLES:
            scope = {'pd': pd, 'print': lambda *args: None}
            exec(dataframe_code(example), scope)
            frames[example['id']] = scope[example['variable']]
            compile(example['plotting'], example['id'], 'exec')

        products = frames['barres'].set_index('Produit')['Ventes']
        self.assertEqual(products.idxmax(), 'Écran')
        self.assertEqual(products.max(), 2100)
        stores = frames['colonnes'].set_index('Magasin')
        gains = stores['CA_2025'] - stores['CA_2024']
        self.assertEqual(gains.idxmax(), 'Nord')
        self.assertEqual(gains.max(), 30)
        self.assertEqual(stores['CA_2025'].idxmax(), 'Sud')
        months = frames['courbe']
        self.assertEqual(months.loc[months['Ventes'].diff() < 0, 'Mois'].tolist(), ['Mar', 'Juin'])
        self.assertEqual(frames['nuage'].shape, (10, 3))
        self.assertGreater(frames['nuage']['Budget'].corr(frames['nuage']['Ventes']), 0.8)
        orders = frames['boxplot']
        self.assertEqual(orders.shape, (10, 3))
        spread = orders.quantile(0.75) - orders.quantile(0.25)
        self.assertEqual(spread.idxmax(), 'Nord')
        for name in orders:
            lo, q1, med, q3, hi, fliers = box_summary(orders[name].tolist())
            self.assertEqual([q1, med, q3], orders[name].quantile([0.25, 0.5, 0.75]).tolist())
            self.assertEqual(fliers, [350] if name == 'Nord' else [])
            self.assertLessEqual(lo, q1)
            self.assertGreaterEqual(hi, q3)

    def test_course_pages_and_corrections_exist(self):
        for name in ['01_explorer', '02_comparer', '03_rentabilite', '04_temps_et_variations', '05_cumuls', '06_distributions']:
            self.assertTrue((ROOT / 'supports' / f'{name}.html').is_file())
            self.assertTrue((ROOT / 'corrections' / f'{name}.html').is_file())

    def test_student_and_instructor_notebooks_are_separate(self):
        student = list((ROOT / 'notebooks').glob('*.ipynb'))
        teacher = list((ROOT / 'formateur' / 'notebooks').glob('*.ipynb'))
        self.assertEqual(len(student), 0)
        self.assertEqual(len(teacher), 8)
        self.assertFalse(any('corrige' in p.name.lower() for p in student))
        shared_notebooks = ROOT.parent / 'sandbox-notebook' / 'notebooks'
        course_notebooks = {'00_demarrage.ipynb','01_exploration.ipynb','02_comparaisons.ipynb','03_rentabilite.ipynb','04_serie_temporelle.ipynb','05_cumuls_avance.ipynb','06_boxplots_avance.ipynb','tp_binomes.ipynb'}
        self.assertFalse(course_notebooks.intersection(p.name for p in shared_notebooks.glob('*.ipynb')))
        self.assertFalse(any('corrige' in p.name.lower() for p in shared_notebooks.glob('*.ipynb')))

    def test_all_notebooks_are_valid_json_without_saved_outputs(self):
        for path in list((ROOT / 'notebooks').glob('*.ipynb')) + list((ROOT / 'formateur' / 'notebooks').glob('*.ipynb')):
            nb = json.loads(path.read_text(encoding='utf8'))
            self.assertEqual(nb['nbformat'], 4, path.name)
            for cell in nb['cells']:
                if cell['cell_type'] == 'code':
                    self.assertEqual(cell['outputs'], [], path.name)
                    compile(''.join(cell['source']), path.name, 'exec')

    def test_quiz_sizes_and_four_choices(self):
        expected = {'reactivation_00':16, 'qcm_matin':15, 'qcm_avance':8}
        for path in (ROOT / 'qcm').glob('*.html'):
            page = path.read_text(encoding='utf8')
            questions = page.count('<fieldset ')
            self.assertEqual(questions, expected[path.stem], path.name)
            self.assertEqual(page.count('type="radio"'), 4 * questions, path.name)

    def test_quiz_answer_positions_are_balanced_and_preserve_correct_text(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            from construire import QUIZZES, distribute_quiz_answers
        finally:
            sys.path.pop(0)

        class Answers(HTMLParser):
            def __init__(self):
                super().__init__()
                self.questions = []
                self.current = None
                self.option = None
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == 'fieldset':
                    self.current = {'answer': int(attrs['data-answer']), 'why': attrs['data-why'], 'options': {}}
                if tag == 'label' and 'quiz-option' in attrs.get('class', '').split():
                    self.option = {'value': None, 'text': []}
                if tag == 'input' and self.option is not None:
                    self.option['value'] = int(attrs['value'])
            def handle_data(self, data):
                if self.option is not None:
                    self.option['text'].append(data)
            def handle_endtag(self, tag):
                if tag == 'label' and self.option is not None:
                    text = ''.join(self.option['text'])
                    self.current['options'][self.option['value']] = text[2:].lstrip()
                    self.option = None
                if tag == 'fieldset':
                    self.questions.append(self.current)
                    self.current = None

        fixture = [(f'Question {i}', ['Réponse A', 'Réponse B', 'Réponse C', 'Réponse D'], i, 'Explication') for i in range(4)]
        for original, prepared in zip(fixture, distribute_quiz_answers('fixture', fixture)):
            self.assertEqual(prepared[1][prepared[2]], original[1][original[2]])

        for key in ['reactivation_00', 'qcm_matin', 'qcm_avance']:
            source = QUIZZES[key][1]
            snapshot = json.dumps(source, ensure_ascii=False)
            prepared = distribute_quiz_answers(key, source)
            self.assertEqual(prepared, distribute_quiz_answers(key, source))
            self.assertEqual(snapshot, json.dumps(source, ensure_ascii=False))
            parser = Answers()
            parser.feed((ROOT / 'qcm' / f'{key}.html').read_text(encoding='utf8'))
            self.assertEqual(len(parser.questions), len(source))
            positions = [question['answer'] for question in parser.questions]
            counts = Counter(positions)
            self.assertEqual(set(counts), {0, 1, 2, 3}, key)
            self.assertLessEqual(max(counts.values()) - min(counts.values()), 1, key)
            self.assertFalse(any(positions[i] == positions[i-1] == positions[i-2] for i in range(2, len(positions))), key)
            for rendered, (_, options, answer, why) in zip(parser.questions, source):
                self.assertEqual(set(rendered['options'].values()), set(options), key)
                self.assertEqual(rendered['options'][rendered['answer']], options[answer], key)
                self.assertEqual(rendered['why'], why, key)

    def test_quiz_feedback_and_reset_controls_exist(self):
        script = (ROOT / 'assets' / 'quiz.js').read_text(encoding='utf8')
        self.assertIn("addEventListener('change'", script)
        self.assertIn("quiz-next", script)
        self.assertIn("Réponse attendue", script)
        self.assertIn("scoreBox.textContent=''", script)
        for key in ['reactivation_00', 'qcm_matin', 'qcm_avance']:
            page = (ROOT / 'qcm' / f'{key}.html').read_text(encoding='utf8')
            self.assertIn('id="quiz-next"', page)
            self.assertIn('hidden data-answer=', page)

    def test_first_block_has_examples_and_exercises_without_inline_solutions(self):
        page = (ROOT / 'supports' / '01_explorer.html').read_text(encoding='utf8')
        positions = [
            page.index('Charger et décrire la feuille Orders'),
            page.index('Exercice 01'),
            page.index('Comparer lignes et commandes par catégorie'),
            page.index('Exercice 02'),
            page.index('Suivre le nombre de commandes par année'),
            page.index('Exercice 03'),
        ]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn('Mise en commun', page)
        self.assertEqual(page.count('<figure class="course-graphic">'), 2)
        self.assertNotIn('qcm-section', page)
        self.assertLess(page.index('Charger la feuille Orders'), page.index('Exemples guidés, graphiques et exercices'))

    def test_index_places_each_quiz_after_its_course_block(self):
        page = (ROOT / 'index.html').read_text(encoding='utf8')
        self.assertNotIn('qcm-index', page)
        quiz_order = ['reactivation_00', 'qcm_matin', 'qcm_avance']
        positions = [page.index(f'href="qcm/{key}.html"') for key in quiz_order]
        self.assertEqual(positions, sorted(positions))
        self.assertLess(page.index('href="qcm/reactivation_00.html"'), page.index('href="supports/01_explorer.html"'))
        self.assertLess(page.index('href="supports/04_temps_et_variations.html"'), page.index('href="qcm/qcm_matin.html"'))
        self.assertLess(page.index('href="supports/04_temps_et_variations.html"'), page.index('href="supports/questions_maths.html"'))
        self.assertLess(page.index('href="supports/questions_maths.html"'), page.index('href="qcm/qcm_matin.html"'))
        self.assertIn('16 questions', page)
        self.assertIn('15 questions', page)
        for filename in ['01_explorer', '02_comparer', '03_rentabilite']:
            support = (ROOT / 'supports' / f'{filename}.html').read_text(encoding='utf8')
            self.assertEqual(support.count('class="course-section qcm-section"'), 0, filename)
        support = (ROOT / 'supports' / '04_temps_et_variations.html').read_text(encoding='utf8')
        self.assertEqual(support.count('class="course-section qcm-section"'), 0)
        for filename in ['06_distributions']:
            support = (ROOT / 'supports' / f'{filename}.html').read_text(encoding='utf8')
            self.assertEqual(support.count('class="course-section qcm-section"'), 1, filename)
        self.assertFalse((ROOT / 'qcm' / 'qcm_comparaisons.html').exists())

    def test_course_opens_jupyterlab_without_prepared_student_notebook(self):
        page = (ROOT / 'supports' / '01_explorer.html').read_text(encoding='utf8')
        self.assertIn('href="http://localhost:8890/lab"', page)
        self.assertNotIn('lab/tree/notebooks/', page)
        self.assertNotIn('Code à compléter', page)
        self.assertFalse((ROOT.parent / 'sandbox-notebook' / 'notebooks' / '01_exploration.ipynb').exists())

    def test_morning_courses_have_multiple_examples_exercises_and_visible_graphics(self):
        expected = {'01_explorer':3, '02_comparer':4, '03_rentabilite':4, '04_temps_et_variations':3}
        for name, count in expected.items():
            page = (ROOT / 'supports' / f'{name}.html').read_text(encoding='utf8')
            self.assertEqual(page.count('<article class="learning-sequence">'), count, name)
            self.assertGreaterEqual(page.count('<figure class="course-graphic">'), count - 1, name)
            self.assertEqual(page.count('<div class="exercise" id="exercice-'), count, name)

    def test_local_html_links_resolve(self):
        class Refs(HTMLParser):
            def __init__(self):
                super().__init__()
                self.refs = []
                self.ids = set()
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if 'id' in attrs:
                    self.ids.add(attrs['id'])
                for key, value in attrs.items():
                    if key in {'href', 'src'} and value:
                        self.refs.append(value)
        for source in ROOT.rglob('*.html'):
            parser = Refs()
            parser.feed(source.read_text(encoding='utf8'))
            for ref in parser.refs:
                url = urlsplit(ref)
                if url.scheme or not url.path:
                    if url.fragment and not url.scheme:
                        self.assertIn(url.fragment, parser.ids, f'{source.relative_to(ROOT)} → {ref}')
                    continue
                target = (source.parent / url.path).resolve()
                self.assertTrue(target.exists(), f'{source.relative_to(ROOT)} → {ref}')
                if url.fragment and target.suffix == '.html':
                    target_parser = Refs()
                    target_parser.feed(target.read_text(encoding='utf8'))
                    self.assertIn(url.fragment, target_parser.ids, f'{source.relative_to(ROOT)} → {ref}')


class CalculationFixtureTests(unittest.TestCase):
    def test_ratio_of_sums_differs_from_mean_of_rates(self):
        sales = pd.Series([100.0, 300.0])
        profit = pd.Series([10.0, 90.0])
        ratio_sums = profit.sum() / sales.sum() * 100
        mean_rates = (profit / sales * 100).mean()
        self.assertEqual(ratio_sums, 25.0)
        self.assertEqual(mean_rates, 20.0)

    def test_first_change_and_zero_denominator(self):
        series = pd.Series([100.0, 120.0])
        self.assertTrue(pd.isna(series.pct_change().iloc[0]))
        self.assertAlmostEqual(series.pct_change().iloc[1] * 100, 20.0)
        ratio = pd.Series([2.0]).div(pd.Series([0.0]).replace(0, float('nan')))
        self.assertTrue(pd.isna(ratio.iloc[0]))


if __name__ == '__main__':
    unittest.main()
