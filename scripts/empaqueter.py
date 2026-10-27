"""Archive apprenant avec liste blanche ; jamais de corrections ni de résultats de travail."""
from pathlib import Path
import zipfile
R=Path(__file__).resolve().parents[1]
base=R/'sandbox-notebook'
paths=['README.md','Dockerfile','compose.yaml','requirements.txt','.dockerignore','notebooks/01_graphiques_fiables.ipynb','data/commandes.csv','data/README.md','resultats/.gitkeep']
target=R/'docs/data/sandbox-notebook.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as archive:
    for path in paths: archive.write(base/path,'sandbox-notebook/'+path)
with zipfile.ZipFile(target) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist())==len(paths)
    assert not any('correction' in x for x in archive.namelist())
print(f'Archive apprenant : {target.name} ; {len(paths)} fichiers ; sans corrigé.')
