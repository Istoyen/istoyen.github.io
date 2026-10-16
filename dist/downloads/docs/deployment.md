# Deployment and local use

## Local preview
Open `dist/index.html` directly, or run:

```sh
python3 -m http.server 8080 --directory dist
```

Visit http://localhost:8080. Stop with Ctrl+C. All interactions are browser-local and use generated synthetic records.

## GitHub repository + Pages
1. Create a new repository in your GitHub account and upload this folder's contents (including hidden `.github/`), excluding `.git/`, `.openai/`, and any private files. No repository has been created by this delivery.
2. Use `main` as the branch, or edit the supplied workflow branch filter.
3. In repository Settings → Pages, select **GitHub Actions** as the source.
4. The supplied `.github/workflows/pages.yml` uploads `dist/` and deploys it. Push to main or run the workflow manually. Check the Actions run and open its Pages URL.
5. Relative asset links support repository subpaths. There is no framework install or build step.

To update, edit the website and source assets, run the pipeline if data changed, run validation, refresh downloads, and commit the changes. Deployment automation requires repository permissions; its included workflow has not been run in your GitHub account.

Official guide: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site

## Other static hosting
Upload the contents of `dist/` to a static host. Use `dist` as the publish directory with no build command. The root entry is `index.html`. The three project pages are explicit HTML files, so no single-page-app rewrite is required.

## Sites
This project was prepared using Sites. `.openai/hosting.json` identifies this specific site and declares `dist/` as its static output. New Sites use owner-private access; public recruiter access is a separate sharing choice. Use supported Sites tools for subsequent source synchronization and deployment. A private preview link is not a public portfolio link.

## Pre-share checks
Finish name/contact/resume placeholders, verify real skill claims, retain synthetic-data notices, check downloads and mobile layout, and verify access from the intended audience. Never upload employer source records into this demonstration repository.
