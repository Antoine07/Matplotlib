"""Vérifie le kit sans modifier les notebooks ou résultats des apprenants."""
from pathlib import Path
from decimal import Decimal
from collections import defaultdict
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import csv, json, os, shutil, sys, tempfile, contextlib, io, importlib.metadata
os.environ.setdefault('MPLCONFIGDIR', '/tmp/matplotlib-cours-cache')
os.environ.setdefault('MPLBACKEND', 'Agg')
import nbformat
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
V=R/'validation'
V.mkdir(exist_ok=True)
rows=list(csv.DictReader((R/'sandbox-notebook/data/commandes.csv').open(encoding='utf-8-sig')))
cat=defaultdict(Decimal); sud=defaultdict(Decimal); products=defaultdict(Decimal)
for row in rows:
    amount=Decimal(row['Ventes'])
    expected=Decimal(row['Quantite'])*Decimal(row['Prix_unitaire'])*(1-Decimal(row['Remise']))
    assert amount == expected, row['Ligne']
    cat[row['Categorie']]+=amount
    products[row['Produit']]+=amount
    if row['Region']=='Sud': sud[row['Categorie']]+=amount
assert len(rows)==60 and len({r['Commande'] for r in rows})==30
assert len({r['Ligne'] for r in rows})==60
assert cat=={'Accessoires':Decimal('1752.50'),'Mobilier':Decimal('13302.50'),'Informatique':Decimal('30776')}
assert sum(cat.values())==Decimal('45831')
assert sum(sud.values())==Decimal('14596.50')
assert products['Ordinateur']==Decimal('25925')
assert (R/'docs/data/commandes.csv').read_bytes()==(R/'sandbox-notebook/data/commandes.csv').read_bytes()
source=R.parent/'TABLEAU/docs'
if source.exists():
    assert (source/'data/tp01_commandes_detail.csv').read_bytes()==(R/'docs/data/commandes.csv').read_bytes()
    for name in ['site.css','tableau.css']:
        assert (source/'assets'/name).read_bytes()==(R/'docs/assets'/name).read_bytes()

# Chaque parcours utilise un dossier de travail et un espace de variables neufs.
# Exécution directe des cellules : aucune dépendance à un serveur Jupyter ou à un port.
summary=[]
for folder,name,expected_files in [
    ('notebooks','01_graphiques_fiables.ipynb',['01_categories.png']),
    ('corrections','01_graphiques_fiables_corrige.ipynb',['01_categories.png','02_sud.png','03_audit_corrige.png','04_produits.png'])]:
    notebook=nbformat.read(R/'sandbox-notebook'/folder/name,as_version=4)
    nbformat.validate(notebook)
    with tempfile.TemporaryDirectory(prefix='mpl-validation-') as tmp:
        root=Path(tmp); (root/folder).mkdir(); shutil.copytree(R/'sandbox-notebook/data',root/'data')
        old=Path.cwd(); os.chdir(root/folder)
        env={'__name__':'__main__'}; log=io.StringIO(); count=0
        try:
            with contextlib.redirect_stdout(log):
                for i,c in enumerate(notebook.cells):
                    if c.cell_type=='code':
                        exec(compile(c.source,f'{name}:cellule-{i+1}','exec'),env)
                        count+=1
            for filename in expected_files:
                p=root/'resultats'/filename
                assert p.is_file() and p.stat().st_size>10000, filename
            assert env['par_categorie'].to_dict()=={k:float(v) for k,v in cat.items()}
            assert env['ventes'].shape==(60,11)
            if folder=='corrections':
                assert env['par_categorie_sud'].to_dict()=={k:float(v) for k,v in sud.items()}
                assert env['par_produit'].to_dict()=={k:float(v) for k,v in products.items()}
                for axname,expected in [('ax',cat),('ax_sud',sud),('ax_ok',cat),('ax_produits',products)]:
                    ax=env[axname]
                    actual=dict(zip([t.get_text() for t in ax.get_yticklabels()],[p.get_width() for p in ax.patches]))
                    assert actual=={k:float(v) for k,v in expected.items()},axname
                    assert ax.get_xlim()[0]==0, axname
                # Prouver que le diagnostic est réel et échappe au seul contrôle de somme.
                ax=env['ax_bug']
                wrong=dict(zip([t.get_text() for t in ax.get_yticklabels()],[p.get_width() for p in ax.patches]))
                assert wrong!={k:float(v) for k,v in cat.items()}
                assert sum(wrong.values())==45831
                shutil.copytree(root/'resultats',V/'figures',dirs_exist_ok=True)
                for filename in expected_files:
                    shutil.copy2(root/'resultats'/filename,R/'docs/assets'/filename)
        finally:
            os.chdir(old); plt.close('all')
        (V/(folder+'_execution.txt')).write_text(log.getvalue(),encoding='utf-8')
        summary.append({'notebook':name,'cellules_code_executees':count,'exports_attendus':expected_files,'statut':'OK'})

class Page(HTMLParser):
    def __init__(self): super().__init__(); self.ids=[]; self.links=[]; self.python=[]; self.incode=False; self.inpre=False; self.buffer=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a' and a.get('href'):self.links.append(a['href'])
        if tag in ['script','img'] and a.get('src'):self.links.append(a['src'])
        if tag=='link' and a.get('href'):self.links.append(a['href'])
        if tag=='pre':self.inpre=True
        if tag=='code' and self.inpre:self.incode=True;self.buffer=[]
    def handle_data(self,data):
        if self.incode:self.buffer.append(data)
    def handle_endtag(self,tag):
        if tag=='code' and self.incode:
            value=''.join(self.buffer)
            if not value.startswith('docker '):self.python.append(value)
            self.incode=False
        if tag=='pre':self.inpre=False
pages={p:Page() for p in (R/'docs').rglob('*.html')}
for p,doc in pages.items():
    doc.feed(p.read_text())
    assert len(doc.ids)==len(set(doc.ids)),f'ID dupliqué : {p}'
    for i,src in enumerate(doc.python): compile(src,f'{p.name}:extrait-{i}','exec')
links=0
for p,doc in pages.items():
    for href in doc.links:
        u=urlsplit(href)
        if u.scheme or u.netloc:continue
        dest=(p.parent/unquote(u.path)).resolve() if u.path else p
        # L'archive est créée après la validation, car elle inclut le notebook contrôlé.
        if dest.name=='sandbox-notebook.zip':continue
        assert dest.exists(),f'Lien absent : {p} -> {href}'
        if u.fragment and dest in pages:assert unquote(u.fragment) in pages[dest].ids,f'Ancre absente : {href}'
        links+=1
versions={m:importlib.metadata.version(m) for m in ['matplotlib','pandas','numpy','nbformat','nbclient','jupyterlab','ipykernel']}
report={'validation':'OK','python':sys.version.split()[0],'versions':versions,'execution':'Cellules exécutées séquentiellement par exec dans un espace neuf par notebook, backend Agg ; pas un test du serveur Jupyter.','notebooks':summary,'liens_locaux_verifies':links,'pages_html':len(pages),'donnees':{'lignes':len(rows),'commandes':30,'total_ventes':45831,'categories':{k:str(v) for k,v in cat.items()}}}
(V/'bilan.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
