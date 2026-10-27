"""Archive apprenant : liste blanche, sans corrigés, secrets ni travaux personnels."""
from pathlib import Path
import zipfile
R=Path(__file__).resolve().parents[1]
base=R/'sandbox-notebook'
paths=['README.md','Dockerfile','compose.yaml','requirements.txt','.dockerignore','.env.example',
       'notebooks/00_test_postgres.ipynb','notebooks/01_comprendre_graphiques.ipynb','notebooks/02_indicateurs.ipynb',
       'data/commandes.csv','data/indicateurs_mensuels.csv','data/README.md',
       'data/visuels/01_categories.png','data/visuels/01_courbe.png','data/visuels/01_histogramme.png','resultats/.gitkeep']
target=R/'docs/data/sandbox-notebook.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as archive:
    for path in paths:archive.write(base/path,'sandbox-notebook/'+path)
with zipfile.ZipFile(target) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist())==len(paths)
    assert not any('correction' in x or '.Trash' in x or 'Untitled' in x or x.endswith('/.env') for x in archive.namelist())
print(f'Archive apprenant : {len(paths)} fichiers, deux carnets de cours et test PostgreSQL ; sans corrigé.')
