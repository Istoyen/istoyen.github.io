# Busayo Oyewole — Healthcare Analytics Portfolio

A complete, editable portfolio for a **Healthcare Data Analyst / BI / SQL reporting automation specialist**.

> All datasets, identifiers, projects, and analytical findings are synthetic. No AssistRx data, confidential business rules, or verified employer achievements are included. Professional background is based on Busayo’s supplied resume. This is not a claim of actual healthcare performance.

## Open the website
Open `dist/index.html` in a browser. The dashboard works locally without a server or internet connection. If preferred, run `python3 -m http.server 8080 --directory dist` and visit http://localhost:8080.

## Reproduce the analysis
Python 3.9+ with the standard library is sufficient; there are no package dependencies.

```sh
python3 python/build_data.py
python3 python/validate.py
```

The generator uses seed 42 and a fixed snapshot date of **2026-07-01**. It rebuilds the CSV extracts, SQLite database, summary outputs, and browser data asset. It replaces generated data intentionally; do not use these paths for real records.

## Included
- `dist/`: responsive website, three individual project pages, an interactive dashboard, and downloads.
- `projects/`: GitHub-ready case studies: patient access, shipment quality, onboarding/bridge turnaround.
- `sql/`: executable SQLite schema, views, and three analysis queries.
- `python/`: deterministic generation, analysis execution, and meaningful integrity/edge-case checks.
- `data/`: original synthetic records, modeled extracts, summaries, and SQLite database.
- `powerbi/`: Power Query import function and queries, DAX measures, theme, model and page specifications.
- `docs/`: data/metric dictionary, personalization checklist, resume draft, impact evidence worksheet, deployment and SQL portability notes.

## Baseline synthetic findings
1,200 referrals; 975 paid starts; 82 pending cases; 143 closed cases. Snapshot paid-start conversion = 81.25% (displayed as 81.3%). Median completed paid-start turnaround = 16 calendar days. Shipment feed = 1,776 rows; flagged = 232; accepted = 1,544.

## Make it yours
Start with `docs/personalize.md`. Name, email, LinkedIn, professional background and resume download have been personalized. GitHub profile: https://github.com/Istoyen. Website: https://istoyen.github.io/

Source repository: https://github.com/Istoyen/istoyen.github.io Keep the synthetic labels intact.

## Power BI status
Import-ready assets and a detailed build guide are included. This package does **not** include a compiled `.pbix` or `.pbit`, and the DAX/M assets have not been executed inside Power BI Desktop. The browser dashboard is implemented and uses the same CSV-derived records.

## Publish
See `docs/deployment.md`. GitHub Pages workflow is included for Istoyen/istoyen.github.io. Sites hosting identity, if present in `.openai/hosting.json`, belongs to this specific portfolio instance and should be removed when someone else forks it.

## Updating packaged downloads
After editing any project, SQL, data, or documentation file, run `python3 python/package_downloads.py` to refresh website downloads. Keep sensitive information out of this public-facing project pack. The build is entirely synthetic by design.
