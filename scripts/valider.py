"""Exécute les carnets modèles en isolation et contrôle les résultats indépendamment."""
from pathlib import Path
from decimal import Decimal
from collections import defaultdict
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import csv, json, os, sys, tempfile, contextlib, io, shutil, re, warnings
os.environ.setdefault('MPLCONFIGDIR','/tmp/mpl-cours-cache')
os.environ.setdefault('MPLBACKEND','Agg')
import nbformat
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from contenu_cours import BLOCKS, DAILY
R=Path(__file__).resolve().parents[1];V=R/'validation';V.mkdir(exist_ok=True)
warnings.filterwarnings('ignore',message='FigureCanvasAgg is non-interactive')
rows=list(csv.DictReader((R/'sandbox-notebook/data/commandes.csv').open(encoding='utf-8-sig')))
cat=defaultdict(Decimal);regions=defaultdict(Decimal)
for row in rows:
    value=Decimal(row['Ventes'])
    assert value==Decimal(row['Quantite'])*Decimal(row['Prix_unitaire'])*(1-Decimal(row['Remise']))
    cat[row['Categorie']]+=value;regions[row['Region']]+=value
assert len(rows)==60 and len({r['Commande'] for r in rows})==30
assert sum(cat.values())==Decimal(45831)
assert cat=={'Accessoires':Decimal('1752.5'),'Mobilier':Decimal('13302.5'),'Informatique':Decimal(30776)}
assert regions=={'Nord':Decimal('18979.5'),'Sud':Decimal('14596.5'),'Ouest':Decimal(12255)}
assert (R/'docs/data/commandes.csv').read_bytes()==(R/'sandbox-notebook/data/commandes.csv').read_bytes()
source=R.parent/'TABLEAU/docs'
if source.exists():
    for name in ['site.css','tableau.css']:assert (source/'assets'/name).read_bytes()==(R/'docs/assets'/name).read_bytes()
    assert (source/'data/tp01_commandes_detail.csv').read_bytes()==(R/'docs/data/commandes.csv').read_bytes()
monthly=list(csv.DictReader((R/'sandbox-notebook/data/indicateurs_mensuels.csv').open()))
amounts=[Decimal(r['ventes']) for r in monthly];profits=[Decimal(r['profit']) for r in monthly]
assert sum(amounts)==Decimal(80500) and sum(profits)==Decimal(18350)
expected_variation=[float('nan')]+[float((b/a-1)*100) for a,b in zip(amounts,amounts[1:])]
expected_evolution=[float((v/amounts[0]-1)*100) for v in amounts]
expected_cumul=[sum(amounts[:i+1]) for i in range(6)]
expected_rolling=[float('nan'),float('nan')]+[float(sum(amounts[i-2:i+1])/3) for i in range(2,6)]
expected_margin=[float(p/v*100) for p,v in zip(profits,amounts)]
expected_cum_margin=[float(sum(profits[:i+1])/sum(amounts[:i+1])*100) for i in range(6)]
reports=[]
for b in BLOCKS:
    for corrected in [False,True]:
        folder='corrections' if corrected else 'notebooks'
        name=b['notebook']+('_corrige' if corrected else '')+'.ipynb'
        nb=nbformat.read(R/'sandbox-notebook'/folder/name,as_version=4);nbformat.validate(nb)
        assert all(c.get('execution_count') is None and not c.get('outputs') for c in nb.cells if c.cell_type=='code')
        with tempfile.TemporaryDirectory(prefix='mpl-cours-') as tmp:
            root=Path(tmp);shutil.copytree(R/'sandbox-notebook/data',root/'data');(root/'resultats').mkdir()
            env={'__name__':'__main__'};out=io.StringIO();count=0
            with contextlib.redirect_stdout(out):
                for i,c in enumerate(nb.cells):
                    if c.cell_type=='code':
                        # Seuls les chemins Docker sont redirigés vers la copie de test.
                        code=c.source.replace('/workspace/',root.as_posix()+'/')
                        exec(compile(code,f'{name}:cellule-{i+1}','exec'),env)
                        count+=1
                        plt.close('all')
                if b['n']==1:
                    assert env['ventes'].shape==(60,11)
                    assert env['par_categorie'].to_dict()=={k:float(v) for k,v in cat.items()}
                    np.testing.assert_allclose(env['parts'].sum(),100)
                    if corrected:
                        assert env['par_region'].to_dict()=={k:float(v) for k,v in regions.items()}
                        np.testing.assert_allclose(env['parts_region'].sum(),100)
                        # histogramme : effectifs conservés lors du changement de classes
                        counts,_=np.histogram(env['ventes']['Ventes'],bins=3)
                        assert counts.sum()==60 and len(counts)==3
                    exec(DAILY.replace('/workspace/',root.as_posix()+'/'),env)
                    plt.close('all')
                else:
                    df=env['df']
                    for key,expected in [('variation_pct',expected_variation),('evolution_pct',expected_evolution),('ventes_cumulees',[float(x) for x in expected_cumul]),('moyenne_mobile',expected_rolling),('marge_pct',expected_margin)]:
                        np.testing.assert_allclose(df[key],expected,rtol=1e-10,equal_nan=True)
                    np.testing.assert_allclose(env['marge_globale'],float(sum(profits)/sum(amounts)*100))
                    if corrected:
                        np.testing.assert_allclose(df['marge_cumulee_pct'],expected_cum_margin)
                        assert round(env['moyenne_taux'],2)==22.5
                        assert round(df['marge_cumulee_pct'].iloc[-1],2)==22.8
            expected_files=set()
            for lesson in b['lessons']:
                sources=[lesson['code'],lesson.get('before_code','')]
                if corrected:sources.append(lesson['exercise']['solution'])
                for s in sources:expected_files.update(re.findall(r'/workspace/resultats/([^"\n]+\.png)',s))
            if b['n']==2:expected_files.add('02_mensuel.png')
            for filename in expected_files:
                file=root/'resultats'/filename
                assert file.exists() and file.stat().st_size>5000,filename
            if corrected:
                for file in (root/'resultats').glob('*.png'):
                    shutil.copy2(file,R/'docs/assets'/file.name)
                    (V/'figures').mkdir(exist_ok=True);shutil.copy2(file,V/'figures'/file.name)
                if b['n']==1:
                    gallery=R/'sandbox-notebook/data/visuels';gallery.mkdir(exist_ok=True)
                    for stem in ['01_categories','01_courbe','01_histogramme']:shutil.copy2(root/'resultats'/f'{stem}.png',gallery/f'{stem}.png')
            (V/f'{name}.txt').write_text(out.getvalue())
            reports.append({'notebook':name,'cellules_executees':count,'exports':sorted(expected_files),'statut':'OK'})

