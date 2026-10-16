"""Refresh website downloads from repository source; no private site identity included."""
from pathlib import Path
import shutil, zipfile
R = Path(__file__).resolve().parents[1]
out = R / 'dist' / 'downloads'
out.mkdir(parents=True, exist_ok=True)
folders = ['data','sql','python','projects','powerbi','docs']
for folder in folders:
    shutil.copytree(R/folder, out/folder, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
shutil.copy2(R/'README.md', out/'README.md')
with zipfile.ZipFile(out/'portfolio-projects.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for folder in folders:
        for path in sorted((R/folder).rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts:
                z.write(path, path.relative_to(R))
    z.writestr('README.md', '# Synthetic Healthcare Analytics Project Pack\n\nThis is the analysis-only download. It contains data, SQL, Python, case studies, Power BI assets, and documentation. The complete portfolio delivery also includes the website.\n\nRun `python3 python/build_data.py` followed by `python3 python/validate.py`. Python 3.9+; no external dependencies. The generator creates a browser data asset in dist/assets, but this archive does not include website HTML. All records and results are synthetic. Start with docs/data-dictionary.md and powerbi/README.md.\n')
print('Refreshed downloadable assets and project archive.')