class Page(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.links=[];self.code=[];self.inpre=False;self.incode=False;self.buffer=[];self.text=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag in ['a','link'] and a.get('href'):self.links.append(a['href'])
        if tag in ['img','script'] and a.get('src'):self.links.append(a['src'])
        if tag=='pre':self.inpre=True
        if tag=='code' and self.inpre:self.incode=True;self.buffer=[]
    def handle_data(self,data):
        self.text.append(data)
        if self.incode:self.buffer.append(data)
    def handle_endtag(self,tag):
        if tag=='code' and self.incode:self.code.append(''.join(self.buffer));self.incode=False
        if tag=='pre':self.inpre=False
pages={p:Page() for p in (R/'docs').rglob('*.html')}
for p,page in pages.items():
    page.feed(p.read_text())
    assert len(page.ids)==len(set(page.ids)),p
    for i,s in enumerate(page.code):compile(s,f'{p.name}:extrait-{i}','exec')
    assert not re.search(r'\b\d+\s*(?:min(?:utes?)?|heures?)\b|\b\d+\s*h\s*\d+', ' '.join(page.text),re.I),f'Durée pédagogique : {p}'
links=0
for p,page in pages.items():
    for link in page.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:continue
        target=(p.parent/unquote(u.path)).resolve() if u.path else p
        if target.name=='sandbox-notebook.zip':continue
        assert target.exists(),(p,link)
        if u.fragment and target in pages:assert unquote(u.fragment) in pages[target].ids,(p,link)
        links+=1
report={'statut':'OK','versions':{'python':sys.version.split()[0],'pandas':pd.__version__,'matplotlib':matplotlib.__version__,'seaborn':sns.__version__},'execution':'Cellules exécutées dans un espace neuf par carnet, backend Agg ; chemins /workspace redirigés vers une copie temporaire. Aucun test du serveur Docker.','notebooks':reports,'pages_html':len(pages),'liens_locaux':links,'durees_pedagogiques':0,'total_csv':45831,'total_scenario_mensuel':80500,'profit_scenario_mensuel':18350,'marge_globale_pct':float(sum(profits)/sum(amounts)*100)}
(V/'bilan.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
